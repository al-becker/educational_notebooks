import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count
from multiprocessing import queues
import math

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
    prime: bool
    elapsed: float


JobQueue = queues.SimpleQueue[int]
ResultQueue = queues.SimpleQueue[PrimeResult]


def check(n: int) -> PrimeResult:
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)


def worker(jobs: JobQueue, results: ResultQueue) -> None:
    while n := jobs.get():
        results.put(check(n))


def main(n_worker: int = 0) -> None:
    if n_worker:
        workers = n_worker
    else:
        workers = cpu_count()

    print(f'Checking {len(NUMBERS)} numbers with {workers} processes:')

    jobs: JobQueue = SimpleQueue()
    results: ResultQueue = SimpleQueue()
    t0 = perf_counter()

    for n in NUMBERS:
        jobs.put(n)

    for _ in range(workers):
        proc = Process(target=worker, args=(jobs, results))
        proc.start()
        jobs.put(0)

    print(jobs)
    while True:
        n, prime, elapsed = results.get()
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')
        if jobs.empty():
            break

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')



if __name__ == '__main__':
    main()