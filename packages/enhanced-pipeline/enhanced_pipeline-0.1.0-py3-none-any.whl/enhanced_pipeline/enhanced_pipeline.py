import logging
import inspect
import multiprocessing as mp
from dataclasses import dataclass
from typing import Callable, List, Any, Optional, Dict
from contextlib import contextmanager
import time
import random

logger = logging.getLogger(__name__)


@dataclass
class Stage:
    """Represents a single stage in the pipeline.

    Attributes:
        num_workers (int): Number of parallel workers for this stage
        func (Callable): Function to be executed by workers
        input_queue (mp.Queue): Input queue for this stage (can be a list too)
        output_queue (mp.Queue): Output queue for this stage (can be a list too)
        extras (Optional[List[Any]]): Extra arguments passed to each worker at that stage
        global_variable (Optional[Any]): Global variable shared across workers
    """
    num_workers: int
    func: Callable
    input_queue: mp.Queue
    output_queue: mp.Queue
    extras: Optional[List[Any]] = None
    global_variable: Optional[Any] = None


class EnhancedPipeline:
    def __init__(self, stages: List[Dict], items_to_process: List[Any], error_func: Optional[Callable] = None):
        self.stages = [Stage(**stage) for stage in stages]
        self.items_to_process = items_to_process
        self.error_queue = mp.Queue()
        self.processes = []
        self._validate_stages()
        self.error_func = error_func or self.default_error_func

    def _validate_stages(self):
        """Validate stage configurations and functions."""
        for i, stage in enumerate(self.stages):
            if stage.func is None:
                stage.func = self.default_stage_func
            else:
                sig = inspect.signature(stage.func)
                if len(sig.parameters) < 4:
                    raise ValueError(
                        f"Stage {i} function must accept at least 4 parameters: "
                        "input_queue, output_queue, stage_index, error_queue"
                    )

    @contextmanager
    def _manage_processes(self):
        """Context manager for process lifecycle management."""
        try:
            yield
        finally:
            for p in self.processes:
                if p.is_alive():
                    p.terminate()
            for p in self.processes:
                p.join()

    def _create_stage_processes(self, stage: Stage, stage_index: int) -> List[mp.Process]:
        """Create processes for a single stage."""
        if stage.extras:
            if len(stage.extras) != stage.num_workers:
                raise ValueError(f"Stage {stage_index}: extras must match num_workers")
            return [
                mp.Process(
                    target=stage.func,
                    args=(stage.input_queue, stage.output_queue, stage_index,
                          self.error_queue, extra),
                    name=f"Stage{stage_index + 1}_Worker{i + 1}"
                )
                for i, extra in enumerate(stage.extras)
            ]
        elif stage.global_variable is not None:
            return [
                mp.Process(
                    target=stage.func,
                    args=(stage.input_queue, stage.output_queue, stage_index,
                          self.error_queue, stage.global_variable),
                    name=f"Stage{stage_index + 1}_Worker{i + 1}"
                )
                for i in range(stage.num_workers)
            ]
        else:
            return [
                mp.Process(
                    target=stage.func,
                    args=(stage.input_queue, stage.output_queue, stage_index,
                          self.error_queue),
                    name=f"Stage{stage_index + 1}_Worker{i + 1}"
                )
                for i in range(stage.num_workers)
            ]

    @staticmethod
    def default_stage_func(input_queue, output_queue, stage_index, error_queue):
        while True:
            _item = input_queue.get()
            try:
                if _item is None:
                    output_queue.put(None)
                    break
                print(f'Stage {stage_index + 1} {mp.current_process().name}: {_item}')
                time.sleep(random.uniform(0.5, 1.5))
                output_queue.put(_item)
            except Exception as e:
                error_queue.put((_item, str(e)))

    @staticmethod
    def default_error_func(error_queue):
        while True:
            try:
                error_item = error_queue.get()
                if error_item is None:
                    break
                item, error = error_item
                logging.error(f'Error in {mp.current_process().name}: {item} - {error}')
            except Exception as e:
                logging.error(f'Error handler failed: {str(e)}')

    def run(self):
        """Execute the pipeline with proper process management."""
        with self._manage_processes():
            # Create and start all stage processes
            for stage_index, stage in enumerate(self.stages):
                stage_processes = self._create_stage_processes(stage, stage_index)
                self.processes.extend(stage_processes)
                for p in stage_processes:
                    p.start()

            # Start error handler
            error_handler = mp.Process(
                target=self.error_func,
                args=(self.error_queue,),
                name="ErrorHandler"
            )
            error_handler.start()
            self.processes.append(error_handler)

            # Feed initial items
            for item in self.items_to_process:
                self.stages[0].input_queue.put(item)

            # Send termination signals
            for _ in range(self.stages[0].num_workers):
                self.stages[0].input_queue.put(None)

            # Wait for completion
            for p in self.processes[:-1]:  # All except error handler
                p.join()

            # Terminate error handler
            self.error_queue.put(None)
            error_handler.join()
