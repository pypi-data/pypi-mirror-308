import importlib.util
from collections.abc import Generator
from pathlib import Path
from typing import Any, Optional

import ijson
from package_schemes import Package
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from uv_audit.scan.base import BaseScanProvider, PackageVulnerability


class SafetyScanProvider(BaseScanProvider):
    def __init__(self) -> None:
        safety_db_dir = Path(importlib.util.find_spec('safety_db').origin).parent  # type: ignore

        self.insecure_path = safety_db_dir / 'insecure.json'
        self.insecure_full_path = safety_db_dir / 'insecure_full.json'

    def __get_record_in_insecure(self, key: str) -> Optional[list[str]]:
        with open(self.insecure_path, encoding='utf-8') as file:
            for package_name, value in ijson.kvitems(file, ''):
                if package_name == key:
                    return list(value)
        return None

    def __get_record_in_insecure_full(self, key: str) -> Optional[list[dict[str, Any]]]:
        with open(self.insecure_full_path, encoding='utf-8') as file:
            for package_name, value in ijson.kvitems(file, ''):
                if package_name == key:
                    return value
        return None

    def get_package_vulnerability(self, package: Package) -> Generator[PackageVulnerability, Any, Any]:
        # def get_package_vulnerability(self, package: Package) -> Generator[PackageVulnerability, Any, Any]:
        specifier_versions = self.__get_record_in_insecure(package.name)

        if specifier_versions is None:
            return

        target_version = Version(package.version)

        founded = False
        for specifier_version in specifier_versions:
            specifier = SpecifierSet(specifier_version)

            if target_version in specifier:
                founded = True
                break

        if not founded:
            return

        v1 = self.__get_record_in_insecure_full(package.name)

        if v1 is None:
            return

        for vulnerability_spec in v1:
            for specifier_version in vulnerability_spec['specs']:
                specifier = SpecifierSet(specifier_version)

                if target_version in specifier:
                    yield PackageVulnerability.model_validate(vulnerability_spec)
