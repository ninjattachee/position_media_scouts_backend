from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import Dict, Literal


@dataclass
class Event:
    timestamp: datetime
    data: str

@dataclass
class Job:
    status: Literal["Running", "Completed", "Failed"]
    events: list[Event]
    result: str

jobs_lock = Lock()
jobs: Dict[str, "Job"] = {}

def append_event(job_id: str, event_data: str):
    with jobs_lock:
        if job_id not in jobs:
            print(f"Starting new job {job_id}")
            jobs[job_id] = Job(status="Running", events=[], result="")
        
        print(f"Appending event to job {job_id}")
        jobs[job_id].events.append(Event(timestamp=datetime.now(), data=event_data))
