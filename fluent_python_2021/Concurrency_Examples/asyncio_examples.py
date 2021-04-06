import asyncio

import asyncio
import itertools


async def spin_va(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')


async def slow_va() -> int:
    await asyncio.sleep(3)
    return 42


async def supervisor_va() -> int:
    spinner = asyncio.create_task(spin_va('thinking!'))
    print(f'spinner object: {spinner}')
    result = await slow_va()
    spinner.cancel()
    return result


def main_va() -> None:
    result = asyncio.run(supervisor_va())
    print(f'Answer: {result}')


main_va()
