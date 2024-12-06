import contextvars
import copy
import json
import logging
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import sleep
from typing import Dict, NoReturn, Optional


import yaml
from jsonschema import validate
from requests import HTTPError

from workflows_emulator.lib.http_utils import (
    AUTH_OAUTH2,
    request as authenticated_request,
)
from workflows_emulator.render import assign_var, render_config, run_code
from workflows_emulator.utils import (
    Context, DISCOVERY_DOCUMENTS_PATH, NextStep,
    ParallelTask, ReturnValue, RisingThread, STEP_NOT_FOUND, SpecialNextStep,
    StepConfig,
    UnhandledBranchError, WorkflowError, load_package_config, RuntimeError as
    CustomRuntimeError
)

logger = logging.getLogger('workflows')

# TODO: implement SafeLineLoader to enrich the error messages
# class SafeLineLoader(SafeLoader):
#     def construct_mapping(self, node, deep=False):
#         mapping = super(SafeLineLoader, self).construct_mapping(node,
#         deep=deep)
#         # Add 1 so line numbering starts at 1
#         mapping['__line__'] = node.start_mark.line + 1
#         return mapping

def load_config(config_path: str) -> dict:
    """Load a configuration file from a given path."""
    with open(config_path) as file:
        return yaml.safe_load(file)


WORKFLOW_SCHEMA = load_package_config('workflow-schema.json')

LOCK = Lock()

def load_workflow(config_path: str) -> Dict:
    """Load a workflow from a given path."""
    workflow = load_config(config_path)
    validate(workflow, WORKFLOW_SCHEMA)
    return workflow


def execute_workflow(config: dict | list[dict], params: dict) -> any:
    """
    Runs a workflow given a configuration and parameters.

    We need the whole config inside the prams to run try/retry "predicate" and
    to be able to call other sub-workflows. Also, having it in the context is
    cleaner than storing it in a global variable
    """
    # if the root is a list of steps instead of a map with a 'main' key
    if isinstance(config, list):
        config = {'main': {'steps': config}}

    main_config = config.pop('main')
    logger.info(f"Running 'main' workflow: params -> {json.dumps(params)}")
    return execute_subworkflow(main_config, params, config)


def get_params(workflow_params: list[str | dict], runtime_params: dict) -> dict:
    context = {}
    for param in workflow_params:
        if isinstance(param, dict):
            param_name = list(param.keys())[0]
            param_value = param[param_name]
            context[param_name] = runtime_params.get(param_name, param_value)
        else:
            try:
                context[param] = runtime_params[param]
            except KeyError:
                raise KeyError(f"Missing workflow parameter: {param}")
    return context


def execute_subworkflow(workflow: dict, params: dict, context: dict) -> any:
    """Executes a subworkflow given a configuration and parameters.

    The context is required since it stores the rest of sub-workflows that might
    need to be called.
    """
    solved_params = get_params(workflow.get('params', []), params)
    logger.info(f"Subworkflow running")
    logger.debug(
        f"Subworkflow started: : params -> {json.dumps(solved_params)}"
    )
    context.update(solved_params)
    _ctxt, next_step, ret_value = execute_steps_list(workflow['steps'], context)
    if next_step not in [None, SpecialNextStep.END]:
        raise ValueError(f"Step {next_step} not found in the workflow")
    logger.info(f"Subworkflow complete: result -> {ret_value}")
    return ret_value


class Step(ABC):

    def __init__(self, step_id: str, config: StepConfig, context: Context):
        self.step_id = step_id
        self.config = config
        self.context = context
        step_type = self.__class__.__name__.replace('Step', '').lower()
        self.logger = logging.getLogger('workflows.' + step_type)

    @abstractmethod
    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        pass


def keep_only_subworkflows(context: Context) -> Context:
    """
    Receives a Context and returns a new context with only the subworkflows
    """
    return {
        key: value
        for key, value in context.items()
        if isinstance(value, dict) and 'steps' in value
    }


class StepReturn(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        ret_value = render_config(self.config['return'], self.context)
        return self.context, None, ret_value


class StepFor(Step):

    @staticmethod
    def inclusive_range(start: int | float, end: int | float):
        """Returns a range from start to end inclusive."""
        # if start is float
        if isinstance(start, float) or isinstance(end, float):
            elements = []
            while start <= end:
                elements.append(start)
                start += 1.0
            return elements
        return range(start, end + 1)

    def get_iterator(self):
        config = self.config['for']
        if 'in' in config:
            return render_config(config['in'], self.context)
        iterable_range = render_config(config['range'], self.context)
        return StepFor.inclusive_range(*iterable_range)

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        config = self.config['for']
        copy_context = copy.deepcopy(self.context)
        # determine the kind of loop
        iterable = self.get_iterator()
        index_variable = config.get('index', '__index')
        value_variable = config.get('value', '__value')
        next_step = None
        ret_value = None
        for index, value in enumerate(iterable):
            self.logger.debug(
                f"  Iterating: {index_variable}={index}, "
                f"{value_variable}={value}"
            )
            copy_context[index_variable] = index
            copy_context[value_variable] = value
            copy_context, next_step, ret_value = StepSteps(
                step_id=self.step_id,
                config=config,
                context=copy_context
            ).execute()
            if next_step == SpecialNextStep.BREAK:
                next_step = None
                break
            if next_step == SpecialNextStep.CONTINUE:
                next_step = None
                continue
            if ret_value is not None or next_step is not None:
                break
        copy_context.pop(index_variable, None)
        copy_context.pop(value_variable, None)

        # update the parent context with the new variables
        offending_vars = [
            key for key in copy_context.keys()
            if key not in self.context
        ]
        if offending_vars:
            self.logger.warning(
                f'Variables {offending_vars} in `for` step "{self.step_id}" '
                f'are not parent context and will be discarded'
            )
        update_vars = {
            key: value
            for key, value in copy_context.items()
            if key in self.context and self.context[key] != value
        }
        self.context.update(update_vars)
        return self.context, next_step, ret_value


class StepRaise(Step):

    def execute(self) -> NoReturn:
        rendered_error = render_config(self.config['raise'], self.context)
        # suppose that the error is a string by default
        # TODO: add the step_id to the trace
        if isinstance(rendered_error, str):
            raise CustomRuntimeError(rendered_error)
        if isinstance(rendered_error, dict):
            raise CustomRuntimeError(**rendered_error)
        raise SyntaxError(
            f"Error type not supported: {type(rendered_error)}"
        )


class StepNext(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        self.logger.debug(f"Next step: {self.config.get('next')}")
        return self.context, self.config.get('next'), None


class StepTry(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        step = self.config
        context = self.context
        try:
            return execute_step(self.step_id, step['try'], context)
        except WorkflowError as err:
            error_var = step['except']['as']
            context[error_var] = err.payload
            self.logger.error(f"Error caught: {err.payload}")
            return execute_steps_list(step['except']['steps'], context)


class StepRetry(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        step = self.config
        context = self.context
        logger = self.logger
        retry_config = render_config(step['retry'], context)
        backoff_config = retry_config.get('backoff', {})
        delay = backoff_config.get('delay', 1)
        max_delay = backoff_config.get('max_delay', 60)
        multiplier = backoff_config.get('multiplier', 1)
        predicate = retry_config.get('predicate', None)
        max_retries = retry_config.get('max_retries', 0)
        raised_err = None
        for retry_num in range(max_retries + 1):
            try:
                if retry_num > 0:
                    logger.debug(f"Retry -> Attempt {retry_num}")
                return execute_step(self.step_id, step['try'], context)
            except WorkflowError as err:
                raised_err = err
                # check if we need to execute the predicate
                if predicate is not None:
                    logger.info(f"Running predicate")
                    run_result = execute_subworkflow(
                        workflow=predicate,
                        params={'e': err.payload},
                        context=keep_only_subworkflows(context)
                    )
                    # if the predicate asserts it's not a retryable error break
                    if not run_result:
                        logger.error("Error type not supported by predicate")
                        break
                # do the sleep
                if 'backoff' in retry_config:
                    logger.debug(f"Waiting {delay} seconds")
                    if delay < max_delay:
                        sleep(delay)
                        delay *= multiplier
                    # we run out of time but the issue was not fixed
                    else:
                        logger.error(f"Timeout {max_delay=}")
                        break
        # if retries run out, but not the max_delay and the predicate
        # didn't fix it
        else:
            logger.error(f"Max retries reached: {max_retries}")
        if 'except' in step:
            error_var = step['except']['as']
            context[error_var] = raised_err.payload.to_dict()
            return execute_steps_list(step['except']['steps'], context)
        else:
            raise raised_err


class StepSteps(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Executes a list of steps.

        The steps are executed sequentially. If a step returns a value, the
        execution stops and the value is returned.

        All variables assigned within are accessible in the upper workflow
        context.
        """
        step_list = self.config['steps']
        context = self.context
        new_context, next_step, ret_value = execute_steps_list(
            step_list,
            context
        )
        context.update(new_context)
        return context, next_step, ret_value


def preserve_context(context: Context, new_context: Context) -> Context:
    """Preserves the context variables that are not in the new context."""
    new_vars = {
        key: new_context.get(key, value)
        for key, value in context.items()
    }
    context.update(new_vars)
    return context


class StepAssign(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Assigns a value to a variable in the context.

        Variable names are rendered before assignment. So it allows for map
        and list index assignment."""
        LOCK.acquire()
        context = self.context
        _context = {}  # only for logging purposes
        for var in self.config['assign']:
            var_name = list(var.keys())[0]
            var_value = var[var_name]
            rendered_value = render_config(var_value, context)
            root_key, new_val = assign_var(var_name, rendered_value, context)
            context[root_key] = new_val
            _context[root_key] = new_val
        self.logger.debug(json.dumps(_context))
        LOCK.release()
        return context, self.config.get('next'), None


class StepCall(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Executes a call step.

        The call step can be a call to a Google API, a subworkflow, or a Python
        function from the standard library."""
        step = self.config
        context = self.context
        logger = self.logger
        rendered_step = render_config(step, context)
        callable_name = rendered_step['call']
        if callable_name.startswith('googleapis.'):
            logger.debug(f"Calling Connector: {callable_name}")
            run_result = StepCall.execute_connector(rendered_step)
        # call another subworkflow
        elif callable_name in context:
            logger.debug(f"Call Subworkflow: {callable_name}")
            run_result = execute_subworkflow(
                workflow=context[callable_name],
                params=rendered_step.get('args', {}),
                context=keep_only_subworkflows(context)
            )
        # call a python function from the standard library
        else:
            fn_args = rendered_step.get('args', {})
            log_args = ', '.join([f"{k}={v}" for k, v in fn_args.items()])
            logger.debug(f"Call std lib method: `{callable_name}({log_args})`")
            args_str = "**_args" if isinstance(fn_args, dict) else "*_args"
            run_result = run_code(
                code=f'{callable_name}({args_str})',
                context={**context, '_args': fn_args}
            )
        if 'result' in rendered_step:
            context[step['result']] = run_result

        return context, step.get('next'), None

    @staticmethod
    def execute_connector(rendered_step: StepConfig) -> Context:
        """Executes a connector step.

        The connector step is a call to a Google API. It retrieves the
        service url and http verb from the discovery documents."""

        # googleapis.service_name.version.[resource1[.resource2[...]]].method
        call_parts = rendered_step['call'].split('.')
        _, service_name, version, *resources, method = call_parts
        # @formatter:off
        service_discovery_file_path = f'{DISCOVERY_DOCUMENTS_PATH}/{service_name}_{version}.json'
        # @formatter:on
        service_discovery_config = load_package_config(
            service_discovery_file_path
        )
        # iteratively consume the parts to get the final config
        next_part = service_discovery_config
        for resource in resources:
            next_part = next_part['resources'][resource]
        final_config = next_part['methods'][method]

        # now that we have the actual method config, extract the information
        scopes = final_config['scopes']
        http_verb: str = final_config['httpMethod']
        base_url = service_discovery_config['rootUrl']
        config_path = final_config['path'].replace('+', '')
        service_path = service_discovery_config['servicePath']
        final_url_template = base_url + service_path + config_path
        # replaces the variables in the url
        final_url = run_code(
            code=f'f"""{final_url_template}"""',
            context=rendered_step['args']
        )
        # make the request
        logger.debug(f"{http_verb.upper()} {final_url}")
        result = authenticated_request(
            url=final_url,
            auth=AUTH_OAUTH2,
            body=rendered_step['args'].get('body', None),
            method=http_verb,
            scopes=scopes
        )
        return result['body']


class StepParallel(Step):

    def filter_vars(self, new_context: dict):
        """
        Provided the modified context from the parallel execution, modifies the
        outer context accordingly
        """
        shared_vars = list(set(self.config['parallel'].get('shared', [])))
        new_keys = []
        # get new variables that won't be shared
        for key, val in new_context.items():
            if key not in self.context:
                new_keys.append(key)
        if new_keys:
            self.logger.debug(
                f"New variables defined inside the parallel step "
                f"{new_keys} wont be shared with the outer context"
            )
        # get modified variables that where not in the shared list
        offending_keys = []
        for key, val in new_context.items():
            if key in self.context and key not in shared_vars and self.context[key] != val:
                offending_keys.append(key)
        if len(offending_keys) > 0:
            raise SyntaxError(
                f"Variables {offending_keys} where modified inside the parallel step but "
                f"where not in the shared list {shared_vars}"
            )
        new_values = {
            key: new_context[key]
            for key in shared_vars
            if key in new_context
        }
        self.context.update(new_values)

    def check_raise_results(self, exceptions_lookup: dict[str, WorkflowError]):
        if exceptions_lookup == {}:
            return
        # filter only exceptions
        branches_exceptions = [
            {
                'id': str(branch_id),
                'error': {
                    'context': f'{err.__context__.__class__.__name__}:'
                               f' {err.__context__}',
                    'payload': err.payload,
                }
            }
            for branch_id, err in exceptions_lookup.items()
        ]
        self.logger.error(f"Branches with errors: {exceptions_lookup}")
        # get all the tags
        tags = {
            tag
            for err_info in exceptions_lookup.values()
            if 'tags' in err_info.payload
            for tag in err_info.payload.tags
        }
        # if it contains subclases of WorkflowError and no tags capture them too
        exception_names = [err.__class__.__name__ for err in exceptions_lookup.values()]
        tags.add(UnhandledBranchError.__name__)
        tags.update(exception_names)
        # if there are exceptions, raise a new branch error to handle them
        if len(branches_exceptions) > 0:
            raise UnhandledBranchError(
                message='UnhandledBranchError: One or more branches or '
                        'iterations encountered an unhandled runtime error',
                tags=sorted(list(tags)),
                branches=branches_exceptions,
                truncated=False,
            )

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        inner_step = self.config['parallel']
        args = {
            'concurrency_limit': inner_step.get('concurrency_limit')
        }
        if 'for' in inner_step:
            args.update({
                'task_configs': self.get_for_tasks(),
                'value_var':  inner_step['for'].get('value', '__value'),
                'index_var': inner_step['for'].get('index', '__index'),
            })
        else:
            args.update({
                'task_configs': self.get_branch_tasks()
            })
        new_context = self.execute_task_config(**args)
        return new_context, self.config.get('next'), None

    def get_branch_tasks(self) -> list[ParallelTask]:
        """Generates task configuration to run from a fot loop"""
        branches_config = self.config['parallel']['branches']
        tasks: list[ParallelTask] = []
        context_copy = copy.deepcopy(self.context)
        for branch_config in branches_config:
            step_id = list(branch_config.keys())[0]
            step_config = branch_config[step_id]
            tasks.append(
                ParallelTask(
                    id=step_id,
                    config=step_config,
                    context=context_copy
                )
            )
        return tasks

    def get_for_tasks(self) -> list[ParallelTask]:
        """Generates task configuration to run from a fot loop"""
        for_config = self.config['parallel']
        step_executor = StepFor(self.step_id, for_config, self.context)
        iterations = list(step_executor.get_iterator())
        inner_config = for_config['for']
        context_copy = copy.deepcopy(self.context)
        tasks = []
        for val in iterations:
            tasks.append(
                ParallelTask(
                    id=val,
                    config={'steps': inner_config['steps']},
                    context=context_copy
                )
            )
        return tasks

    def execute_task_config(
        self,
        task_configs: list[ParallelTask],
        concurrency_limit: int= None,
        index_var: str = '__index',
        value_var: str = '__value',
    ) -> Context:
        """Generates task configuration to run from a fot loop"""

        running_threads = []
        context_copy = copy.deepcopy(self.context)
        ctx_var_index = contextvars.ContextVar(index_var)
        ctx_var_value = contextvars.ContextVar(value_var)
        with ThreadPoolExecutor(max_workers=concurrency_limit):
            for index, task_config in enumerate(task_configs):
                ctx_var_value.set(task_config['id'])
                ctx_var_index.set(index)
                thread = RisingThread(
                        target=run_with_context,
                        kwargs={
                            'fn' : execute_step,
                            'thread_context': contextvars.copy_context(),
                            'step_id': str(task_config['id']),
                            'config': task_config['config'],
                            'context': context_copy,
                        }
                    )
                running_threads.append(thread)
            # run all threads
            task_ids = [task_config['id'] for task_config in task_configs]
            for thread in running_threads:
                thread.start()
            # wait for all threads
            errors: dict[str, WorkflowError] = {}
            for task_id, thread in zip(task_ids, running_threads):
                try:
                    thread.join()
                except WorkflowError as err:
                    errors[task_id] = err
        self.filter_vars(context_copy)
        # format possible result errors
        self.check_raise_results(errors)
        # context was checked, and it's safe to return (if we didn't raise)
        return self.context


class StepSwitch(Step):

    def execute(self) -> tuple[Context, Optional[NextStep], ReturnValue]:
        """Checks each condition of the switch and executes the inner step.

        Inner step is run if condition evaluates to True.
        """
        context = self.context
        for condition in self.config['switch']:
            # evaluate the condition and remove the field
            condition_copy = copy.deepcopy(condition)
            evaluated_condition = render_config(
                condition_copy['condition'],
                context
            )
            if not isinstance(evaluated_condition, bool):
                raise SyntaxError(
                    f'The switch condition must evaluate to a boolean: `'
                    f'{condition_copy["condition"]}`'
                )
            if evaluated_condition:
                condition_copy.pop('condition')
                context, next_step, ret_value = execute_step(
                    step_id=self.step_id,
                    config=condition_copy,
                    context=context
                )
                if ret_value is not None or next_step is not None:
                    return context, next_step, ret_value
        return context, self.config.get('next'), None


def execute_steps_list(
    steps: list[dict[str, StepConfig]],
    context: Context,
    next_step: NextStep = None,
) -> tuple[Context, Optional[NextStep], ReturnValue]:
    """
    It either returns a context and a ret_value or a step_id to go to and
    continue execution

    Returns:
    - context: The context after executing the steps
    - next_step: The step id to go to, or None to continue with the next step
    - ret_value: The return value of the steps
    """
    ret_value = None
    while True:
        step_id, step_index, step_config = get_step(steps, next_step)
        # if the next_step was SET but NOT FOUND, return to search in the parent
        if step_index == STEP_NOT_FOUND:
            break
        logger.info(f"Step running: `{step_id}`")
        context, next_step, ret_value = execute_step(
            step_id,
            step_config,
            context
        )
        if ret_value is not None:
            break
        # if the step did not return a next_step, get the next step in the list
        match next_step:
            case SpecialNextStep.END:
                # keep it's 'end' value for the outer scope
                break
            case None:
                # continue with the next step in the list
                if step_index + 1 < len(steps):
                    next_step = list(steps[step_index + 1].keys())[0]
                    continue
                else:
                    break
            case _:
                # allow to search for the next_step in the next iteration
                continue
        # if the list returned a next_step, will be used in the next iteration
    return context, next_step, ret_value


def run_with_context(
    thread_context: contextvars.Context,
    fn: callable,
    *args,
    **kwargs
):
    return thread_context.run(fn, *args, **kwargs)

def execute_step(
    step_id: NextStep,
    config: StepConfig,
    context: Context
) -> tuple[Context, Optional[NextStep], ReturnValue]:
    """Executes the step and returns the context and, if any, the result and
    return value

    Returns:
    - context: The context after executing the step
    - next: None to go to the next step, or the step id to go to a specific step
    - return: The return value of the step
    """
    logger.debug(f"Step type: {'/'.join(config.keys())}")
    try:
        StepExecutor = get_step_executor(config)
        step_instance = StepExecutor(
            step_id=step_id,
            config=config,
            context=context
        )
        return step_instance.execute()
    except WorkflowError as err:
        raise err
    except (
        ConnectionError, TypeError, ValueError, KeyError, RuntimeError,
        SystemError, TimeoutError, IndexError, RecursionError, ZeroDivisionError
    ) as err:
        raise WorkflowError(
            message=err.args[0],
            tags=[err.__class__.__name__],
        )
    except HTTPError as err:
        body = err.response.text
        if 'application/json' in err.response.headers.get('Content-Type', ''):
            body = err.response.json()
        raise WorkflowError(
            message=err.args[0],
            tags=[err.__class__.__name__],
            code=err.response.status_code,
            headers=dict(err.response.headers),
            body=body,
        )


def get_step(
    steps: list[dict], step_id: NextStep
) -> tuple[str | None, int, dict]:
    """Returns the index of the step with the given id, or -1 if not found."""
    if step_id is None:
        step_id = list(steps[0].keys())[0]
        return step_id, 0, steps[0][step_id]
    for index, step in enumerate(steps):
        if list(step.keys())[0] == step_id:
            return step_id, index, step[step_id]
    return None, STEP_NOT_FOUND, {}


def get_step_executor(step_config: StepConfig) -> type[Step]:
    """Step factory method.

    Determines the executor to use given a step config. The lookup is
    prioritized since —for example— `retry` and `try` behave different. Or in a
    step having `assign` and `next`we would like to run `assign` first and let
    it handle the `next` field.
    """
    step_type_lookup = [
        ('call', StepCall),
        ('return', StepReturn),
        ('assign', StepAssign),
        ('raise', StepRaise),
        ('retry', StepRetry),
        ('try', StepTry),
        ('steps', StepSteps),
        ('for', StepFor),
        ('parallel', StepParallel),
        ('switch', StepSwitch),
        ('next', StepNext),
    ]
    for step_field, step_executor in step_type_lookup:
        if step_field in step_config:
            return step_executor
    raise SyntaxError(f"Step type not found in {list(step_config.keys())}")
