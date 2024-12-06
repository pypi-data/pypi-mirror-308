import functools
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, Callable, Any
import time
import cloudpickle
import multiprocessing as mp
from .tracker import ExperimentTracker

def _run_single_experiment(serialized_func, experiment_name, run_index, times, args, kwargs):
    """在进程中执行的顶层函数"""
    # 反序列化函数
    func = cloudpickle.loads(serialized_func)
    # 创建追踪器
    tracker = ExperimentTracker(experiment_name)
    tracker.log_params({
        "run_index": run_index,
        "total_runs": times,
        "parallel": True,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    # 执行函数
    return func(tracker, *args, **kwargs)

def repeat_experiment(
    times: int = 1,
    experiment_name: Optional[str] = None,
    parallel: bool = False,
    max_workers: Optional[int] = None
):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal experiment_name
            if experiment_name is None:
                experiment_name = func.__name__

            results = []
            
            if parallel:
                # 序列化函数
                serialized_func = cloudpickle.dumps(func)
                
                # 使用 spawn 方法创建进程
                ctx = mp.get_context('spawn')
                with ProcessPoolExecutor(
                    max_workers=max_workers,
                    mp_context=ctx
                ) as executor:
                    futures = []
                    for i in range(times):
                        future = executor.submit(
                            _run_single_experiment,
                            serialized_func,
                            experiment_name,
                            i,
                            times,
                            args,
                            kwargs
                        )
                        futures.append(future)
                    
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            results.append(result)
                        except Exception as e:
                            print(f"Run failed with error: {e}")
            else:
                # 串行执行保持不变
                for i in range(times):
                    tracker = ExperimentTracker(experiment_name)
                    tracker.log_params({
                        "run_index": i,
                        "total_runs": times,
                        "parallel": False,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    try:
                        result = func(tracker, *args, **kwargs)
                        results.append(result)
                    except Exception as e:
                        print(f"Run {i} failed with error: {e}")
            
            return results
        return wrapper
    return decorator