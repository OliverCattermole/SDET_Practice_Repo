sdet-practice-playwright

📌 Project Overview
This repository serves as a showcase of my Playwright, Pytest, Jenkins & Docker skills. It demonstrates a robust automated testing framework covering Web UI and API layers, integrated into a containerised CI/CD pipeline.

The goal of this project is to implement scalable, maintainable, and environment-aware test automation that follows industry-standard design patterns.


🚀 Key Features
Web UI Automation: Built with Playwright using the Page Object Model (POM) for enhanced maintainability and reduced code duplication.

API Testing: Implemented using Requests with integrated JSON Schema Validation to ensure contract adherence and data integrity.

Infrastructure as Code: A declarative Jenkinsfile that manages the entire lifecycle: environment setup, linting, test execution, and report generation.

Code Quality: Integrated Flake8 linting within the CI pipeline to enforce PEP 8 standards and maintain high code quality.

Advanced Reporting: Integration with Allure Reports for detailed, visual test execution history and failure analysis.


🛠️ Tech Stack

Language - Python 3.x

Test Runner - Pytest

UI Automation - Playwright

Schema Validation - jsonschema

CI/CD - Jenkins (Pipeline as Code)

Containerisation - Docker

Linting - Flake8

Reporting - Allure


🏗️ CI/CD Pipeline

The project includes a Jenkinsfile that automates the following stages:

Setup: Initialises the Python virtual environment and installs system dependencies.

Static Analysis: Runs Flake8 to check for code style violations.

Test Execution: Runs the full suite (UI & API) using pytest.

Reporting: Generates and archives an Allure Report.

Cleanup: Automatically tears down the virtual environment post-execution.

