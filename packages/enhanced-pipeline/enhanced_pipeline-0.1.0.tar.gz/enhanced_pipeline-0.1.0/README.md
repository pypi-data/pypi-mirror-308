# EnhancedPipeline

A robust and flexible parallel processing pipeline implementation for Python that enables the creation of multi-stage data processing workflows with configurable worker processes.

## Installation

```bash
pip install enhanced-pipeline
```

## Quick Start

```python
from enhanced_pipeline import EnhancedPipeline
import multiprocessing as mp
from enhanced_pipeline import EnhancedPipeline
import multiprocessing as mp

# Define stage functions
def stage1_func(input_queue, output_queue, stage_index, error_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        output_queue.put(item * 2)

def stage2_func(input_queue, output_queue, stage_index, error_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        output_queue.put(item + 10)

def stage3_func(input_queue, output_queue, stage_index, error_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        print(item)

if __name__ == "__main__":
    # Create queues
    q1, q2, q3 = mp.Queue(), mp.Queue(), mp.Queue()

    # Configure pipeline stages
    stages = [
        {'num_workers': 2, 'func': stage1_func, 'input_queue': q1, 'output_queue': q2},
        {'num_workers': 2, 'func': stage2_func, 'input_queue': q2, 'output_queue': q3},
        {'num_workers': 2, 'func': stage3_func, 'input_queue': q3, 'output_queue': None},
    ]

    # Create and run pipeline
    pipeline = EnhancedPipeline(stages=stages, items_to_process=[1, 2, 3, 4, 5])
    pipeline.run()
```

## Key Features

- Multiple processing stages with configurable number of workers
- Built-in error handling and monitoring
- Support for stage-specific extra parameters
- Automatic process lifecycle management
- Type-safe implementation with runtime validation

## Detailed Usage

### 1. Basic Pipeline Configuration

The pipeline requires two main components:
- A list of stage configurations
- Items to process

```python
from enhanced_pipeline import EnhancedPipeline
import multiprocessing as mp

# Create queues for each stage
input_queue = mp.Queue()
middle_queue = mp.Queue()
output_queue = mp.Queue()

# Define stages
stages = [
    {
        'num_workers': 3,
        'func': my_stage_func,
        'input_queue': input_queue,
        'output_queue': middle_queue
    },
    {
        'num_workers': 2,
        'func': another_stage_func,
        'input_queue': middle_queue,
        'output_queue': output_queue
    }
]

# Initialize pipeline
pipeline = EnhancedPipeline(
    stages=stages,
    items_to_process=[1, 2, 3, 4, 5]
)

# Run pipeline
pipeline.run()
```

### 2. Custom Stage Functions

Stage functions must accept at least four parameters:
- input_queue: Queue for receiving items
- output_queue: Queue for sending processed items
- stage_index: Integer indicating stage position
- error_queue: Queue for error reporting

```python
def custom_stage_function(input_queue, output_queue, stage_index, error_queue):
    while True:
        try:
            # Get item from input queue
            item = input_queue.get()
            
            # Check for termination signal
            if item is None:
                break
                
            # Process item
            result = process_item(item)
            
            # Send to next stage
            output_queue.put(result)
            
        except Exception as e:
            # Report error
            error_queue.put((item, str(e)))
```

### 3. Using Extra Parameters

You can pass stage-specific parameters to workers such as different DB connections for each workers so that db access won't get conflicted:

```python
def stage_with_extras(input_queue, output_queue, stage_index, error_queue, extra_param):
    while True:
        item = input_queue.get()
        if item is None:
            break
        # Use extra_param in processing
        result = process_with_param(item, extra_param)
        output_queue.put(result)

# Configure stage with extras
stages = [
    {
        'num_workers': 2,
        'func': stage_with_extras,
        'input_queue': q1,
        'output_queue': q2,
        'extras': ['param1', 'param2']  # One for each worker
    }
]
```

### 4. Global Variables

Share common data across all workers in a stage:


```python
manager = mp.Manager()

# Create thread-safe shared states
shared_config = manager.dict({
    'validation_rules': ['price_check', 'items_check'],
    'min_order_amount': 10.0,
    'stats': manager.Value('i', 0)  # Counter for validated orders
})


def stage_with_global(input_queue, output_queue, stage_index, error_queue, global_data):
    while True:
        item = input_queue.get()
        if item is None:
            break
        # Use global_data in processing
        result = process_with_global(item, global_data)
        output_queue.put(result)

# Configure stage with global variable
stages = [
    {
        'num_workers': 2,
        'func': stage_with_global,
        'input_queue': q1,
        'output_queue': q2,
        'global_variable': shared_config
    }
]
```

### 5. Custom Error Handling

Implement custom error handling:

```python
def custom_error_handler(error_queue):
    while True:
        try:
            error_item = error_queue.get()
            if error_item is None:
                break
            
            item, error = error_item
            # Custom error handling logic
            log_error(item, error)
            alert_admin(item, error)
            
        except Exception as e:
            logging.critical(f"Error handler failed: {str(e)}")

# Use custom error handler
pipeline = EnhancedPipeline(
    stages=stages,
    items_to_process=items,
    error_func=custom_error_handler
)
```

### 6. Real-World Example: Image Processing Pipeline

```python



```

## API Reference

### EnhancedPipeline

```python
class EnhancedPipeline:
    def __init__(self, 
                 stages: List[Dict], 
                 items_to_process: List[Any], 
                 error_func: Optional[Callable] = None):
        """
        Initialize pipeline with stages and items to process.
        
        Args:
            stages: List of stage configurations
            items_to_process: Items to be processed by the pipeline
            error_func: Optional custom error handling function
        """
        
    def run(self):
        """
        Execute the pipeline with all configured stages.
        Manages process lifecycle and handles cleanup.
        """
```

### Stage Configuration

Each stage in the pipeline is configured with a dictionary containing:

| Parameter | Type | Required | Description                                        |
|-----------|------|----------|----------------------------------------------------|
| num_workers | int | Yes | Number of worker processes                         |
| func | Callable | Yes | Processing function                                |
| input_queue | Queue | Yes | Input queue for this stage (also a can be a list)  |
| output_queue | Queue | Yes | Output queue for this stage (also a can be a list) |
| extras | List[Any] | No | Extra parameters for each worker                   |
| global_variable | Any | No | Shared data for all workers                        |

## Best Practices

1. **Error Handling**: Always implement proper error handling in stage functions:
```python
try:
    # Process item
    result = process_item(item)
except Exception as e:
    error_queue.put((item, str(e)))
    return
```

2. **Resource Management**: Close resources properly in stage functions:
```python
def stage_func(input_queue, output_queue, stage_index, error_queue):
    resource = acquire_resource()
    try:
        while True:
            item = input_queue.get()
            if item is None:
                break
            # Process with resource
    finally:
        release_resource(resource)
```

3. **Queue Management**: Monitor queue sizes to prevent memory issues:
```python
def stage_func(input_queue, output_queue, stage_index, error_queue):
    while True:
        # Add timeout to prevent deadlocks
        try:
            item = input_queue.get(timeout=60)
        except Empty:
            continue
```

## Limitations

- No built-in support for distributed processing across machines
- Queue size limited by available system memory
- All stages must run in the same Python process space

## Contributing

Contributions are welcome!  submit pull requests to git repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.