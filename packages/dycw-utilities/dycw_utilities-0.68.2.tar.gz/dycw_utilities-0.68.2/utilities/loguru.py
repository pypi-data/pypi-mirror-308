from __future__ import annotations

import asyncio
import logging
import sys
import time
from asyncio import AbstractEventLoop
from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass
from enum import StrEnum, unique
from logging import Handler, LogRecord
from sys import __excepthook__, _getframe, stderr
from typing import TYPE_CHECKING, Any, Literal, TextIO, TypedDict, assert_never, cast

from loguru import logger
from typing_extensions import override

from utilities.datetime import duration_to_timedelta
from utilities.iterables import (
    OneEmptyError,
    OneNonUniqueError,
    one,
    resolve_include_and_exclude,
)

if TYPE_CHECKING:
    import datetime as dt
    from multiprocessing.context import BaseContext
    from types import TracebackType

    from loguru import (
        CompressionFunction,
        FilterDict,
        FilterFunction,
        FormatFunction,
        LevelConfig,
        Message,
        Record,
        RetentionFunction,
        RotationFunction,
        Writable,
    )

    from utilities.asyncio import Coroutine1, MaybeCoroutine1
    from utilities.iterables import MaybeIterable
    from utilities.types import Duration, PathLike, StrMapping


_RECORD_EXCEPTION_VALUE = "{record[exception].value!r}"
LEVEL_CONFIGS: Sequence[LevelConfig] = [
    {"name": "TRACE", "color": "<blue><bold>"},
    {"name": "DEBUG", "color": "<cyan><bold>"},
    {"name": "INFO", "color": "<green><bold>"},
    {"name": "SUCCESS", "color": "<magenta><bold>"},
    {"name": "WARNING", "color": "<yellow><bold>"},
    {"name": "ERROR", "color": "<red><bold>"},
    {"name": "CRITICAL", "color": "<red><bold><blink>"},
]


class HandlerConfiguration(TypedDict, total=False):
    """A handler configuration."""

    sink: (
        TextIO
        | Writable
        | Callable[[Message], MaybeCoroutine1[None]]
        | Handler
        | PathLike
    )
    level: int | str
    format: str | FormatFunction
    filter: str | FilterFunction | FilterDict | None
    colorize: bool | None
    serialize: bool
    backtrace: bool
    diagnose: bool
    enqueue: bool
    context: str | BaseContext | None
    catch: bool
    loop: AbstractEventLoop
    rotation: str | int | dt.time | dt.timedelta | RotationFunction | None
    retention: str | int | dt.timedelta | RetentionFunction | None
    compression: str | CompressionFunction | None
    delay: bool
    watch: bool
    mode: str
    buffering: int
    encoding: str
    kwargs: StrMapping


class InterceptHandler(Handler):
    """Handler for intercepting standard logging messages.

    https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    @override
    def emit(self, record: LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        try:  # pragma: no cover
            level = logger.level(record.levelname).name
        except ValueError:  # pragma: no cover
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = _getframe(6), 6  # pragma: no cover
        while (  # pragma: no cover
            frame and frame.f_code.co_filename == logging.__file__
        ):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(  # pragma: no cover
            level, record.getMessage()
        )


@unique
class LogLevel(StrEnum):
    """An enumeration of the logging levels."""

    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def get_logging_level_name(level: int, /) -> str:
    """Get the logging level name."""
    core = logger._core  # noqa: SLF001 # pyright: ignore[reportAttributeAccessIssue]
    try:
        return one(k for k, v in core.levels.items() if v.no == level)
    except OneEmptyError:
        raise _GetLoggingLevelNameEmptyError(level=level) from None
    except OneNonUniqueError as error:
        error = cast(OneNonUniqueError[str], error)
        raise _GetLoggingLevelNameNonUniqueError(
            level=level, first=error.first, second=error.second
        ) from None


@dataclass(kw_only=True, slots=True)
class GetLoggingLevelNameError(Exception):
    level: int


@dataclass(kw_only=True, slots=True)
class _GetLoggingLevelNameEmptyError(GetLoggingLevelNameError):
    @override
    def __str__(self) -> str:
        return f"There is no level with severity {self.level}"


@dataclass(kw_only=True, slots=True)
class _GetLoggingLevelNameNonUniqueError(GetLoggingLevelNameError):
    first: str
    second: str

    @override
    def __str__(self) -> str:
        return f"There must be exactly one level with severity {self.level}; got {self.first!r}, {self.second!r} and perhaps more"


def get_logging_level_number(level: str, /) -> int:
    """Get the logging level number."""
    try:
        return logger.level(level).no
    except ValueError:
        raise GetLoggingLevelNumberError(level=level) from None


@dataclass(kw_only=True, slots=True)
class GetLoggingLevelNumberError(Exception):
    level: str

    @override
    def __str__(self) -> str:
        return f"Invalid logging level: {self.level!r}"


def logged_sleep_sync(
    duration: Duration, /, *, level: LogLevel = LogLevel.INFO, depth: int = 1
) -> None:
    """Log a sleep operation, synchronously."""
    timedelta = duration_to_timedelta(duration)
    logger.opt(depth=depth).log(
        level, "Sleeping for {timedelta}...", timedelta=timedelta
    )
    time.sleep(timedelta.total_seconds())


async def logged_sleep_async(
    duration: Duration, /, *, level: LogLevel = LogLevel.INFO, depth: int = 1
) -> None:
    """Log a sleep operation, asynchronously."""
    timedelta = duration_to_timedelta(duration)
    logger.opt(depth=depth).log(
        level, "Sleeping for {timedelta}...", timedelta=timedelta
    )
    await asyncio.sleep(timedelta.total_seconds())


def make_except_hook(
    **kwargs: Any,
) -> Callable[[type[BaseException], BaseException, TracebackType | None], None]:
    """Make an `excepthook` which uses `loguru`."""

    def except_hook(
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
        /,
    ) -> None:
        """Exception hook which uses `loguru`."""
        if issubclass(exc_type, KeyboardInterrupt):  # pragma: no cover
            __excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.bind(**kwargs).opt(  # pragma: no cover
            exception=exc_value, record=True
        ).error(_RECORD_EXCEPTION_VALUE)
        sys.exit(1)  # pragma: no cover

    return except_hook


def make_filter(
    *,
    level: LogLevel | None = None,
    min_level: LogLevel | None = None,
    max_level: LogLevel | None = None,
    name_include: MaybeIterable[str] | None = None,
    name_exclude: MaybeIterable[str] | None = None,
    extra_include_all: MaybeIterable[Hashable] | None = None,
    extra_include_any: MaybeIterable[Hashable] | None = None,
    extra_exclude_all: MaybeIterable[Hashable] | None = None,
    extra_exclude_any: MaybeIterable[Hashable] | None = None,
    final_filter: bool | Callable[[], bool] | None = None,
) -> FilterFunction:
    """Make a filter."""

    def filter_func(record: Record, /) -> bool:
        rec_level_no = record["level"].no
        if (level is not None) and (rec_level_no != get_logging_level_number(level)):
            return False
        if (min_level is not None) and (
            rec_level_no < get_logging_level_number(min_level)
        ):
            return False
        if (max_level is not None) and (
            rec_level_no > get_logging_level_number(max_level)
        ):
            return False
        name = record["name"]
        if name is not None:
            name_inc, name_exc = resolve_include_and_exclude(
                include=name_include, exclude=name_exclude
            )
            if (name_inc is not None) and not any(name.startswith(n) for n in name_inc):
                return False
            if (name_exc is not None) and any(name.startswith(n) for n in name_exc):
                return False
        rec_extra_keys = set(record["extra"])
        extra_inc_all, extra_exc_any = resolve_include_and_exclude(
            include=extra_include_all, exclude=extra_exclude_any
        )
        if (extra_inc_all is not None) and not extra_inc_all.issubset(rec_extra_keys):
            return False
        if (extra_exc_any is not None) and (len(rec_extra_keys & extra_exc_any) >= 1):
            return False
        extra_inc_any, extra_exc_all = resolve_include_and_exclude(
            include=extra_include_any, exclude=extra_exclude_all
        )
        if (extra_inc_any is not None) and (len(rec_extra_keys & extra_inc_any) == 0):
            return False
        if (extra_exc_all is not None) and extra_exc_all.issubset(rec_extra_keys):
            return False
        return (final_filter is None) or (
            (isinstance(final_filter, bool) and final_filter)
            or (isinstance(final_filter, Callable) and final_filter())
        )

    return filter_func


def make_formatter(
    mode: Literal["console", "file-color", "file-plain"],
    /,
    *,
    prefix: str | None = None,
    exception: bool = True,
) -> FormatFunction:
    """Make a formatter."""

    def format_record(record: Record, /) -> str:
        """Format a record."""
        time_part = "<level>{time:HH:mm:ss}</level>"
        match mode:
            case "console":
                datetime_part = f"{{time:YYYY-MM-DD}} {time_part}.{{time:SSS}}"
            case "file-color" | "file-plain":
                datetime_part = f"{{time:YYYY-MM-DD (ddd)}} {time_part}.{{time:SSS zz}}"
            case _ as never:  # pyright: ignore[reportUnnecessaryComparison]
                assert_never(never)
        parts1 = [datetime_part]
        if mode == "file-plain":
            parts1.append("<level>{level.name}</level>")
        if record["message"]:
            parts1.append("<level>{function}</level>: <level>{message}</level>")
        else:
            parts1.append("<level>{function}</level>")
        try:
            extra = record["extra"]
        except KeyError:
            pass
        else:
            extra_non_underscore = {
                k: v
                for k, v in extra.items()
                if not (isinstance(k, str) and k.startswith("_"))
            }
            if len(extra_non_underscore) >= 1:
                parts1.append("{extra}")
        parts1.append("({name}:{line})")
        parts2 = ["  ".join(parts1), "\n"]
        if prefix is not None:
            parts2.insert(0, prefix)
        if (record["exception"] is not None) and exception:
            parts2.extend(["{exception}", "\n"])
        return "".join(parts2)

    return format_record


def make_slack_sink(url: str, /) -> Callable[[Message], None]:
    """Make a `slack` sink."""
    from utilities.slack_sdk import SendSlackError, send_slack_sync

    def sink_sync(message: Message, /) -> None:
        try:
            send_slack_sync(message, url=url)
        except SendSlackError as error:
            _ = stderr.write(f"{error}\n")  # pragma: no cover

    return sink_sync


def make_slack_sink_async(url: str, /) -> Callable[[Message], Coroutine1[None]]:
    """Make an asynchronous `slack` sink."""
    from utilities.slack_sdk import SendSlackError, send_slack_async

    async def sink_async(message: Message, /) -> None:
        try:
            await send_slack_async(message, url=url)
        except SendSlackError as error:
            _ = stderr.write(f"{error}\n")  # pragma: no cover

    return sink_async


__all__ = [
    "LEVEL_CONFIGS",
    "GetLoggingLevelNameError",
    "GetLoggingLevelNumberError",
    "HandlerConfiguration",
    "InterceptHandler",
    "LogLevel",
    "get_logging_level_name",
    "get_logging_level_number",
    "logged_sleep_async",
    "logged_sleep_sync",
    "make_except_hook",
    "make_filter",
    "make_formatter",
    "make_slack_sink",
    "make_slack_sink_async",
]
