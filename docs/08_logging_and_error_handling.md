# Logging and Error Handling

## 1. Purpose

Logging and error handling make the ETL pipeline observable and controllable.

The pipeline processes multiple datasets and executes several independent scripts. Without logging, a failure could require manually identifying which stage failed and why.

The implementation therefore records:

- Pipeline start
- Pipeline completion
- Current ETL step
- Step completion
- Step execution time
- Error output
- Failed step
- Total execution time

The main components are:

```text
src/logging_config.py
src/run_pipeline.py
```

Runtime logs are written to:

```text
logs/pipeline.log
```

---

## 2. Why Logging Was Added

The pipeline contains multiple stages:

```text
Extraction
    ↓
Source Validation
    ↓
Transformation
    ↓
Transformation Validation
    ↓
Loading
    ↓
Database Validation
```

If one stage fails, simply printing:

```text
Pipeline failed
```

does not provide enough information.

The logging implementation instead identifies:

```text
Which step?
When did it start?
How long did it run?
Did it complete?
What error occurred?
Did the pipeline stop?
```

This makes the pipeline easier to debug and monitor.

---

## 3. Logging Configuration

File:

```text
src/logging_config.py
```

The module creates the project's logging configuration.

It determines the project root using:

```python
project_root = Path(__file__).resolve().parents[1]
```

This allows the log location to be based on the project directory rather than the current terminal location.

---

## 4. Log Directory

The logging configuration creates:

```text
logs/
```

if it does not already exist.

The log file is:

```text
logs/pipeline.log
```

The directory is created with:

```python
log_folder.mkdir(exist_ok=True)
```

This means the pipeline does not require the developer to manually create the log directory before execution.

---

## 5. Logger

The project uses a named logger:

```python
logging.getLogger("etl_pipeline")
```

The logging level is:

```text
INFO
```

This captures normal pipeline progress as well as warnings and errors.

---

## 6. Log Format

The formatter is:

```text
%(asctime)s | %(levelname)s | %(message)s
```

Example:

```text
2026-08-24 12:56:12,550 | INFO | Pipeline started
```

The three important parts are:

```text
Timestamp
   |
   +-- Log level
   |
   +-- Message
```

This makes the log easy to read during debugging.

---

## 7. Console and File Logging

Two handlers are configured.

### File Handler

```python
logging.FileHandler(
    log_file,
    encoding="utf-8"
)
```

This writes logs to:

```text
logs/pipeline.log
```

### Console Handler

```python
logging.StreamHandler()
```

This displays the same log messages in the terminal.

Therefore:

```text
                    Logger
                   /      \
                  /        \
                 ↓          ↓
            Terminal      Log File
```

The developer can see progress immediately while also retaining a persistent execution record.

---

## 8. Preventing Duplicate Handlers

The configuration checks:

```python
if logger.handlers:
    return logger
```

This prevents the same handlers from being attached multiple times if `setup_logger()` is called again within the same process.

Without this protection, one log message could be written multiple times.

---

## 9. Pipeline Orchestration

The main orchestration file is:

```text
src/run_pipeline.py
```

It maintains the ordered list of pipeline steps.

Each script is executed as a separate Python process.

---

## 10. Step-Level Logging

Before each step starts:

```python
logger.info(f"Running: {step}")
```

Example:

```text
INFO | Running: src/transformation/transform_orders.py
```

After successful completion:

```text
INFO | Completed: src/transformation/transform_orders.py in 3.96 seconds
```

This gives visibility into both progress and performance.

---

## 11. Execution Timing

The orchestrator records the start time before each step:

```python
step_start = time.time()
```

After execution:

```python
step_time = time.time() - step_start
```

The duration is logged:

```text
Completed: src/transformation/transform_orders.py in 3.96 seconds
```

The entire pipeline is also timed.

Example:

```text
Pipeline completed successfully in 69.48 seconds
```

---

## 12. Why Execution Time Is Logged

Execution timing provides useful operational information.

It helps identify:

- Slow transformation steps
- Expensive database loads
- Large-data bottlenecks
- Performance changes between runs

For example, the geolocation transformation processes a large dataset and therefore takes longer than the small category translation transformation.

Timing makes this visible without requiring manual measurement.

---

## 13. Capturing Subprocess Output

The orchestrator runs each script using:

```python
subprocess.run(
    ...,
    capture_output=True,
    text=True
)
```

This allows the orchestrator to capture:

```text
stdout
stderr
```

Normal output is still displayed in the terminal.

Error output can therefore be captured and recorded when a step fails.

---

## 14. Error Detection

Every subprocess returns an exit code.

The orchestrator checks:

```python
if result.returncode != 0:
```

A non-zero exit code indicates that the step failed.

The pipeline then logs the error rather than continuing to later stages.

---

## 15. Error Logging

When an error occurs, the actual stderr output is recorded.

Conceptually:

```python
logger.error(
    f"Error output from {step}:\n"
    f"{result.stderr.strip()}"
)
```

This preserves the traceback or error message generated by the failed script.

An actual development failure occurred while writing the processed orders file, producing:

```text
OSError: [Errno 22] Invalid argument
```

The error was associated with:

```text
src/transformation/transform_orders.py
```

---

## 16. Failed-Step Logging

After recording the actual error, the orchestrator records:

```text
Pipeline failed at: <step> after <time> seconds
```

This provides a concise failure summary.

The resulting structure is:

```text
Running step
     ↓
Step fails
     ↓
Capture stderr
     ↓
Log traceback/error
     ↓
Log failed step + duration
     ↓
Stop pipeline
```

---

## 17. Why the Pipeline Stops

The pipeline executes dependent stages.

For example:

```text
Transformation
      ↓
Transformation Validation
      ↓
Loading
```

If transformation fails, loading should not continue because the data may be incomplete or invalid.

Therefore, after logging the failure, the orchestrator exits using the subprocess return code.

This prevents a later stage from operating on an invalid intermediate state.

---

## 18. Controlled Failure Testing

Error handling was tested rather than assumed to work.

A temporary controlled failure was introduced using:

```text
src/test_failure.py
```

The purpose was to verify that the orchestrator actually:

```text
Detects the failure
      ↓
Captures the error
      ↓
Logs the traceback
      ↓
Identifies the failed step
      ↓
Stops the pipeline
```

After testing, the temporary failure was removed.

The normal pipeline was then executed again successfully.

---

## 19. Example Successful Logging

A successful pipeline run produces messages similar to:

```text
INFO | Pipeline started
INFO | Running: src/extraction/extract_data.py
INFO | Completed: src/extraction/extract_data.py in 13.28 seconds

INFO | Running: src/transformation/transform_orders.py
INFO | Completed: src/transformation/transform_orders.py in 3.96 seconds

INFO | Running: src/loading/load_data.py
INFO | Completed: src/loading/load_data.py in 23.70 seconds

INFO | Running: src/loading/validate_database.py
INFO | Completed: src/loading/validate_database.py in 2.72 seconds

INFO | Pipeline completed successfully in 69.48 seconds
```

This provides a readable execution trail.

---

## 20. Example Failure Logging

A failed stage produces a structure similar to:

```text
INFO | Running: src/transformation/transform_orders.py

ERROR | Error output from src/transformation/transform_orders.py:
Traceback ...
OSError: [Errno 22] Invalid argument ...

ERROR | Pipeline failed at:
src/transformation/transform_orders.py
after 2.10 seconds
```

This makes the failure location immediately visible.

---

## 21. Logging vs Printing

The project does not completely eliminate `print()` statements from individual transformation scripts.

There is a distinction between:

### Script Output

Examples:

```text
Customers transformed: 99441 rows
Saved to: ...
```

This communicates dataset-specific processing information.

### Pipeline Logging

Examples:

```text
Pipeline started
Running: ...
Completed: ... in 3.96 seconds
Pipeline failed at: ...
```

This communicates orchestration and operational status.

The two serve different purposes.

---

## 22. Why Rotating File Handler Was Not Required

A rotating file handler was considered during the logging design.

A rotating handler is useful when:

```text
Applications run continuously
+
Logs grow indefinitely
+
Old logs need automatic rotation
```

This project uses a static historical dataset and is designed as a batch ETL demonstration.

The pipeline is not intended to run continuously against a changing production source.

Therefore, a simple:

```python
logging.FileHandler
```

is sufficient for the current project scope.

Adding rotation would introduce infrastructure that does not solve a current project requirement.

---

## 23. Why the Pipeline Does Not Need to Run Daily

The Olist dataset is a static historical snapshot.

Therefore, repeatedly running the pipeline does not represent daily production ingestion.

Instead, rerunning the pipeline demonstrates:

```text
Reproducibility
Repeatability
Failure recovery
Data validation
Database reconstruction
```

The full-refresh strategy means the same dataset can be rebuilt consistently.

A real production system could later replace the source with:

```text
API
Database source
Cloud storage
New daily files
CDC stream
```

At that point, incremental processing and scheduling could become appropriate.

They are outside the current project scope.

---

## 24. Error Handling Strategy

The current error-handling strategy is intentionally simple and appropriate for the project.

```text
Execute step
    ↓
Check exit code
    ↓
Success?
 /       \
Yes       No
 |         |
Log       Log error
success   + traceback
 |         |
Next      Stop
step
```

This prevents silent failures and prevents downstream stages from running after a failed dependency.

---

## 25. Logging Architecture

The logging architecture can be summarized as:

```text
                   run_pipeline.py
                         │
                         ↓
                  setup_logger()
                         │
                ┌────────┴────────┐
                ↓                 ↓
          Console Handler    File Handler
                │                 │
                ↓                 ↓
            Terminal       logs/pipeline.log
```

The orchestrator is therefore the central point for pipeline-level logging.

---

## 26. Current Implementation

The current implementation contains:

```text
src/
├── logging_config.py
├── run_pipeline.py
└── test_failure.py
```

The runtime logs are stored under:

```text
logs/
└── pipeline.log
```

The runtime logs are not intended to be committed to the repository.

---

## 27. Final Verification

After implementing logging and error handling, the complete pipeline was executed successfully.

The final run demonstrated:

```text
Pipeline started
        ↓
All extraction steps completed
        ↓
All transformations completed
        ↓
Transformation validation completed
        ↓
Database loading completed
        ↓
Database validation completed
        ↓
Pipeline completed successfully
```

The latest successful execution completed in:

```text
69.48 seconds
```

with all configured database key and foreign-key validation checks passing.

---

## 28. Summary

The logging and error-handling layer provides the pipeline with basic operational observability.

It supports:

```text
Execution tracking
+
Step timing
+
Persistent logs
+
Console visibility
+
Error capture
+
Failure identification
+
Pipeline stopping
+
Controlled failure testing
```

The implementation is intentionally proportional to the project.

It demonstrates production-relevant concepts without introducing unnecessary infrastructure such as schedulers, streaming systems, or rotating log management that are not required for this static batch ETL project.
