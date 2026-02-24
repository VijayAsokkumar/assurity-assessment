***API Test Framework (Pytest Based)
Overview***

This project is a scalable API test framework built using pytest.
It validates the Category Details API in a fully data-driven manner using YAML-based test configuration.

The framework is designed for extensibility and can be expanded to support additional APIs, HTTP methods, and validation rules.

***Prerequisites***

Python 3.x (latest recommended)

Python Virtual Environment (venv)

Verify Python version:

```python --version```

***Setup Instructions***
1. Create Virtual Environment
```python -m venv venv```
2. Activate Virtual Environment

Mac / Linux:

```source venv/bin/activate```

Windows:

```venv\Scripts\activate```
3. Install Dependencies

All required dependencies are listed in requirements.txt.

```pip install -r requirements.txt```

***Project Structure***
```
framework/
│
├── lib/
│   ├── api/
│   │   ├── api_service.py
│   │   └── api_urls.py
│   │
│   └── base/
│       └── base_config.py
│
├── tests/
│   └── scripts/
│       └── test_category_details.py
│
└── resources/
    └── data/
        └── test_data.yaml
```
***Component Description***
1. api_service.py

    Python requests-based API client.
    Currently supports GET operations and is designed to be extended for POST, PUT, and DELETE methods.

2. api_urls.py

    Centralized location for API endpoint definitions to support easy addition of new APIs.

3. base_config.py

    Loads configuration from .env file and shares environment and resource path information across the framework.

4. test_category_details.py

    Data-driven pytest test script that:

    Iterates through categories defined in YAML

    Validates HTTP status code

    Validates top-level response fields

    Validates Promotions section using rule-based conditions

5. test_data.yaml

    Contains all test execution data.
    New categories and validation rules can be added without modifying test logic.


***Running Tests***

Execute the tests and generate an HTML report using:

```pytest -v --html=reports/report.html --self-contained-html```

***Viewing Test Report***

After execution, the report will be generated in the reports/ directory:

```reports/report.html```

Open this file in a browser to view detailed test results.

***Key Features***

Built using pytest

Fully data-driven validation

Scalable architecture

Centralized configuration management

HTML reporting support

Designed for future extensibility