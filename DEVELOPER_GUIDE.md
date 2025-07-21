# Developer Documentation: CI to Lara Crew

## 1. Project Overview

This document provides instructions for setting up, running, and developing the **CI to Lara Crew** application. The application is a Python-based tool that leverages CrewAI and FastAPI to facilitate and validate migrations from the CodeIgniter (CI) framework to Laravel (Lara). It features agent-based orchestration, schema-based validation, comprehensive logging, and an extensible architecture for adding new migration crews and tools.

## 2. Key Components

### Application Entry Point
- **`app.py`**: Starts the FastAPI server, loads environment variables, sets up CORS, and includes API routers. It uses token-based middleware for security.

### CrewAI Integration
- **`src/base_crews/Ci2ToLara8XCrewBase.py`**: Defines the base crew, agents, and tasks.
- **`src/crews/Ci2Tolara8XCrew.py`**: Defines the main Crew class (`CiToLaraCrew`) using CrewAI decorators.
- **`src/base_crews/config/agents.yaml`**: Configurations for the AI agents.
- **`src/base_crews/config/tasks.yaml`**: Configurations for the AI tasks.
- **`src/base_crews/tools/custom_tool.py`**: Example of a custom tool for agent use.

### API Layer
- **`src/routers/api.py`**: Exposes a `/ci-lara-ai-converter` endpoint for migration validation and crew execution.

### Validation
- **`src/validation/migration_validator.py`**: Validates migration requests against a JSON schema.
- **`src/schemas/framework_migration_schema.json`**: The JSON schema for validation.

### Logging
- **`src/local_log/log.py`**: A logging utility that writes logs to `src/storage/logs/` and can also output to the console.

### Crew Factory
- **`src/factories/centralized_crew_factory.py`**: Dynamically discovers and registers crew classes from the `src/crews/` directory.

### Knowledge & User Preferences
- **`knowledge/user_preference.txt`**: Stores user-specific preferences and information.

### Testing
- **`tests/test_api.py`**: Unit tests for the API endpoints.

## 3. Prerequisites

- Python 3.8+
- Poetry

## 4. Setup and Installation

1.  **Install Dependencies**:
    This project uses Poetry to manage dependencies. Run the following command to install them:

    ```bash
    poetry install
    ```

2.  **Configure Environment Variables**:
    Copy the example environment file and update it with your credentials.

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

-   **Add New Crews**:
    Place new crew classes in the `src/crews/` directory. The factory will auto-discover and register them.

-   **Add New Agents/Tasks**:
    Update the YAML configuration files in `src/base_crews/config/`.

-   **Add New Tools**:
    Implement new tools in `src/base_crews/tools/` and reference them in the agent configurations.

## 9. Project Structure

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

## 10. Contribution Guidelines

Please adhere to the existing code style and conventions. Before submitting any changes, ensure that all tests pass successfully.

All contributions are subject to the terms outlined in the [`LICENSE`](LICENSE) file.

## 11. Authors

- Taj (tajulislamj200@gmail.com)

## 12. References

- [CrewAI Documentation](https://docs.crewai.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)