from pprint import pp

import pytest
from typer.testing import CliRunner

from uv_audit import cli


class TestCli(object):
    @pytest.fixture()
    def runner(self):
        return CliRunner()

    def test_root(self, runner: CliRunner):
        result = runner.invoke(cli)
        pp(result.output)
        assert result.exit_code == 0

    def test_version(self, runner: CliRunner):
        result = runner.invoke(cli, ['--version'])
        pp(result.output)
        assert result.exit_code == 0
