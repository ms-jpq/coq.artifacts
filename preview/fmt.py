#!/usr/bin/env python3

from asyncio import create_subprocess_exec, run
from asyncio.tasks import gather
from contextlib import suppress
from pathlib import Path
from subprocess import DEVNULL, CalledProcessError

_TOP_LV = Path(__file__).resolve().parent


async def _conv(path: Path) -> None:
    name = path.with_suffix(".gif")
    name.unlink(missing_ok=True)

    args = (
        "ffmpeg",
        "-i",
        path,
        "-filter:v",
        "fps=50,scale=1000:-1",
        name,
    )
    proc = await create_subprocess_exec(
        *args,
        cwd=_TOP_LV,
        stdin=DEVNULL,
    )

    try:
        code = await proc.wait()
        if code:
            raise CalledProcessError(returncode=code, cmd=args)
    finally:
        with suppress(ProcessLookupError):
            proc.kill()
        await proc.wait()

    pass


async def main() -> None:
    movs = _TOP_LV.glob("*.mov")
    await gather(*map(_conv, movs))


run(main())
