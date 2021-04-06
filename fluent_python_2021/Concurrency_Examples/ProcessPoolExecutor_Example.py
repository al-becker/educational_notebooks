import sys
import math
from concurrent import futures
from time import perf_counter
from typing import NamedTuple


def is_prime(n: int = 5000111000222021) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    root = math.isqrt(n)
    for i in range(3, root + 1, 2):
        if n % i == 0:
            return False
    return True


NUMBERS = (
    2,
    3333333333333333,
    4444444444444444,
    5555555555555555,
    6666666666666666,
    142702110479723,
    7777777777777777,
    299593572317531,
    9999999999999999,
    3333333333333301,
    3333335652092209,
    4444444488888889,
    4444444444444423,
    5555553133149889,
    5555555555555503,
    6666666666666719,
    6666667141414921,
    7777777536340681,
    7777777777777753,
    9999999999999917
)


class PrimeResult(NamedTuple):
    n: int
    flag: bool
    elapsed: float


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def main() -> None:
    if len(sys.argv) < 2:
        workers = None
    else:
        workers = int(sys.argv[1])

    executor = futures.ProcessPoolExecutor(workers)
    # noinspection PyProtectedMember
    actual_workers = executor._max_workers

    print(f'Checking {len(NUMBERS)} numbers with {actual_workers} processes:')

    t0 = perf_counter()

    numbers = sorted(NUMBERS, reverse=True)
    with executor:
        for n, prime, elapsed in executor.map(check, numbers):
            label = 'P' if prime else ' '
            print(f'{n:16}  {label} {elapsed:9.6f}s')

    time = perf_counter() - t0
    print(f'Total time: {time:.2f}s')


if __name__ == '__main__':
    main()
