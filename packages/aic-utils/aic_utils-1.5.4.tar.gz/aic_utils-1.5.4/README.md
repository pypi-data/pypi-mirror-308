# AIC Utilities Package Documentation

## Overview
The AIC Utilities package provides a set of classes and methods to interact with the AIC API for managing projects, workspaces, and pipelines. It also integrates with GitLab for source control management and Slack for logging and notifications. The package includes three main components:

1. **AIC**: Manages interactions with the ACI API for fetching project and workspace details, handling pipeline configurations, and managing file uploads.
2. **GitLabManager**: Manages interactions with GitLab, including pushing files to repositories, managing repository existence, and ensuring the correct subgroup configuration based on the workspace.
3. **SlackLogger**: Provides logging functionality that sends log messages to a specified Slack channel, with the ability to redirect print statements to Slack.

## Classes and Methods

### 1. AIC Class
The `AIC` class handles interactions with the J.D. Power API, including managing projects, workspaces, pipelines, and file uploads.

#### Methods

- **`__init__(self, api_key, project, workspace, pipelines=[], gitlab_token=None)`**
  - Initializes the AIC instance with the specified API key, project, workspace, pipelines, and optional GitLab token.
  
- **`get_data(self)`**
  - Prints project, workspace, and drive IDs.

- **`get_config(self)`**
  - Returns the pipeline configurations.

- **`get_project(self, project)`**
  - Fetches the project ID for the specified project name.

- **`get_workspace(self, workspace)`**
  - Fetches the workspace ID for the specified workspace name.

- **`pop_pipelines(self)`**
  - Retrieves and returns the list of pipelines in the specified workspace.

- **`fetch_pipeline_config(self, pipeline)`**
  - Fetches the configuration for a single pipeline.

- **`pop_pipeline_config(self, pipelines)`**
  - Fetches configurations for multiple pipelines concurrently using `ThreadPoolExecutor`.

- **`get_drive_id(self, drive_name="config")`**
  - Fetches the drive ID for the specified drive name.

- **`upload_json(self, file_name, json_content)`**
  - Uploads JSON content to the specified drive.

- **`push_to_gitlab(self, pipelines=[])`**
  - Pushes pipeline configurations to GitLab concurrently.

- **`upload_configs_to_drive(self)`**
  - Uploads pipeline configurations to the drive.

- **`get_files_from_drive(self, drive_id=None)`**
  - Retrieves files from the specified drive.

- **`download_file(self, drive_id, file_name)`**
  - Downloads a file from the storage drive.

- **`download_from_gcs(self, gs_path)`**
  - Downloads content from Google Cloud Storage using the specified path.

- **`delete_file(self, drive_id, file_id)`**
  - Deletes a file from the storage drive.

- **`push_source_code(AIC_prod, AIC_qa, prod_to_qa=False, qa_to_prod=False, pipelines=[])`**
  - Overwrites pipeline configurations between production and QA based on the specified direction and pipelines.

- **`write_config_to_pipeline(self, config)`**
  - Uploads the given configuration to the corresponding pipeline job.

### 2. GitLabManager Class
The `GitLabManager` class manages interactions with GitLab, including pushing files, checking repository existence, and creating repositories if needed.

#### Methods

- **`__init__(self, aic_instance, gitlab_token=None, gitlab_namespace='pin/pin-analytics/pin-fusion-2.0/pipelines', gitlab_base_url='https://git.autodatacorp.org/api/v4', use_hash_comparison=True)`**
  - Initializes the GitLabManager instance with the specified AIC instance, GitLab token, namespace, base URL, and hash comparison setting.

- **`get_token_expiration_date(self)`**
  - Retrieves the expiration date of the GitLab token.

- **`check_token_expiration(self)`**
  - Checks and reports the token expiration date.

- **`read_gitlab_token(self)`**
  - Reads the GitLab token from the storage drive.

- **`generate_hash(self, content)`**
  - Generates a hash for the given content to check for changes.

- **`get_existing_file_content(self, repo_name, file_name)`**
  - Fetches the existing content of a file from the specified repository in GitLab.

- **`push_file_to_repo(self, repo_name, file_name, file_content)`**
  - Pushes a file to the specified repository in GitLab, only if the content has changed.

- **`ensure_correct_subgroup(self, workspace)`**
  - Ensures the correct subgroup path based on the workspace.

- **`create_repository(self, repo_name)`**
  - Creates a new repository in the specified subgroup.

- **`get_subgroup_id(self)`**
  - Fetches the GitLab subgroup ID based on the namespace path.

- **`get_namespace_id(self)`**
  - Retrieves the namespace ID for the current GitLab namespace.

- **`repository_exists(self, repo_path)`**
  - Checks if the repository exists in GitLab.

### 3. SlackLogger Class
The `SlackLogger` class provides logging functionality that sends log messages to a specified Slack channel. It includes a custom logging handler that integrates with Python's logging module.

#### Methods

- **`__init__(self, token, channel)`**
  - Initializes the SlackLogger with the specified Slack token and channel.

- **`send_message(self, text)`**
  - Sends a message to the specified Slack channel.

- **`SlackLoggerHandler(logging.Handler)`**
  - A custom logging handler that sends log messages to Slack using the SlackLogger.

- **`redirect_print_to_logger(logger)`**
  - Redirects print statements to the specified logger.

- **`create_logger(cls, slack_token='xoxb-7424459969442-7456034210037-EMCjbI9oi1xTszU1iUh4tLFH', slack_channel='C07DYFK5SE8', redirect_print=True)`**
  - Creates a logger that sends log messages to Slack, with options to redirect print statements.

## Usage Examples

### Creating an AIC Instance
```python
from aic_utils.aic import AIC

# Initialize AIC instance
aic_instance = AIC(api_key='your_api_key', project='PIN ANALYTICS', workspace='PIN FUSION 2.0', pipelines=['pipeline1', 'pipeline2'])
