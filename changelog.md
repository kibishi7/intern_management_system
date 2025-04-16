# Changelog

## [1.0.3] - 16-04-2025

### Added

- added changelog.md

## [1.0.2] - 16-04-2025

### Added

- added requirements.txt

## [1.0.1] - 16-04-2025

### Removed

- tasks: Assign a task to an intern from main.py

### Changed

- changes in return type from actual return type to "Godwin was here"

## [1.0.0] - 15-04-2025

### Added
- **Database Models**:
  - `Intern` model with fields: `id`, `name`, `email`, `tasks`, and `attendances`.
  - `Attendance` model with fields: `id`, `intern_id`, `date`, `time_in`, and `time_out`.
  - `Task` model with fields: `id`, `title`, `description`, `intern_id`, and `completed`.

- **Schemas**:
  - Pydantic models for `Intern`, `Attendance`, and `Task` with `Base`, `Create`, and response models.

- **CRUD Operations**:
  - Functions to create, retrieve, and update `Intern`, `Attendance`, and `Task` records in the database.

- **API Endpoints**:
  - `POST /interns/`: Create a new intern.
  - `POST /interns/{intern_id}/time_in`: Log time-in for an intern.
  - `POST /interns/{intern_id}/time_out`: Log time-out for an intern.
  - `GET /interns/{intern_id}/attendance`: Retrieve attendance summary for an intern.
  - `POST /tasks/`: Assign a task to an intern.

- **Database Configuration**:
  - SQLite database setup with SQLAlchemy.

- **Middleware**:
  - CORS middleware to allow cross-origin requests.
  - HTTP request logging middleware.

- **SQLite Shell Commands**:
  - A `sqlite_shell_commands.txt` file with instructions to inspect the database.

- **Dependencies**:
  - Added `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, and `python-multipart` to `requirement.txt`.



