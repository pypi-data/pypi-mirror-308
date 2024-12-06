from __future__ import annotations

from asyncio import sleep
from typing import TYPE_CHECKING, Any

from hypothesis import given
from pytest import mark, param, raises

from utilities.asyncio import (
    _MaybeAwaitableMaybeAsyncIterable,
    is_awaitable,
    timeout_dur,
    to_list,
    try_await,
)
from utilities.hypothesis import durations

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterable, Iterator

    from utilities.types import Duration

_STRS = list("AAAABBBCCDAABB")


def _get_strs_sync() -> Iterable[str]:
    return iter(_STRS)


async def _get_strs_async() -> Iterable[str]:
    return _get_strs_sync()


def _yield_strs_sync() -> Iterator[str]:
    return iter(_get_strs_sync())


async def _yield_strs_async() -> AsyncIterator[str]:
    for i in _get_strs_sync():
        yield i
        await sleep(0.01)


class TestIsAwaitable:
    @mark.parametrize(
        ("obj", "expected"), [param(sleep(0.01), True), param(None, False)]
    )
    async def test_main(self, *, obj: Any, expected: bool) -> None:
        result = await is_awaitable(obj)
        assert result is expected


class TestTimeoutDur:
    @given(duration=durations())
    async def test_main(self, *, duration: Duration) -> None:
        async with timeout_dur(duration=duration):
            pass


class TestToList:
    @mark.parametrize(
        "iterable",
        [
            param(_get_strs_sync()),
            param(_get_strs_async()),
            param(_yield_strs_sync()),
            param(_yield_strs_async()),
        ],
    )
    async def test_main(
        self, *, iterable: _MaybeAwaitableMaybeAsyncIterable[str]
    ) -> None:
        result = await to_list(iterable)
        assert result == _STRS


class TestTryAwait:
    async def test_sync(self) -> None:
        def func(*, value: bool) -> bool:
            return not value

        result = await try_await(func(value=True))
        assert result is False

    async def test_async(self) -> None:
        async def func(*, value: bool) -> bool:
            await sleep(0.01)
            return not value

        result = await try_await(func(value=True))
        assert result is False

    @mark.parametrize("cls", [param(ValueError), param(TypeError)], ids=str)
    async def test_error_std_msg_sync(self, *, cls: type[Exception]) -> None:
        def func(*, value: bool) -> bool:
            if not value:
                msg = f"Value must be True; got {value}"
                raise cls(msg)
            return not value

        with raises(cls, match="Value must be True; got False"):
            _ = await try_await(func(value=False))

    @mark.parametrize("cls", [param(ValueError), param(TypeError)], ids=str)
    async def test_error_std_msg_async(self, *, cls: type[Exception]) -> None:
        async def func(*, value: bool) -> bool:
            if not value:
                msg = f"Value must be True; got {value}"
                raise cls(msg)
            await sleep(0.01)
            return not value

        with raises(cls, match="Value must be True; got False"):
            _ = await try_await(func(value=False))

    @mark.parametrize("cls", [param(ValueError), param(TypeError)], ids=str)
    async def test_error_non_std_msg_sync(self, *, cls: type[Exception]) -> None:
        def func(*, value: bool) -> bool:
            if not value:
                raise cls(value)
            return not value

        with raises(cls, match="False"):
            _ = await try_await(func(value=False))

    @mark.parametrize("cls", [param(ValueError), param(TypeError)], ids=str)
    async def test_error_non_std_msg_async(self, *, cls: type[Exception]) -> None:
        async def func(*, value: bool) -> bool:
            if not value:
                raise cls(value)
            await sleep(0.01)
            return not value

        with raises(cls, match="False"):
            _ = await try_await(func(value=False))
