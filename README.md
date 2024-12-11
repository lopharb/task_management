# task_management

Simple web application for cooperative task management.

### Repo structure

```
.
├── alembic                  # Directory for Alembic migrations
│   ├── env.py               # Alembic environment setup script
│   ├── README               # Documentation for Alembic migrations
│   ├── script.py.mako       # Template for Alembic migration scripts
│   └── versions             # Directory to store individual migration scripts
├── alembic.ini              # Configuration file for Alembic migrations
├── app                      # Main application directory
│   ├── api                  # API module
│   │   ├── __init__.py      # Initializes the API module
│   │   └── routers          # Route handlers for specific entities
│   │       ├── company_routers.py   # Routes for managing companies
│   │       ├── __init__.py          # Initializes the routers module
│   │       ├── role_routers.py      # Routes for managing roles
│   │       ├── task_routers.py      # Routes for managing tasks
│   │       ├── user_routers.py      # Routes for managing users
│   │       └── worklog_routers.py   # Routes for managing worklogs
│   ├── frontend             # Vue.js frontend application
│   │   └── tm_frontend      # Vue.js project files
│   │       ├── babel.config.js      # Babel configuration for Vue.js
│   │       ├── jsconfig.json        # Configuration for JavaScript project setup
│   │       ├── package.json         # Dependencies and scripts for the Vue.js app
│   │       ├── package-lock.json    # Lock file for Vue.js dependencies
│   │       ├── public               # Static assets for the frontend
│   │       │   ├── favicon.ico      # Default icon for the app
│   │       │   └── index.html       # HTML entry point for the Vue.js app
│   │       ├── README.md            # Documentation for the Vue.js app
│   │       ├── src                  # Source files for the Vue.js app
│   │       │   ├── App.vue          # Main Vue.js component
│   │       │   ├── assets           # Static assets like images
│   │       │   ├── components       # Vue.js components for specific features
│   │       │   ├── main.js          # Entry point for initializing Vue.js app
│   │       │   ├── router           # Vue.js routing setup
│   │       │   │   └── index.js     # Defines routes for the Vue.js app
│   │       │   └── services         # Services for API communication
│   │       │       └── api.js       # API service for backend communication
│   │       └── vue.config.js        # Vue.js build configuration
│   ├── __init__.py          # Initializes the application module
│   ├── model                # Database models using SQLAlchemy
│   │   ├── base.py          # Base class for SQLAlchemy models
│   │   ├── __init__.py      # Initializes the model module
│   │   ├── task.py          # Database model for tasks
│   │   └── user.py          # Database model for users
│   ├── schemas              # Pydantic models for data validation
│   │   ├── company.py       # Schema for company data
│   │   ├── __init__.py      # Initializes the schemas module
│   │   ├── role.py          # Schema for role data
│   │   ├── task.py          # Schema for task data
│   │   ├── user.py          # Schema for user data
│   │   └── worklog.py       # Schema for worklog data
│   └── utils                # Utility functions and helpers
│       ├── db_utils.py      # Functions for database interaction
│       ├── __init__.py      # Initializes the utils module
│       ├── task_handler.py  # Logic for task-related operations
│       └── user_handler.py  # Logic for user-related operations
├── main.py                  # Entry point for running the FastAPI application
├── package.json             # Lists project dependencies and scripts for Node.js
├── package-lock.json        # Lock file ensuring consistent Node.js dependency versions
├── README.md                # Documentation for the project
└── run.fish                 # Script to run the application using Fish shell
```

### Usage

Install python dependencies:

```bash
pip install -r requirements.txt
```

Install Node.js dependencies:

```bash
npm install
```

Run the application:

- Using `fish` terminal:

```bash
sudo ./run.fish
```

- Using bash:

```bash
sudo ./run.sh
```
