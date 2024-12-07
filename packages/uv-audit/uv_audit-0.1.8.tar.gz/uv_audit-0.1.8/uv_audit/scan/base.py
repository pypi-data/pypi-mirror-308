import abc
from collections.abc import Generator
from typing import Any

from package_schemes import Package
from pydantic import BaseModel


class PackageVulnerability(BaseModel):
    advisory: str
    cve: str
    id: str
    more_info_path: str
    specs: list[str]
    v: str


class BaseScanProvider(abc.ABC):
    @abc.abstractmethod
    def get_package_vulnerability(self, package: Package) -> Generator[PackageVulnerability, Any, Any]:
        pass
