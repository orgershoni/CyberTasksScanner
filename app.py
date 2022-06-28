from flask import Flask, jsonify, request
from db_wrapper import cyber_scan_table, TaskStatus
from configs.config import global_config as config
app = Flask(__name__)


@app.route('/api/ingest', methods=['POST'])
def ingest_task():
    try:
        task_params = request.get_json()
        task = cyber_scan_table.create(task_params)
        return {'task_id': task['id']}, 200
    except Exception as e:
        return {'message': f'could not ingest task. Reason {e}'}, 400


@app.route('/api/update_task/<task_id>', methods=['PATCH'])
def update_task(task_id):
    updated_fields = request.json
    task = cyber_scan_table.update(task_id, updated_fields)
    if not task:
        return {"message": f'task id {task_id} was not found'}, 404
    return jsonify(task), 200


@app.route('/api/status_check/<task_id>', methods=['GET'])
def check_status(task_id):
    scan = cyber_scan_table.find_by_id(task_id)
    if not scan:
        status = TaskStatus.NotFound.name
        return {'status': status}, 404
    status = TaskStatus(scan['status']).name
    return {'status': status}, 200


@app.route('/api/fetch_tasks/', methods=['GET'])
def fetch_tasks():
    try:
        bulk_process = request.args.get('bulk_process')
        tasks = cyber_scan_table.fetch_pending_tasks(bulk_process)
        return jsonify(tasks), 200
    except Exception as e:
        return {'message': f'{e}'}, 400


if __name__ == '__main__':
    host = config.get('app_api_host')
    port = config.get('app_api_port')
    app.run(host=host, port=port)
