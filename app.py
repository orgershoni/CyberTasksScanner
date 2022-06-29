from flask import Flask, jsonify, request
from db_wrapper import tasks_table, mongo_status_table, TaskStatus
from configs.config import global_config as config
app = Flask(__name__)


@app.route('/api/ingest', methods=['POST'])
def ingest_task():
    try:
        task_params = request.get_json()
        task = tasks_table.create(task_params)
        mongo_status_table.init_entry(task['id'])
        return {'task_id': task['id']}, 200
    except Exception as e:
        return {'message': f'Could not ingest task. Reason {e}'}, 400


@app.route('/api/update_task/<task_id>', methods=['PATCH'])
def update_task(task_id):
    try:
        updated_fields = request.get_json()
        task = tasks_table.update(task_id, updated_fields)
        if not task:
            return {"message": f'task id {task_id} was not found'}, 404
        return jsonify(task), 200
    except Exception as e:
        return {'message': f'Could not update task {task_id}.\nReason: {e}'}, 400


@app.route('/api/status_check/<task_id>', methods=['GET'])
def check_status(task_id):
    try:
        status = mongo_status_table.get_status(task_id)
        status = TaskStatus(status)
        return {'status': status.name}, status.value
    except Exception as e:
        return {'message': f'Failed to check status of task {task_id}.\nReason: {e}'}, 400


@app.route('/api/set_status/<task_id>/', methods=['PATCH'])
def set_task_status(task_id):
    try:
        status = int(request.args.get('status'))
        if not mongo_status_table.set_status(task_id, status):
            raise KeyError(f'id {task_id} was not found')
        status_name = TaskStatus(status).name
        return f'status of task {task_id} updated to {status_name}', 200
    except Exception as e:
        return {"message": f'Failed to set status of task {e}.\nReason: {e}'}, 400


@app.route('/api/fetch_tasks/', methods=['PATCH'])
def fetch_tasks():
    try:
        num_tasks = int(request.args.get('num_tasks'))
        tasks = tasks_table.fetch_pending_tasks(num_tasks)
        for task in tasks:
            tasks_table.update(task['id'], {'fetched': True})
        return jsonify(tasks), 200
    except Exception as e:
        return {'message': f'Failed to fetch tasks.\nReason:{e}'}, 400


if __name__ == '__main__':
    host = config.get('app_api_host')
    port = config.get('app_api_port')
    app.run(host=host, port=port)
