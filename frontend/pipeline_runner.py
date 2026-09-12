import subprocess
import sys
import time
from threading import Lock, Thread
from queue import Empty, Queue
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PIPELINE_LOCK = Lock()


def run_pipeline():

    start_time = time.time()

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "src" / "run_pipeline.py")
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    runtime = time.time() - start_time

    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "error": result.stderr,
        "runtime": runtime
    }


def run_pipeline_live():
    """Run the ETL process and yield progress snapshots until it exits."""
    start_time = time.time()

    if not PIPELINE_LOCK.acquire(blocking=False):
        yield {
            "running": False,
            "runtime": 0,
            "output": "Another ETL pipeline run is already in progress.",
            "returncode": 1,
        }
        return

    output_queue = Queue()
    try:
        process = subprocess.Popen(
            [sys.executable, str(PROJECT_ROOT / "src" / "run_pipeline.py")],
            cwd=PROJECT_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            text=True,
        )

        def collect_output():
            for line in process.stdout:
                output_queue.put(line)
            process.stdout.close()

        output_thread = Thread(target=collect_output, daemon=True)
        output_thread.start()
        lines = []

        while process.poll() is None or not output_queue.empty():
            try:
                while True:
                    lines.append(output_queue.get_nowait())
            except Empty:
                pass

            yield {
                "running": process.poll() is None,
                "runtime": time.time() - start_time,
                "output": "".join(lines),
                "returncode": process.returncode,
            }
            time.sleep(0.25)

        returncode = process.wait()
        output_thread.join()
        try:
            while True:
                lines.append(output_queue.get_nowait())
        except Empty:
            pass

        yield {
            "running": False,
            "runtime": time.time() - start_time,
            "output": "".join(lines),
            "returncode": returncode,
        }
    finally:
        PIPELINE_LOCK.release()