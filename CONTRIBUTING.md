# Contributing to CI to Lara Crew

Thank you for your interest in contributing to the CI to Lara Crew project! We welcome contributions from everyone. By contributing, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (to be created if not present).

## Table of Contents

1.  [Project Overview](#1-project-overview)
2.  [Key Components](#2-key-components)
3.  [Prerequisites](#3-prerequisites)
4.  [Setup and Installation](#4-setup-and-installation)
5.  [Running the Application](#5-running-the-application)
6.  [Running the Crew Locally](#6-running-the-crew-locally)
7.  [Running Tests](#7-running-tests)
8.  [Extending the Project](#8-extending-the-project)
9.  [Contribution Guidelines](#9-contribution-guidelines)
    -   [Reporting Bugs](#reporting-bugs)
    -   [Suggesting Enhancements](#suggesting-enhancements)
    -   [Your First Contribution](#your-first-contribution)
    -   [Code Style and Conventions](#code-style-and-conventions)
    -   [Branching Strategy](#branching-strategy)
    -   [Pull Request Process](#pull-request-process)
10. [Project Structure](#10-project-structure)
11. [Authors](#11-authors)
12. [References](#12-references)

---

## 1. Project Overview

This project, **CI to Lara Crew**, is a Python application that leverages CrewAI and FastAPI to facilitate and validate migrations from the CodeIgniter (CI) framework to Laravel (Lara). It features agent-based orchestration, schema-based validation, comprehensive logging, and an extensible architecture for adding new migration crews and tools.

## 2. Key Components

-   **`app.py`**: Starts the FastAPI server, loads environment variables, sets up CORS, and includes API routers. It uses token-based middleware for security.
-   **`src/base_crews/Ci2ToLara8XCrewBase.py`**: Defines the base crew, agents, and tasks.
-   **`src/crews/Ci2Tolara8XCrew.py`**: Defines the main Crew class (`CiToLaraCrew`) using CrewAI decorators.
-   **`src/base_crews/config/agents.yaml`**: Configurations for the AI agents.
-   **`src/base_crews/config/tasks.yaml`**: Configurations for the AI tasks.
-   **`src/base_crews/tools/custom_tool.py`**: Example of a custom tool for agent use.
-   **`src/routers/api.py`**: Exposes a `/ci-lara-ai-converter` endpoint for migration validation and crew execution.
-   **`src/validation/migration_validator.py`**: Validates migration requests against a JSON schema.
-   **`src/schemas/framework_migration_schema.json`**: The JSON schema for validation.
-   **`src/local_log/log.py`**: A logging utility that writes logs to `src/storage/logs/` and can also output to the console.
-   **`src/factories/centralized_crew_factory.py`**: Dynamically discovers and registers crew classes from the `src/crews/` directory.
-   **`knowledge/user_preference.txt`**: Stores user-specific preferences and information.
-   **`tests/test_api.py`**: Unit tests for the API endpoints.

## 3. Prerequisites

-   Python 3.8+
-   Poetry

## 4. Setup and Installation

1.  **Install Dependencies**: This project uses Poetry to manage dependencies. Run the following command to install them:

    ```bash
    poetry install
    ```

2.  **Configure Environment Variables**: Copy the example environment file and update it with your credentials.

    ```bash
    copy .env.example .env
    ```

    Now, open the `.env` file and add the necessary API keys or other configuration values.

## 5. Running the Application

To run the FastAPI server, use the following command:

```bash
poetry run python app.py
```

The API will be accessible at `http://127.0.0.1:8000`.

## 6. Running the Crew Locally

To execute the crew directly from the command line, run:

```bash
poetry run run_crew
```

## 7. Running Tests

The project uses `pytest` for automated testing. To run the test suite, execute:

```bash
poetry run pytest
```

## 8. Extending the Project

-   **Add New Crews**: Place new crew classes in the `src/crews/` directory. The factory will auto-discover and register them.
-   **Add New Agents/Tasks**: Update the YAML configuration files in `src/base_crews/config/`.
-   **Add New Tools**: Implement new tools in `src/base_crews/tools/` and reference them in the agent configurations.

## 9. Contribution Guidelines

We welcome contributions in the form of bug reports, feature requests, and code contributions. Please follow these guidelines to ensure a smooth collaboration process.

### Reporting Bugs

-   Before opening a new bug report, please search existing issues to see if the bug has already been reported.
-   Provide a clear and concise description of the bug.
-   Include steps to reproduce the bug.
-   Specify your operating system, Python version, and any other relevant environment details.
-   If possible, include screenshots or error messages.

### Suggesting Enhancements

-   Before opening a new feature request, please search existing issues to see if the feature has already been suggested.
-   Clearly describe the proposed enhancement and its benefits.
-   Explain why this enhancement would be valuable to the project.
-   Provide any relevant examples or use cases.

### Your First Contribution

If you're new to contributing to open source, we recommend starting with small bug fixes or documentation improvements. Feel free to ask questions in the issue tracker if you need help.

### Code Style and Conventions

-   Please adhere to the existing code style and conventions found throughout the project.
-   We use `ruff` for linting and `black` for formatting. Ensure your code passes these checks before submitting a pull request.
-   Follow Python's PEP 8 style guide.
-   Add comments where necessary to explain complex logic, but avoid excessive commenting for self-explanatory code.
-   Ensure your code is well-tested.

### Branching Strategy

We use a feature-branch workflow:

1.  Fork the repository.
2.  Create a new branch from `main` for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/your-bug-fix-name`.
3.  Make your changes and commit them with clear, concise commit messages.
4.  Push your branch to your forked repository.

### Pull Request Process

1.  Ensure all tests pass and your code adheres to the project's code style.
2.  Open a pull request from your feature branch to the `main` branch of the upstream repository.
3.  Provide a clear and detailed description of your changes in the pull request description.
4.  Reference any related issues (e.g., `Fixes #123`, `Closes #456`).
5.  Be responsive to feedback and be prepared to make further changes if requested.

## 10. Project Structure

```
├── app.py
├── pyproject.toml
├── .env.example
├── knowledge/
│   └── user_preference.txt
├── src/
│   ├── base_crews/
│   │   ├── Ci2ToLara8XCrewBase.py
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   └── tools/
│   │       └── custom_tool.py
│   ├── crews/
│   │   └── Ci2Tolara8XCrew.py
│   ├── routers/
│   │   └── api.py
│   ├── validation/
│   │   └── migration_validator.py
│   ├── local_log/
│   │   └── log.py
│   ├── factories/
│   │   └── centralized_crew_factory.py
│   ├── schemas/
│   │   └── framework_migration_schema.json
│   └── storage/
│       └── logs/
├── tests/
│   └── test_api.py
└── LICENSE
```

## 11. Authors

-   Taj (tajulislamj200@gmail.com)

## 12. References

-   [CrewAI Documentation](https://docs.crewai.com/)
-   [FastAPI Documentation](https://fastapi.tiangolo.com/)
