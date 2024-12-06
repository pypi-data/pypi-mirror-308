import logging
import time
from asyncio import Task
from dataclasses import dataclass
from typing import Any, Optional

import httpx
from rich.console import Console
from rich.syntax import Syntax

from .exceptions import ExecutionError, ExecutionSubmissionError
from .utils import create_token_header, create_access_token_header

_PLATFORM_CORE_PUBLIC_API_HOST = "https://public.lattice.ensquared.co.uk/core"


@dataclass
class Execution:
    id: str
    name: Optional[str]
    is_new: bool
    rejoined: bool
    immediate: bool

    _trace_id: str
    _api_key: str
    _session_token: str
    _disconnect: bool = False
    _tasks: Optional[list[Task]] = None
    _result: Optional[Any] = None
    _console: Console = None

    @classmethod
    def create(
        cls,
        graph: dict,
        *,
        name: Optional[str] = None,
        overwrite: Optional[bool] = False,
        api_key: str,
    ):
        response = httpx.post(
            f"{_PLATFORM_CORE_PUBLIC_API_HOST}/create_execution",
            json={
                "control_graph": graph,
                "name": name,
                "overwrite": overwrite,
            },
            headers={"authorization": create_token_header(api_key)},
            timeout=20,
        )
        if not response.is_success:
            raise ExecutionSubmissionError(response.text)

        response_json = response.json()
        instance = cls(
            _api_key=api_key,
            _session_token=response_json["token"],
            # _trace_id=response_json["execution"]["trace_id"],
            _trace_id="test",
            _console=Console(),
            _result=response_json["result"],
            id=response_json["id"],
            name=response_json["name"],
            is_new=response_json["is_new"],
            rejoined=response_json["rejoined"],
            immediate=response_json["result"] is not None,
        )

        return instance

    def get_result(self):
        return self._result

    def submit(self):
        response = httpx.post(
            f"{_PLATFORM_CORE_PUBLIC_API_HOST}/submit_execution",
            json={"id": self.id},
            headers={"authorization": create_access_token_header(self._session_token)},
            timeout=20,
        )
        if not response.is_success:
            raise ExecutionSubmissionError(response.text)
        return self

    def poll_for_completion(self):
        timeout = 3600
        step = 1
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self._poll_for_completion():
                return self._result
            time.sleep(step)

        raise TimeoutError("Timed out while polling for completion")

    def _poll_for_completion(self):
        response = httpx.post(
            f"{_PLATFORM_CORE_PUBLIC_API_HOST}/get_execution",
            json={"id": self.id},
            headers={"authorization": create_access_token_header(self._session_token)},
            timeout=10,
        )
        if not response.is_success:
            raise ExecutionError(response.text)

        response_json = response.json()
        status = response_json["execution"]["status"]

        if status == "SUBMITTED":
            return False

        if status == "FAILED":
            self._result = response_json["execution"]["result"]
            self._console.print(Syntax(self._result[0]["traceback"], "python"))
            return True

        if status == "SUCCEEDED":
            self._result = response_json["execution"]["result"]
            return True

        logging.warning(f"Unexpected status: {status}")
