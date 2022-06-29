# CyberTaskManager

## Setup
1. Install the dependencies:
    ```bash
    cd <repo_root>
    pip install -r requirements.txt
    ```
2. Refer to the `configs/config.py` file and set the suitable configuration
 params. You can set app's host, port and max number of tasks to execute in
  bulk.
3. Run the API app
    ```bash
    python app.py
    ```
4. Run the Processor app
    ```bash
   python processor.py
   ```
## Usage
> Refer to the [Postman](./CyberScanApp.postman_collection) schema to get
> familiar with app's API calls.
1. `api/ingest` - The `ingest` endpoint expected a JSON body that specifies
 task parameters. I added this option in order to facilitate the `raise_error` field which
 can assist in testing the `Error` status. 
2. `api/status_check/<task_id>` - This endpoint will return task status
 according to the assignment spec.

## Design

The system has 4 logical units:
1. API app (app.py) - contains the endpoints.
2. Processor (processor.py) - listens to above app, retrieves pending tasks
 and executed them.
2. SQL DB (mock) - contains tasks data (`id`, `created_at`, `is_fetched`,
`raise_error`\[a debug option\]).
4. DynamoDB (mock) - contains tasks statuses. This separation was done to
 eliminate additional loads on status checks.
 
   
   