import logging
from typing import Any, Optional

from packaging_version_git import GitVersion

from uv_version.collectors.base import BaseCollector

logger = logging.getLogger('uv-version')


class GitCollector(BaseCollector):
    def collect(self) -> Optional[str]:
        return str(GitVersion.from_commit(as_post=True))

    def data(self) -> Optional[dict[str, Any]]:
        return {}
