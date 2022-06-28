# CyberTaskManager

## Setup
1. Install the dependencies:
    ```bash
    cd <repo_root>
    pip install -r requirements.txt
    ```
2. Refer to the `configs/config.py` file and set the suitable configuration
 params.
3. Run the API app
    ```bash
    python app.py
    ```
4. Run the worker app
    ```bash
   python worker.py
   ```
## Usage
1. Refer to the postman schema (#add postman path here) to get familiar with
 app's API calls.
2. The `ingest` endpoint expected a JSON body that specifies task parameters
. I added this option in order to facilitate the `raise_error` field which
 can assist in testing the `Error` status. 
 
   
   