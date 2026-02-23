# [Project Name]

## Description
<!-- Provide a brief and clear description of what this project does and what problem it solves. -->
This project is an implementation based on the **Gemini Agent Framework**, designed to...

## Prerequisites

- **Python 3.10+**
- **Conda** (Recommended for environment management)
- **API Key** (Configured in `.env`)

## Project Initialization (From Template)

To start a new development based on this framework:

1.  **Clone the template:**
    ```bash
    git clone <REPOSITORY_URL> <NEW_PROJECT_NAME>
    cd <NEW_PROJECT_NAME>
    ```

2.  **Run automatic configuration:**
    This script creates the Conda environment, installs dependencies, and initializes the project.
    ```bash
    bash setup.sh
    ```

3.  **Configure credentials:**
    Edit the generated `.env` file and add your API Keys.

4.  **Activate environment:**
    To start working in future sessions:
    ```bash
    conda activate agent_env
    ```

## Usage

<!-- Instructions on how to run the project or interact with the agent -->
To start the main flow:
```bash
# Example command
python execution/run_agent.py
```

## Agent Architecture
This project uses a 3-layer architecture (Directives, Orchestration, Execution). For technical details on how to operate or extend the agent, consult:

- [Agent Instructions](.gemini/instructions.md)
- [Framework and Philosophy](.gemini/AGENT_FRAMEWORK.md)

## Development Tools
This framework includes tools to facilitate common tasks:

- **`init_project.py`**: Script to clean and configure a new project from this template.
- **`create_new_directive.yaml`**: Directive to automatically generate the skeleton of new directives.
- **`update_template.yaml`**: Directive to bring updates from the original template repository.
- **`deploy_to_github.yaml`**: Automates the git add/commit/push flow to report progress.

## Reporting Progress (Git)
To save your work and upload it to GitHub, you can use the included deployment tool:

1.  **First upload (if history was reset):**
    ```bash
    python execution/deploy_to_github.py --message "Initial delivery" --remote <YOUR_REPO_URL>
    ```

2.  **Daily progress:**
    ```bash
    python execution/deploy_to_github.py --message "Implementing function X"
    ```

## Maintenance and Contribution
If you wish to propose changes or improvements, consult the [Contribution Guide](CONTRIBUTING.md).

To keep this project updated with the original template, you can use the directive `directives/update_template.yaml`. This tool allows the agent to fetch the latest changes from the base repository and merge them with your current work.

## License
This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.