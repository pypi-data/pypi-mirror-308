from pathlib import Path

from package_schemes.interfaces import Project, UvLockV1
from package_schemes.interfaces.pyproject import Pyproject
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.tree import Tree

from uv_audit.scan.safery import SafetyScanProvider

console = Console()

tree = Tree('Rich Tree')


class UvAuditManager(object):
    verbose: bool
    ignore_codes: list[str]
    scan_extra_deps: bool
    scan_dev_deps: bool

    def __init__(self) -> None:
        path = Path.cwd()
        self.scan_manager = SafetyScanProvider()
        self.project = Project(
            Pyproject(path / 'pyproject.toml'),
            UvLockV1(path / 'uv.lock'),
        )

    def set_options(self, verbose: bool, ignore_codes: list[str], scan_extra_deps: bool, scan_dev_deps: bool):
        self.verbose = verbose
        self.ignore_codes = ignore_codes
        self.scan_extra_deps = scan_extra_deps
        self.scan_dev_deps = scan_dev_deps

    def scan(self):
        if self.verbose:
            console.print('Started audit:')
            console.print(Padding(f'- {self.project.pyproject.file}', (0, 0, 0, 1)))
            console.print(Padding(f'- {self.project.lock.file}', (0, 0, 0, 1)))

        total_error = 0
        for package in self.project.get_packages():
            package_has_error = False
            for vulnerability in self.scan_manager.get_package_vulnerability(package):
                total_error += 1
                package_has_error = True

                url = f'https://pyup.io{vulnerability.more_info_path}'
                da = Group(
                    f'[bright_cyan italic]{url}',
                    Padding(Markdown(markup=f'> {vulnerability.advisory}'), (0, 0, 1, 0)),
                    'Affected versions: [bright_yellow]'
                    + '[/bright_yellow] | [bright_yellow]'.join(vulnerability.specs),
                )
                console.print(
                    Panel(
                        da,
                        title_align='left',
                        title=f'[bold bright_red]{package.name}[/bold bright_red] '
                        f'[bright_yellow]{package.version}[/bright_yellow] - '
                        f'[bold bright_red]{vulnerability.cve}[/bold bright_red]',
                    )
                )

            if self.verbose and not package_has_error:
                console.print(f'[bright_green]{package.name}[/bright_green] - {package.version}')

        return total_error
