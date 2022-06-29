global_config = {
  "app_api_protocol": "http",
  "app_api_host": "localhost",
  "app_api_port": 3002,
  "max_tasks_to_process": 1  # How many tasks should be processed in bulk
}

app_url = f'{global_config["app_api_protocol"]}://' \
          f'{global_config["app_api_host"]}:{global_config["app_api_port"]}'