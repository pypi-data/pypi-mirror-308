from multiprocessing.pool import AsyncResult, Pool
from typing import Any, Callable, Iterable, Mapping, Optional, TypeVar

from .graph import Vector

_S = TypeVar("_S")
_T = TypeVar("_T")


class RemotePool(Pool):
    def __init__(self, api_key: str, *args, **kwargs):
        self.api_key = api_key
        super().__init__(*args, **kwargs)

    def apply(
        self,
        func: Callable[..., _T],
        args: Iterable[Any] = ...,
        kwds: Mapping[str, Any] = ...,
    ) -> _T:
        return Vector(args).apply(func).evaluate(api_key=self.api_key)

    def apply_async(
        self,
        func: Callable[..., _T],
        args: Iterable[Any] = ...,
        kwds: Mapping[str, Any] = ...,
        callback: Callable[[_T], object] | None = ...,
        error_callback: Callable[[BaseException], object] | None = ...,
    ) -> AsyncResult[_T]:
        return (
            Vector(args)
            .apply(func)
            .evaluate(
                api_key=self.api_key,
                is_async=True,
                callback=callback,
            )
        )

    def map(
        self,
        func: Callable[[_S], _T],
        iterable: Iterable[_S],
        chunksize: Optional[int] = None,
    ) -> list[_T]:
        return Vector(iterable).map(func).evaluate(api_key=self.api_key)

    def starmap(
        self,
        func: Callable[..., _T],
        iterable: Iterable[Iterable[Any]],
        chunksize: Optional[int] = None,
    ) -> list[_T]:
        return Vector(iterable).starmap(func).evaluate(api_key=self.api_key)

    def join(self):
        ...


def remote_pool(api_key: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
