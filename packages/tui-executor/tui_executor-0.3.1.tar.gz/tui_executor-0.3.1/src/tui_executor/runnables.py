import contextlib
import queue
import textwrap
from typing import Callable
from typing import Dict
from typing import List

from rich.console import Console
from rich.markup import escape
from rich.text import Text

from tui_executor.client import MyClient
from tui_executor.kernel import MyKernel
from tui_executor.utils import create_code_snippet
from tui_executor.utils import create_code_snippet_renderable


class FunctionRunnableKernel(FunctionRunnable):
    def __init__(self, kernel: MyKernel, func: Callable, args: List, kwargs: Dict, input_queue: queue.Queue):
        super().__init__(func, args, kwargs, input_queue)
        self.kernel: MyKernel = kernel
        self.startup_timeout = 60  # seconds
        self.console = Console(record=True, width=240)
        self.running = False

    def is_running(self):
        return self.running

    def run(self):

        self.running = True

        self.signals.data.emit(f"----- Running script '{self.func_name}' in kernel")

        snippet = create_code_snippet(self._func, self._args, self._kwargs)

        self.signals.data.emit("The code snippet:")
        self.signals.data.emit(create_code_snippet_renderable(self._func, self._args, self._kwargs))
        self.signals.data.emit("")

        client = MyClient(self.kernel, startup_timeout=self.startup_timeout)
        try:
            client.connect()
        except RuntimeError as exc:
            self.signals.error.emit(exc)
            return

        msg_id = client.execute(snippet, allow_stdin=True)

        DEBUG and LOGGER.debug(f"{id(client)}: {msg_id = }")

        while True:
            try:
                io_msg = client.get_iopub_msg(msg_id, timeout=1.0)

                if io_msg['parent_header']['msg_id'] != msg_id:
                    DEBUG and LOGGER.debug(f"{id(client)}: Skipping {io_msg = }")
                    continue

                io_msg_type = io_msg['msg_type']
                io_msg_content = io_msg['content']

                DEBUG and LOGGER.debug(f"{id(client)}: {io_msg = }")

                if io_msg_type == 'stream':
                    if 'text' in io_msg_content:
                        text = io_msg_content['text'].rstrip()
                        self.signals.data.emit(text)
                elif io_msg_type == 'status':
                    if io_msg_content['execution_state'] == 'idle':
                        # self.signals.data.emit("Execution State is Idle, terminating...")
                        DEBUG and LOGGER.debug(f"{id(client)}: Execution State is Idle, terminating...")
                        self.collect_response_payload(client, msg_id, timeout=1.0)
                        break
                    elif io_msg_content['execution_state'] == 'busy':
                        # self.signals.data.emit("Execution State is busy...")
                        DEBUG and LOGGER.debug(f"{id(client)}: Execution State is busy...")
                        continue
                    elif io_msg_content['execution_state'] == 'starting':
                        # self.signals.data.emit("Execution State is starting...")
                        DEBUG and LOGGER.debug(f"{id(client)}: Execution State is starting...")
                        continue
                elif io_msg_type == 'display_data':
                    if 'data' in io_msg_content:
                        DEBUG and LOGGER.debug(f"{id(client)}: display data of type {io_msg_content['data'].keys()}")
                        if 'text/html' in io_msg_content['data']:
                            text = io_msg_content['data']['text/html'].rstrip()
                            self.signals.html.emit(text)
                        elif 'image/png' in io_msg_content['data']:
                            data = io_msg_content['data']['image/png']
                            self.signals.png.emit(data)
                        elif 'text/plain' in io_msg_content['data']:
                            text = io_msg_content['data']['text/plain'].rstrip()
                            self.signals.data.emit(text)
                elif io_msg_type == 'execute_input':
                    ...  # ignore this message type
                    #     self.signals.data.emit("The code snippet:")
                    #     source_code = io_msg_content['code']
                    #     syntax = Syntax(source_code, "python", theme='default')
                    #     self.signals.data.emit(syntax)
                elif io_msg_type == 'error':
                    if 'traceback' in io_msg_content:
                        traceback = io_msg_content['traceback']
                        self.signals.data.emit(Text.from_ansi('\n'.join(traceback)))
                else:
                    self.signals.error.emit(RuntimeError(f"Unknown io_msg_type: {io_msg_type}"))

            except queue.Empty:
                DEBUG and LOGGER.debug(f"{id(client)}: Catching on empty queue -----------")
                # We fall through here when no output is received from the kernel. This can mean that the kernel
                # is waiting for input and therefore this is a good opportunity to check for stdin messages.
                with contextlib.suppress(queue.Empty):
                    in_msg = client.get_stdin_msg(timeout=0.1)

                    DEBUG and LOGGER.debug(f"{id(client)}: {in_msg = }")

                    if in_msg['msg_type'] == 'input_request':
                        prompt = in_msg['content']['prompt']
                        response = self.handle_input_request(prompt)
                        client.input(response)
            except Exception as exc:
                # We come here after a kernel interrupt that leads to incomplete
                LOGGER.error(f"{id(client)}: Caught Exception: {exc}", exc_info=True)
                self.signals.data.emit(exc)

        client.disconnect()
        self.running = False
        self.signals.finished.emit(self, self.func_name, True)

    def handle_input_request(self, prompt: str = None) -> str:
        """
        This function is called when a stdin message is received from the kernel.

        Args:
            prompt: the text that was given as a prompt to the user

        Returns:
            A string that will be sent to the kernel as a reply.
        """
        if prompt:
            if self._check_for_input and all(pattern not in prompt for pattern in self._input_patterns):
                self.signals.data.emit(
                    textwrap.dedent(
                        f"""\
                        [red][bold]ERROR: [/]The input request prompt message doesn't match any of the expected prompt messages.[/]
                        [default]→ input prompt='{escape(prompt)}'[/]
                        [default]→ expected=({", ".join(f"'{escape(x)}'" for x in self._input_patterns)})[/]

                        [blue]Ask the developer of the task to match up the input request patterns and the prompt.[/]
                        """
                    )
                )

            self.signals.data.emit(escape(prompt))
            self.signals.input.emit(prompt)

            response = self._input_queue.get()
            self._input_queue.task_done()
            return response
        else:
            # The input() function had no prompt argument
            self.signals.data.emit(
                textwrap.dedent(
                    f"""\
                    [red][bold]ERROR: [/]No prompt was given to the input request function.[/]
                    An input request was detected from the Jupyter kernel, but no message was given to describe the 
                    request. Ask the developer of the task to pass a proper message to the input request.

                    [blue]An empty string will be returned to the kernel.[/]
                    """
                )
            )
            return ''

    def collect_response_payload(self, client, msg_id, timeout: float):
        try:
            shell_msg = client.get_shell_msg(msg_id, timeout=timeout)
        except queue.Empty:
            DEBUG and LOGGER.debug(f"{id(client)}: No shell message available for {timeout}s....")
            self.signals.data.emit(
                "[red]No result received from kernel, this might happen when kernel is interrupted.[/]")
            return

        msg_type = shell_msg["msg_type"]
        msg_content = shell_msg["content"]

        DEBUG and LOGGER.debug(f"{id(client)}: {shell_msg = }")

        if msg_type == "execute_reply":
            status = msg_content['status']
            if status == 'error' and 'traceback' in msg_content:
                # We are not sending this traceback anymore to the Console output
                # as it was already handled in the context of the io_pub_msg.
                self.signals.data.emit(f"{status = }")
                traceback = msg_content['traceback']
                self.signals.data.emit(Text.from_ansi('\n'.join(traceback)))
