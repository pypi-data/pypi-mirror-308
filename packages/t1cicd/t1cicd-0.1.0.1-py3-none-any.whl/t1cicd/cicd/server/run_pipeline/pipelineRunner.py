from t1cicd.cicd.parser.parser import YAMLParser


class PipelineRunner:
    def __init__(
        self,
        repo,
        branch,
        commit,
        config_file=None,
        pipeline_name=None,
        temp_dir=None,
        git_handler=None,
        docker_runner=None,
    ):
        self.repo = repo
        self.branch = branch
        self.commit = commit
        self.config_file = config_file
        self.pipeline_name = pipeline_name
        self.sorted_jobs = []
        self.temp_dir = temp_dir
        self.git_handler = git_handler
        self.docker_runner = docker_runner

    def clone_and_prepare_repo(self):
        try:
            # Git clone and checkout
            self.git_handler.clone_and_checkout(
                self.repo, self.branch, self.commit, self.temp_dir
            )
        except Exception as e:
            raise RuntimeError(f"Failed to clone and checkout the repo: {e}")

    def get_sorted_jobs(self):
        try:
            # Situation 1: Only --file is provided
            if self.config_file:
                print(f"Config file found: {self.config_file}")
                parser = YAMLParser(self.config_file)
                parsed_pipeline = parser.parse()
                for stage_name in parsed_pipeline.get_all_stage_names():
                    print(f"Executing Stage: {stage_name}")
                    self.sorted_jobs = (
                        parsed_pipeline.parsed_stages.get_sorted_jobs_in_stage(
                            stage_name
                        )
                    )

            # TODO: Handle other cases (pipeline_name or multiple pipelines in repo)
            elif self.pipeline_name:
                pass  # Logic for a single pipeline
            else:
                pass  # Logic to run all pipelines in the repo
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {e}")
        except Exception as e:
            raise RuntimeError(f"Error parsing the pipeline config: {e}")

    def execute_jobs(self):
        try:
            absolute_path = self.temp_dir
            volumes = {absolute_path: {"bind": "/app", "mode": "rw"}}
            work_dir = "/app"

            for job in self.sorted_jobs:
                print(f"Executing job: {job.name}")
                self.docker_runner.execute_job(job, work_dir, volumes, auto_clean=True)
        except Exception as e:
            raise RuntimeError(f"Error executing job: {e}")

    def get_pipeline_result(self):
        if self.config_file:
            return f"Pipelines triggered for branch '{self.branch}', commit '{self.commit}', using config file '{self.config_file}'"
        elif self.pipeline_name:
            return f"Pipelines triggered for branch '{self.branch}', commit '{self.commit}', using pipeline '{self.pipeline_name}'"
        else:
            return f"Pipelines triggered for branch '{self.branch}', commit '{self.commit}', with pipelines in the repo."

    def run(self):
        self.clone_and_prepare_repo()
        self.get_sorted_jobs()
        self.execute_jobs()
        return self.get_pipeline_result()
