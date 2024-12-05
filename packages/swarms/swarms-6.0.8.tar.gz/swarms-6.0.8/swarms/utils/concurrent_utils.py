import concurrent.futures
from typing import List, Tuple, Any, Dict, Union, Callable


def execute_concurrently(
    callable_functions: List[
        Tuple[Callable, Tuple[Any, ...], Dict[str, Any]]
    ],
    max_workers: int = 5,
) -> List[Union[Any, Exception]]:
    """
    Executes callable functions concurrently using multithreading.

    Parameters:
    - callable_functions: A list of tuples, each containing the callable function and its arguments.
      For example: [(function1, (arg1, arg2), {'kwarg1': val1}), (function2, (), {})]
    - max_workers: The maximum number of threads to use.

    Returns:
    - results: A list of results returned by the callable functions. If an error occurs in any function,
      the exception object will be placed at the corresponding index in the list.
    """
    results = [None] * len(callable_functions)

    def worker(
        fn: Callable,
        args: Tuple[Any, ...],
        kwargs: Dict[str, Any],
        index: int,
    ) -> None:
        try:
            result = fn(*args, **kwargs)
            results[index] = result
        except Exception as e:
            results[index] = e

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:
        futures = []
        for i, (fn, args, kwargs) in enumerate(callable_functions):
            futures.append(
                executor.submit(worker, fn, args, kwargs, i)
            )

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

    return results
