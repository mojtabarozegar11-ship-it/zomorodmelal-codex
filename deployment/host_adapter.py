from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class DeploymentResult:
    success: bool
    status: str
    returncode: Optional[int] = None
    stdout: str = ""
    stderr: str = ""


class HostDeploymentAdapter:
    """Explicit host adapter boundary; disabled unless the host opts in."""

    def __init__(self, enabled: Optional[bool] = None, command: Optional[str] = None, timeout: int = 60) -> None:
        raw_enabled = os.environ.get("MASTER_AGENT_DEPLOY_ENABLED", "false").lower()
        self.enabled = enabled if enabled is not None else raw_enabled in {"1", "true", "yes"}
        self.command = command if command is not None else os.environ.get("MASTER_AGENT_DEPLOY_COMMAND", "")
        self.timeout = max(1, min(int(timeout), 300))

    def _argv(self) -> List[str]:
        if not self.command:
            raise ValueError("deployment command is not configured")
        argv = shlex.split(self.command)
        if not argv or any(token in {"&&", "||", ";", "|", ">", ">>", "<"} for token in argv):
            raise ValueError("deployment command must be a simple argv list")
        return argv

    def deploy(self) -> DeploymentResult:
        if not self.enabled:
            return DeploymentResult(False, "adapter_disabled")
        try:
            argv = self._argv()
            completed = subprocess.run(argv, shell=False, capture_output=True, text=True, timeout=self.timeout)
            return DeploymentResult(completed.returncode == 0, "completed" if completed.returncode == 0 else "failed", completed.returncode, completed.stdout[-4000:], completed.stderr[-4000:])
        except ValueError as exc:
            return DeploymentResult(False, "configuration_error", None, "", str(exc))
        except subprocess.TimeoutExpired as exc:
            return DeploymentResult(False, "timeout", None, "", str(exc))
        except OSError as exc:
            return DeploymentResult(False, "execution_error", None, "", str(exc))
