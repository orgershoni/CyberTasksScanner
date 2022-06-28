from flask import Flask, jsonify, request
from db_wrapper import tasks_table, TaskStatus
from configs.config import global_config as config
app = Flask(__name__)


@app.route('/api/ingest', methods=['POST'])
def ingest_task():
    try:
        task_params = request.get_json()
        task = tasks_table.create(task_params)
        return {'task_id': task['id']}, 200
    except Exception as e:
        return {'message': f'could not ingest task. Reason {e}'}, 400


@app.route('/api/update_task/<task_id>', methods=['PATCH'])
def update_task(task_id):
    updated_fields = request.json
    task = tasks_table.update(task_id, updated_fields)
    if not task:
        return {"message": f'task id {task_id} was not found'}, 404
    return jsonify(task), 200


@app.route('/api/status_check/<task_id>', methods=['GET'])
def check_status(task_id):
    scan = tasks_table.find_by_id(task_id)
    if not scan:
        status = TaskStatus.NotFound.name
        return {'status': status}, 404
    status = TaskStatus(scan['status']).name
    return {'status': status}, 200


@app.route('/api/fetch_tasks/', methods=['GET'])
def fetch_tasks():
    try:
        num_tasks = int(request.args.get('num_tasks'))
        tasks = tasks_table.fetch_pending_tasks(num_tasks)
        return jsonify(tasks), 200
    except Exception as e:
        return {'message': f'{e}'}, 400


if __name__ == '__main__':
    host = config.get('app_api_host')
    port = config.get('app_api_port')
    app.run(host=host, port=port)
