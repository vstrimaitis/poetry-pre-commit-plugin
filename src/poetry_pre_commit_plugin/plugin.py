import subprocess
from pathlib import Path
from typing import Optional

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import TERMINATE
from cleo.events.event_dispatcher import EventDispatcher
from cleo.io.io import IO
from poetry.console.application import Application
from poetry.console.commands.add import AddCommand
from poetry.console.commands.install import InstallCommand
from poetry.plugins.application_plugin import ApplicationPlugin


class PreCommitPlugin(ApplicationPlugin):  # type: ignore
    def activate(self, application: Application) -> None:
        application.event_dispatcher.add_listener(TERMINATE, self._handle_post_command)

    def _handle_post_command(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        # this attribute seems to only be present on a TERMINATE event, so be careful
        # to not use similar logic if listening to different events
        exit_code: int = event._exit_code

        if exit_code != 0:
            # The command failed, so the plugin shouldn't do anything
            return

        if not self._is_pre_commit_package_installed():
            return

        if self._get_git_directory_path() is None:
            # Not in a git repository - can't install hooks
            return

        if self._are_pre_commit_hooks_installed():
            # pre-commit hooks already installed - nothing to do
            return

        command = event.command
        if isinstance(command, InstallCommand) or isinstance(command, AddCommand):
            if command.option("dry-run") is True:
                return
            self._install_pre_commit_hooks(event.io)

    def _install_pre_commit_hooks(self, io: IO) -> None:
        try:
            io.write_line("<info>Installing pre-commit hooks...</>")
            return_code = subprocess.check_call(
                ["poetry", "run", "pre-commit", "install"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if return_code == 0:
                io.write_line(
                    "<fg=green>pre-commit hooks successfully installed</info>"
                )
            else:
                io.write_error_line("<error>Failed to install pre-commit hooks</>")
        except Exception as e:
            io.write_error_line(
                "<error>Failed to install pre-commit hooks due to an unexpected error</>"
            )
            io.write_error_line(f"<error>{e}</>")

    def _is_pre_commit_package_installed(self) -> bool:
        try:
            output = subprocess.check_output(
                ["poetry", "run", "pip", "freeze", "--local"],
            ).decode()
            return "pre-commit" in output
        except FileNotFoundError:
            return False

    def _are_pre_commit_hooks_installed(self) -> bool:
        git_root = self._get_git_directory_path()
        if git_root is None:
            return False
        return (git_root / "hooks" / "pre-commit").exists()

    def _get_git_directory_path(self) -> Optional[Path]:
        try:
            result = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"],
            )
            return Path(result.decode().strip()) / ".git"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
