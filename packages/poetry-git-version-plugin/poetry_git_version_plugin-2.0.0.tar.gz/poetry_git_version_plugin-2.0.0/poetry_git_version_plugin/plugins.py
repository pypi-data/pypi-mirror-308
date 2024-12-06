from __future__ import annotations

from cleo.io.io import IO
from cleo.io.outputs.output import Verbosity
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin
from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry

from poetry_git_version_plugin.config import PLUGIN_NAME, GitVersionPluginConfig
from poetry_git_version_plugin.exceptions import plugin_exception_wrapper
from poetry_git_version_plugin.services import VersionService


class GitVersionCommand(Command):
    name = 'git-version'

    @plugin_exception_wrapper
    def handle(self) -> None:  # pragma: no cover
        self.io.write_line(str(self.poetry.package.version))


class SetGitVersionCommand(Command):
    name = 'set-git-version'

    @plugin_exception_wrapper
    def handle(self) -> None:  # pragma: no cover
        version = str(self.poetry.package.version)

        try:
            self.poetry.pyproject.data['tool']['poetry']['version'] = version  # type: ignore

        except KeyError as ex:
            self.io.write_line(f'Error with parsing pyproject: {ex}')
            return

        self.io.write_line(f'The new version has been installed: {version}')

        self.poetry.pyproject.save()


class PoetryGitVersionPlugin(Plugin):
    """Плагин определения версии по гит тегу."""

    @plugin_exception_wrapper
    def activate(self, poetry: Poetry, io: IO):  # pragma: no cover
        io.write_line(f'<b>{PLUGIN_NAME}</b>: Init', Verbosity.VERBOSE)

        config = GitVersionPluginConfig()
        version = VersionService(config).safe_get_version(io, poetry)

        if version is not None:
            poetry.package.version = version

        io.write_line(f'<b>{PLUGIN_NAME}</b>: Finished\n', Verbosity.VERBOSE)


class PoetryGitVersionApplicationPlugin(ApplicationPlugin):
    commands = [GitVersionCommand, SetGitVersionCommand]
