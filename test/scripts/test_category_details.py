from re import match

from dotenv.main import logger

from framework.lib.api.api_service import ApiService
from framework.lib.api.api_urls import APIEndpoints
import os
import logging as log
import pytest
from framework.lib.base.base_config import BaseConfig
import yaml



@pytest.fixture()
def api():
    """Provide ApiService instance for tests and close it safely."""
    service = ApiService()
    yield service
    service.close()

@pytest.fixture(scope="session")
def testdata():
    path = BaseConfig().get_test_data_path()
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_get_category_details(api, testdata):
    """
    Test Category Details API for multiple categories defined in testdata.
    This test dynamically reads category configurations from the YAML testdata file,
    calls the Category Details endpoint for each category, and validates:
    - HTTP status code
    - Top-level response fields (exact match)
    - Promotions section (match by Name and validate conditions such as 'contains')
    The test is fully data-driven and scalable — new categories or validation rules
    can be added in testdata without modifying the test logic.
    """
    print("Running test_get_category_details...",testdata)
    category_details = testdata.get("category_details")
    for category in category_details.keys():
        print("Processing category:", category)
        print("Category Details from testdata:", category_details,category_details.keys())
        response = api.get(
        APIEndpoints.CATEGORY_DETAILS.format(category_id=category),
        params={"catalogue": "false"},)
        data = response.json()
        log.info(f"Received response for category {category}: {data.keys()}")
        expected = category_details[category].get("expected")
        print("Expected data:", expected)
        for expected_item in expected:
            log.info(f"Validating {expected_item}...")
            if expected_item == "status_code":
                log.info("--- Status code  validation Started ---")
                assert response.status_code == expected[expected_item], f"Expected status code {expected[expected_item]}, but got {response.status_code}"
                log.info("Status code validation passed. Expected=%d Actual=%d", expected[expected_item], response.status_code)
                log.info("--- Status code  validation Completed ---")
            elif expected_item == "fields":
                log.info("--- Fields  validation Started ---")
                log.info(f"Validating presence of fields: {expected[expected_item]} in response data")
                for field in expected[expected_item]:
                    log.info("Checking field '%s' in response data...", field)
                    assert field in data, f"Expected field '{field}' not found in response data"
                    assert data[field] == expected[expected_item][field], f"Expected field '{field}' to be {expected[expected_item][field]}, but got {data[field]}"
                    log.info("Field '%s' validation passed. Expected=%r Actual=%r",
                             field,expected[expected_item][field],data[field])
                log.info("--- Fields  validation Completed ---")
            elif expected_item == "Promotions":
                log.info("--- Promotion  validation Started ---")
                log.info(f"Validating presence of fields: {expected[expected_item]} in response data")
                for promotions in expected[expected_item]:
                    log.info("Checking field '%s' in response data...", promotions)
                    promotion_check_length = len(promotions)
                    response_promotions = data.get("Promotions", [])
                    print("Response Promotions:", response_promotions)
                    matched_conditions = 0
                    for promotion in response_promotions:
                        log.info("Checking promotion '%s' in response data...", promotion)
                        if promotion["Name"] == promotions["match"]["Name"]:
                            matched_conditions += 1
                            promotion_validations = promotions["match"]["validations"]
                            for promotion_validation, promotion_validation_condition in promotion_validations.items():
                                log.info("Checking promotion field '%s' in response data %s...", promotion_validation, promotion_validation_condition)
                                
                                if "contains" in promotion_validation_condition:
                                    match_text = str(promotion_validations[promotion_validation]['contains'])
                                    response_promotions_text = str(promotion[promotion_validation])
                                    assert promotion_validation in promotion, f"Expected promotion field '{promotion_validation}' not found in response data"
                                    assert match_text in response_promotions_text, (f"Expected '{response_promotions_text}' to contain '{match_text}'"
)
                        if matched_conditions == promotion_check_length:
                            log.info("--- Promotion  validation Completed ---")
                            break
                            
            else:
                assert data.get(expected_item) == expected[expected_item], f"Expected {expected_item} to be {expected[expected_item]}, but got {data.get(expected_item)}"


    
