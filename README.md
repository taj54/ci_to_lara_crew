# CI to Lara Crew: Project Overview

## Description

**CI to Lara Crew** is a Python application that leverages CrewAI and FastAPI to facilitate and validate migrations from CodeIgniter (CI) to Laravel (Lara). It features agent-based orchestration, schema-based validation, logging, and an extensible architecture for adding new migration crews and tools.

---

## Project Structure

```
.
├── app.py
├── pyproject.toml
├── .env.example
├── knowledge/
│   └── user_preference.txt
├── src/
│   ├── base_crews/
│   │   ├── Ci2ToLara8XCrewBase.py
│   │   ├── main.py
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
│   └── test_migration_validator.py
```

---

## Key Components

### Application Entry Point

- **[app.py](app.py)**  
  Starts the FastAPI server, loads environment variables, sets up CORS, and includes API routers. Uses token-based middleware for security.

### CrewAI Integration

- **[src/ci_to_lara_crew/crew.py](src/ci_to_lara_crew/crew.py)**  
  Defines the main Crew class (`CiToLaraCrew`) using CrewAI decorators. Agents and tasks are configured via YAML files:
  - [agents.yaml](src/ci_to_lara_crew/config/agents.yaml)
  - [tasks.yaml](src/ci_to_lara_crew/config/tasks.yaml)

- **[src/ci_to_lara_crew/main.py](src/ci_to_lara_crew/main.py)**  
  CLI entry points for running, training, replaying, and testing the crew.

- **[src/ci_to_lara_crew/tools/custom_tool.py](src/ci_to_lara_crew/tools/custom_tool.py)**  
  Example of a custom tool for agent use.

### API Layer

- **[src/routers/api.py](src/routers/api.py)**  
  Exposes a `/ci-lara-ai-converter` endpoint for migration validation and crew execution.

### Validation

- **[src/validation/migration_validator.py](src/validation/migration_validator.py)**  
  Validates migration requests against a schema ([framework_migration_schema.json](src/schemas/framework_migration_schema.json)). Returns detailed error messages for invalid requests.

### Logging

- **[src/local_log/log.py](src/local_log/log.py)**  
  Logging utility that writes logs to `src/storage/logs/` and optionally to the console.

### Crew Factory

- **[src/factories/centralized_crew_factory.py](src/factories/centralized_crew_factory.py)**  
  Dynamically discovers and registers crew classes from the `crews` directory.

### Knowledge & User Preferences

- **[knowledge/user_preference.txt](knowledge/user_preference.txt)**  
  Stores user-specific preferences and information.

### Testing

- **[tests/test_migration_validator.py](tests/test_migration_validator.py)**  
  Unit tests for the migration validator.

---

## Configuration

- **Environment Variables:**  
  Managed via `.env` and `.env.example`.

- **Dependencies:**  
  Managed with Poetry ([pyproject.toml](pyproject.toml)).  
  Key dependencies: `crewai`, `fastapi`, `uvicorn`, `python-dotenv`, `humps`, `decouple`.

---

## Usage

### Installation

```sh
python setup.py     ✅ One step setup!
```

### Running the Application 
```sh
poetry run python [app.py]
```
### Running the Crew Locally
```sh
poetry run run_crew
```
### Testing
```sh
poetry run pytest
```

## Extending the Project

- **Add new crews:**  
  Place new crew classes in the `src/crews/` directory. The factory will auto-discover and register them.

- **Add new agents/tasks:**  
  Update the YAML config files in `src/ci_to_lara_crew/config/`.

- **Add new tools:**  
  Implement them in `src/ci_to_lara_crew/tools/` and reference them in agent configs.

## License

This project is licensed under the terms of the [`LICENSE`](LICENSE) file.

## Authors

- Taj (tajulislamj200@gmail.com)

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)