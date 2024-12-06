from poetry_git_version_plugin.config import PLUGIN_NAME
from poetry_git_version_plugin.exceptions import PluginException, plugin_exception_wrapper


class TestPluginException(object):
    def test_init_base_ex(self):
        ex = RuntimeError('lorem')

        plugin_ex = PluginException(ex)

        assert str(plugin_ex) == f'<b>{PLUGIN_NAME}</b>: RuntimeError: lorem'

    def test_init_test(self):
        plugin_ex = PluginException('lorem')

        assert str(plugin_ex) == f'<b>{PLUGIN_NAME}</b>: lorem'


class TestPluginExceptionWrapper(object):
    def test_plugin_ex(self):
        @plugin_exception_wrapper
        def inner():
            raise PluginException('lorem')

        try:
            inner()

        except PluginException as ex:
            assert str(ex) == f'<b>{PLUGIN_NAME}</b>: lorem'

    def test_base_ex(self):
        @plugin_exception_wrapper
        def inner():
            raise RuntimeError('lorem')

        try:
            inner()

        except PluginException as ex:
            assert str(ex) == f'<b>{PLUGIN_NAME}</b>: RuntimeError: lorem'
