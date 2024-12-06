import logging
from unittest.mock import MagicMock

from poetry_git_version_plugin.services import VersionService

logger = logging.getLogger('app')


class TestVersionService(object):
    def test_init(self, git_version_service) -> None:
        assert isinstance(git_version_service, VersionService)

    def test_get_version(self, git_version_service: VersionService) -> None:
        version = git_version_service.get_version()
        logger.error(f'testing version - {version}')

    def test_safe_get_version(self, git_version_service: VersionService) -> None:
        version = git_version_service.safe_get_version(MagicMock(spec=None), MagicMock(spec=None))
        logger.error(f'testing version - {version}')
