"""Pretty print package version."""

import logging
from types import MappingProxyType

from .scm_common import Commit

log = logging.getLogger(__name__)


class Version:
    """Pretty print version for SCM commit."""

    Styles = MappingProxyType(
        {
            "internal": "{count}.{extra}.{type}.{hash}",
            "public": "{count}.{extra}",
            "base": "{extra}",
        }
    )

    def __init__(self, commit: Commit):
        self.commit = commit

    def fmt(
        self, style: str = "internal", extra: str = "", prn_name: bool = False
    ) -> str:
        """Format scm version."""
        info = dict(self.commit.info)
        if info["count"] != "0":
            info["count"] = "rev." + info["count"]
        else:
            info["count"] = ""
        log.debug("info %s", info)
        xstyle = self.Styles[style]
        txt = xstyle.format(extra=extra, **info)
        txt = ".".join([e for e in txt.split(".") if e])
        txt = "-" + txt if txt else ""
        txt = f"{info['tag']}{txt}"
        log.debug("txt %s", txt)
        if prn_name:
            txt = f"{info['name']} {txt}"
        return txt
