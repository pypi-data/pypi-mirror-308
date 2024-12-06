from cleo.io.io import IO
from packaging_version_git import GitVersion
from poetry.core.constraints.version import Version
from poetry.poetry import Poetry

from poetry_git_version_plugin.config import GitVersionPluginConfig, ReleaseTypeEnum


class VersionService(object):
    config: GitVersionPluginConfig

    def __init__(self, config: GitVersionPluginConfig) -> None:
        self.config = config

    def get_version(self):
        if self.config.release_type == ReleaseTypeEnum.tag:
            return GitVersion.from_tag()

        if self.config.release_type == ReleaseTypeEnum.alpha:
            return GitVersion.from_commit(as_alpha=True)

        if self.config.release_type == ReleaseTypeEnum.beta:
            return GitVersion.from_commit(as_beta=True)

        if self.config.release_type == ReleaseTypeEnum.rc:
            return GitVersion.from_commit(as_rc=True)

        if self.config.release_type == ReleaseTypeEnum.post:
            return GitVersion.from_commit(as_post=True)

        if self.config.release_type == ReleaseTypeEnum.dev:
            return GitVersion.from_commit(as_dev=True)

        return GitVersion.from_tag()

    def safe_get_version(self, io: IO, poetry: Poetry) -> Version | None:
        try:
            version = self.get_version()
            return Version.parse(str(version))

        except Exception as ex:
            io.write_error_line(str(ex))
            return None
