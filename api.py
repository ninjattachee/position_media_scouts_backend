from datetime import datetime
import json
import uuid
from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS

from crew import CompanyResearchCrew
from job_manager import Event, append_event, jobs, jobs_lock
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def kickoff_crew(companies: list[str], positions: list[str], job_id: str):
    logger.info(f"Kicking off crew for {companies} with positions {positions} and job_id {job_id}")

    # Setup crew
    results = None
    try:
        crew = CompanyResearchCrew(job_id)
        crew.setup_crew(companies, positions)
        
        results = crew.kickoff()
        logger.info(f"Crew for job {job_id} completed", results)

    except Exception as e:
        logger.error(f"Error kicking off crew: {e}")
        append_event(job_id, f"Error kicking off crew: {e}")
        jobs[job_id].result = str(e)
        jobs[job_id].status = "Failed"

    with jobs_lock:
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(timestamp=datetime.now(), data=f"Crew completed"))
        jobs[job_id].status = "Completed"


@app.route('/api/crew', methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        return jsonify({"status": "Failed", "message": "Missing required fields"}), 400

    job_id = str(uuid.uuid4())
    companies = data['companies']
    positions = data['positions']

    # Run the crew
    thread = Thread(target=kickoff_crew, args=(companies, positions, job_id))
    thread.start()

    return jsonify({ "job_id": job_id }), 200

@app.route('/api/crew/<job_id>', methods=['GET'])
def get_crew(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return jsonify({ "status": "Failed", "message": "Job not found" }), 404

    # Parse the JSON data
    try:
        result_json = json.loads(job.result)
    except json.JSONDecodeError:
        result_json = job.result

    # Return everything
    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    }), 200
    


if __name__ == '__main__':
    app.run(debug=True, port=3001)