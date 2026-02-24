import os
import logging as log
import dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
framework_root = os.path.dirname(os.path.dirname(current_dir))
class BaseConfig:
    """
    Base configuration class to manage environment variables and common settings.
    """

    def __init__(self):
        log.info("Loading configuration from environment variables...")
        self.resources_path = os.path.join(os.path.dirname(framework_root), "resources")
        log.info(f"Resources path set to: {self.resources_path}")
    
    def get_api_base_url(self) -> str:
        dotenv.load_dotenv(self.get_environment_file())
        return os.getenv("BASE_URL", "https://api.tmsandbox.co.nz") 
    
    def get_environment_file(self) -> str:
        env_file = os.path.join(self.resources_path, ".env")
        log.info(f"Environment file path: {env_file}")
        return env_file
    
    def get_test_data_path(self) -> str:
        test_data_path = os.path.join(self.resources_path, "data", "testdata.yaml")
        log.info(f"Test data path: {test_data_path}")
        return test_data_path