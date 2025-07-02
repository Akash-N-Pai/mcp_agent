# mcp_server.py

from flask import Flask, jsonify
from handlers import list_jobs, get_job, cluster_status

app = Flask(__name__)

@app.route("/list_jobs", methods=["GET"])
def list_jobs_route():
    return jsonify(list_jobs())

@app.route("/get_job/<job_id>", methods=["GET"])
def get_job_route(job_id):
    return jsonify(get_job(job_id))

@app.route("/cluster_status", methods=["GET"])
def cluster_status_route():
    return jsonify(cluster_status())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
