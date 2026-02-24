import logging as log
import os
import requests
from framework.lib.base.base_config import BaseConfig


class ApiService:
    """
    Reusable API service class to perform HTTP operations.
    """

    def __init__(self ):
        self.base_url = BaseConfig().get_api_base_url()
        self.session = requests.Session()

    def get(self, endpoint: str, params: dict | None = None, headers: dict | None = None):
        """
        Perform GET request
        :param endpoint: API endpoint (e.g., /v1/categories)
        :param params: Query parameters
        :param headers: Optional headers
        :return: Response object
        """
        log.info(f"Making GET request to endpoint: {endpoint} with params: {params} ")
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        response = self.session.get(url, params=params, headers=headers)

        # Raise exception for 4xx/5xx
        response.raise_for_status()

        return response

    def close(self):
        self.session.close()