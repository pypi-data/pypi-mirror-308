import os

import yaml
from flasgger import Swagger
from flask import Flask, jsonify, request

import t1cicd.cicd.server.reports as reports
from t1cicd.cicd.db.db import init_flask_db
from t1cicd.cicd.parser.parser import YAMLParser
from t1cicd.cicd.parser.utils import (
    apply_override,
    get_dry_run_order,
    is_valid_override,
)
from t1cicd.cicd.server.gitHandler import HandleGit
from t1cicd.cicd.server.mock import MockConfiguration
from t1cicd.cicd.server.run_pipeline.dockerRunner import DockerJobRunner
from t1cicd.cicd.server.run_pipeline.pipelineScheduler import PipelineScheduler

app = Flask(__name__)
swagger = Swagger(app)
init_flask_db(app)

mock = MockConfiguration()
config = mock.load_config()

# Define the API root dir
API_ROOT_DIR = os.getcwd()
TEMP_DIR = os.path.abspath("./tmp")
PIPELINES_DIR = os.path.abspath(".cicd-pipelines")


@app.route("/")
def welcome_page():
    """Welcome Page
    ---
    responses:
      200:
        description: Welcome message
    """
    return "REST API for CICD System!"


@app.route("/api/check-config", methods=["POST"])
def check_config():
    """Check YAML Configuration
    ---
    parameters:
      - name: yaml_path
        in: body
        type: string
        required: true
        description: Path to the YAML configuration file
    responses:
      200:
        description: Valid YAML configuration
      404:
        description: YAML file not found
      400:
        description: Invalid YAML or other error
    """
    data = request.json

    # Get the path to the YAML config file
    yaml_path = data.get("yaml_path")

    # Try parsing the YAML configuration
    try:
        parser = YAMLParser(yaml_path)
        parser.parse()
    except FileNotFoundError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "YAML file not found at the specified path",
                }
            ),
            404,
        )
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except yaml.YAMLError as exc:
        return (
            jsonify({"status": "error", "message": f"Invalid YAML: {str(exc)}"}),
            400,
        )

    return (
        jsonify({"status": "success", "message": "YAML configuration is valid"}),
        200,
    )


@app.route("/api/dry-run", methods=["POST"])
def dry_run():
    """Dry Run Pipeline
    ---
    parameters:
      - name: yaml_path
        in: body
        required: true
        schema:
          type: object
          properties:
            yaml_path:
              type: string
              description: Path to the YAML configuration file
    responses:
      200:
        description: Successful dry run execution
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Dry run executed successfully. Pipeline: TestPipeline, Job order: Stage: Stage1, Job: Job1"
      404:
        description: YAML file not found
      400:
        description: Invalid YAML or other error
    """
    data = request.json
    # Get the path to the YAML config file
    yaml_path = data.get("yaml_path")

    if not yaml_path:
        yaml_path = "../../../.cicd/pipeline.yml"

    # Parse the YAML configuration using YAMLParser
    try:
        parser = YAMLParser(yaml_path)
        parsed_pipeline = parser.parse()
    except FileNotFoundError:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "YAML file not found at the specified path",
                }
            ),
            404,
        )
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    except yaml.YAMLError as exc:
        return (
            jsonify({"status": "error", "message": f"Invalid YAML: {str(exc)}"}),
            400,
        )

    # job order
    job_order = get_dry_run_order(parsed_pipeline.parsed_stages.stages)

    print(job_order)
    # For each stage, add all jobs in topo order in job_order
    # for stage_name, jobs in parsed_pipeline.get_all_stages():
    #     # Create a new dictionary for each stage
    #     stage = {"stage_name": stage_name}
    #
    #     # Perform topological sorting for the jobs in the current stage
    #     jobs_in_stage = get_dry_run_order(jobs)
    #
    #     # Add the sorted jobs to the stage dictionary
    #     stage["jobs"] = jobs_in_stage
    #
    #     # Append the stage to the job order
    #     job_order.append(stage)

    # Including the job order in the message
    message = (
        f"Dry run executed successfully. \n"
        f"Pipeline: {parsed_pipeline.pipeline_name}, \n"
        f"Job order: {job_order}"
    )

    return jsonify({"status": "success", "message": message}), 200


@app.route("/api/run-pipeline", methods=["POST"])
def run_pipeline():
    """Run Pipelines
    ---
    parameters:
      - in: body
        name: pipeline_data
        required: false
        schema:
          type: object
          properties:
            repo:
              type: string
              description: URL of the repository
              example: "https://github.com/example/repo.git"
            commit:
              type: string
              description: Commit hash to use for the pipeline run
              example: "abc123"
            branch_name:
              type: string
              description: Name of the branch to run pipelines on (default is 'main')
              example: "main"
            pipeline:
              type: string
              description: Name of the pipeline to execute (mutually exclusive with 'file')
              example: "pipeline_hello_world"
            file:
              type: string
              description: Path to the specific pipeline config file (mutually exclusive with 'pipeline')
              example: "../.cicd-pipelines/pipeline_hello_world.yml"
    responses:
      200:
        description: Successful pipeline run
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Pipelines successfully triggered for branch 'main', commit 'abc123' on repository 'https://github.com/example/repo.git'"
      400:
        description: Bad request due to mutual exclusivity error or invalid input
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Only one of --pipeline or --file can be provided."
      404:
        description: Config file or resource not found
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "Config file or resource not found. Ensure the file path is correct and the file exists."
      500:
        description: Server error due to runtime issues or unexpected failures
        schema:
          type: object
          properties:
            status:
              type: string
              example: "error"
            message:
              type: string
              example: "A runtime error occurred during pipeline execution: Git cloning errors, Docker issues, or pipeline configuration issues."
    """
    # Get the parameters from the request
    data = request.json
    pipeline_name = data.get("pipeline")
    config_file = data.get("file")
    repo = data.get("repo")
    commit = data.get("commit")
    branch = data.get("branch_name") or "main"
    # Mutual exclusivity check
    if pipeline_name and config_file:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Only one of --pipeline or --file can be provided.",
                }
            ),
            400,
        )

    try:
        # Change to API ROOT DIR before every request
        os.chdir(API_ROOT_DIR)

        # Initialize and run the PipelineScheduler
        pipeline_scheduler = PipelineScheduler(
            repo=repo,
            branch=branch,
            commit=commit,
            config_file=config_file,
            pipeline_name=pipeline_name,
            temp_dir=TEMP_DIR,  # Make sure this points to your temporary directory
            pipelines_dir=PIPELINES_DIR,  # Your folder containing pipelines
            git_handler=HandleGit(),  # Custom or default git handler
            docker_runner=DockerJobRunner(),  # Custom or default Docker runner
        )

        # Run the pipeline
        pipeline_result = pipeline_scheduler.run()

        # Change to API ROOT DIR from TEMP DIR
        os.chdir(API_ROOT_DIR)

    except FileNotFoundError as e:
        error_msg = (
            f"Config file or resource not found: {str(e)}."
            f"Ensure the file path is correct and the file exists."
            f"Attempted to find the file: {config_file or 'No config file provided'}"
        )
        return jsonify({"status": "error", "message": error_msg}), 404

    except ValueError as e:
        error_msg = (
            f"Invalid input detected: {str(e)}."
            f"Check the repository URL, branch name, commit hash, or pipeline name."
            f"Provided repo: {repo}, branch: {branch}, commit: {commit}, pipeline: {pipeline_name}."
        )
        return jsonify({"status": "error", "message": error_msg}), 400

    except RuntimeError as e:
        error_msg = (
            f"A runtime error occurred during pipeline execution: {str(e)}."
            f"Possible issues include Git cloning errors, Docker execution problems, "
            f"or pipeline configuration issues."
            f"Attempted repository: {repo}, branch: {branch}, commit: {commit}, config: {config_file}."
        )
        return jsonify({"status": "error", "message": error_msg}), 500

    except Exception as e:
        error_msg = (
            f"An unexpected error occurred: {str(e)}. "
            f"Please check the provided repository URL, branch, commit hash, and config file. "
            f"Provided data: repo: {repo}, branch: {branch}, commit: {commit}, config file: {config_file}, pipeline: {pipeline_name}."
        )
        return jsonify({"status": "error", "message": error_msg}), 500

    return jsonify({"status": "success", "message": pipeline_result}), 200


@app.route("/api/stop-pipeline", methods=["POST"])
def stop_pipeline():
    """Stop Pipelines
    ---
    parameters:
      - name: repo
        in: body
        required: true
        schema:
          type: object
          properties:
            repo:
              type: string
              description: URL of the repository
            commit:
              type: string
              description: Commit hash to use
            branch_name:
              type: string
              description: Name of the branch to stop pipelines on
    responses:
      200:
        description: Successful pipeline stop
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Pipelines successfully stopped for branch 'main', commit 'abc123' on repository 'https://github.com/example/repo.git'"
      500:
        description: Failed to stop pipeline
    """
    data = request.json

    # Get the repository URL and branch name from the request
    repo = data.get("repo")
    commit = data.get("commit")
    branch = data.get("branch_name")

    # Dummy logic for stop the pipeline
    try:
        # In a real use case, you would clone the repository and check out the branch here
        # This could be done with git commands or a similar mechanism
        pipeline_result = f"Pipelines successfully stopped for branch '{branch}', commit '{commit}' on repository '{repo}'"

        # For example, you might run some pipeline logic here and todo

    except Exception as e:
        # Return an error if something went wrong
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Failed to stopped pipeline: {str(e)}",
                }
            ),
            500,
        )

    # Return success with the pipeline result
    return jsonify({"status": "success", "message": pipeline_result}), 200


@app.route("/api/override-config", methods=["POST"])
def override_config():
    """Override Configuration
    ---
    parameters:
      - name: repo
        in: body
        required: true
        schema:
          type: object
          properties:
            repo:
              type: string
              description: URL of the repository
            override:
              type: string
              description: New configuration to override the existing configuration
    responses:
      200:
        description: Successful configuration override
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            message:
              type: string
              example: "Configuration successfully overridden for repository "
      500:
        description: Failed to override configuration
      400:
        description: Invalid override configuration
    """
    data = request.json

    # Get the repository URL and override configuration from the request
    repo = data.get("repo")
    override = data.get("override")
    print(override)
    try:
        if not is_valid_override(override):
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Invalid override configuration",
                    }
                ),
                400,
            )
        print(config)
        apply_override(config, override)
        print(config)
        override_result = f"Configuration successfully overridden for repository {repo}"

    except Exception as e:
        # Return an error if something went wrong
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Failed to override configuration: {str(e)}",
                }
            ),
            500,
        )

    # Return success with the override result
    return jsonify({"status": "success", "message": override_result}), 200


@app.route("/api/report", methods=["GET"])
def get_all_pipelines_summary():
    """Get all pipelines summary
    ---
    parameters:
      - name: repo
        in: query
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of all pipelines summary
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            data:
              type: object
              properties:
                repo:
                  type: string
                  description: URL of the repository
                pipelines:
                  type: array
                  items:
                    type: object
                    properties:
                      pipeline_name:
                        type: string
                      runs:
                        type: array
                        items:
                          type: object
                          properties:
                            run_number:
                              type: integer
                            git_commit_hash:
                              type: string
                            status:
                              type: string
                            start_time:
                              type: string
                              format: date-time
                            completion_time:
                              type: string
                              format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    repo_summary = reports.repo_run_summary_response
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "message": "".join(
                    [
                        "showing all pipelines summary for all runs.\n\n",
                        repo_summary.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route("/api/report/pipeline/<pipeline_name>", methods=["GET"])
def get_pipeline_summary(pipeline_name):
    """Get pipeline summary
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of pipeline summary
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            data:
              type: object
              properties:
                runs:
                  type: array
                  items:
                    type: object
                    properties:
                      run_number:
                        type: integer
                      git_commit_hash:
                        type: string
                      status:
                        type: string
                      start_time:
                        type: string
                        format: date-time
                      completion_time:
                        type: string
                        format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    pipeline_summary = reports.pipeline_run_detail_response
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "message": "".join(
                    [
                        "Showing a specific pipeline summary for all runs.\n\n",
                        pipeline_summary.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route("/api/report/pipeline/<pipeline_name>/<int:run_number>", methods=["GET"])
def get_pipeline_run_detail(pipeline_name, run_number):
    """Get pipeline run detail
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of pipeline run detail
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            run:
              type: integer
              description: Run number of the pipeline
            data:
              type: object
              properties:
                git_commit_hash:
                  type: string
                status:
                  type: string
                stages:
                  type: array
                  items:
                    type: object
                    properties:
                      stage_name:
                        type: string
                      stage_status:
                        type: string
                      start_time:
                        type: string
                        format: date-time
                      completion_time:
                        type: string
                        format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    pipeline_run = reports.pipeline_run_detail
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "run": run_number,
                "message": "".join(
                    [
                        "Showing a specific pipeline run detail.\n\n",
                        pipeline_run.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route("/api/report/stage/<pipeline_name>/<stage_name>", methods=["GET"])
def get_stage_summary(pipeline_name, stage_name):
    """Get stage summary
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of stage summary
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            stage:
              type: string
              description: Name of the stage
            data:
              type: object
              properties:
                stage_status:
                  type: string
                start_time:
                  type: string
                  format: date-time
                completion_time:
                  type: string
                  format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    stage_summary = reports.stage_run_detail_response
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "stage": stage_name,
                "message": "".join(
                    [
                        "Showing a specific stage summary for all runs.\n\n",
                        stage_summary.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route(
    "/api/report/stage/<pipeline_name>/<stage_name>/<int:run_number>",
    methods=["GET"],
)
def get_stage_run_detail(pipeline_name, stage_name, run_number):
    """Get stage run detail
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of stage run detail
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            stage:
              type: string
              description: Name of the stage
            run:
              type: integer
              description: Run number of the stage
            data:
              type: object
              properties:
                git_commit_hash:
                  type: string
                stage_status:
                  type: string
                jobs:
                  type: array
                  items:
                    type: object
                    properties:
                      job_name:
                        type: string
                      job_status:
                        type: string
                      allows_failure:
                        type: boolean
                      start_time:
                        type: string
                        format: date-time
                      completion_time:
                        type: string
                        format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    stage_run = reports.stage_run_detail
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "stage": stage_name,
                "run": run_number,
                "message": "".join(
                    [
                        "Showing a specific stage run detail.\n\n",
                        stage_run.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route("/api/report/job/<pipeline_name>/<stage_name>/<job_name>", methods=["GET"])
def get_job_summary(pipeline_name, stage_name, job_name):
    """Get job summary
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of job summary
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            stage:
              type: string
              description: Name of the stage
            job:
              type: string
              description: Name of the job
            data:
              type: object
              properties:
                job_status:
                  type: string
                allows_failure:
                  type: boolean
                start_time:
                  type: string
                  format: date-time
                completion_time:
                  type: string
                  format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    job_summary = reports.job_run_detail_response
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "stage": stage_name,
                "job": job_name,
                "message": "".join(
                    [
                        "Showing a specific job summary for all runs.\n\n",
                        job_summary.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


@app.route(
    "/api/report/job/<pipeline_name>/<stage_name>/<job_name>/<int:run_number>",
    methods=["GET"],
)
def get_job_run_detail(pipeline_name, stage_name, job_name, run_number):
    """Get job run detail
    ---
    parameters:
      - name: repo
        in: body
        type: string
        required: true
        description: URL of the repository
    responses:
      200:
        description: Successful retrieval of job run detail
        schema:
          type: object
          properties:
            status:
              type: string
              example: "success"
            repo:
              type: string
              description: URL of the repository
            pipeline:
              type: string
              description: Name of the pipeline
            stage:
              type: string
              description: Name of the stage
            job:
              type: string
              description: Name of the job
            run:
              type: integer
              description: Run number of the job
            data:
              type: object
              properties:
                git_commit_hash:
                  type: string
                job_status:
                  type: string
                allows_failure:
                  type: boolean
                start_time:
                  type: string
                  format: date-time
                completion_time:
                  type: string
                  format: date-time
      400:
        description: Invalid input or parameters
    """
    data = request.json
    repo = data.get("repo")
    if not repo:
        return (
            jsonify({"status": "error", "message": "Repository URL is required"}),
            400,
        )
    job_run = reports.job_run_detail
    return (
        jsonify(
            {
                "status": "success",
                "repo": repo,
                "pipeline": pipeline_name,
                "stage": stage_name,
                "job": job_name,
                "run": run_number,
                "message": "".join(
                    [
                        "Showing a specific job run detail.\n\n",
                        job_run.model_dump_json(),
                    ]
                ),
            }
        ),
        200,
    )


def main():
    app.run(debug=False)


if __name__ == "__main__":
    app.run(debug=False)
