# SQLMesh CLI Crash Course 

This is a simple repo to learn the SQLMesh CLI.

## Setup

Copy/paste and run directly in your terminal.

```bash
uv python install 3.12
uv venv --python 3.12 --seed # ensures pip is installed
source .venv/bin/activate
uv pip install sqlmesh
source .venv/bin/activate # reactivate the venv to ensure you're using the right installation
sqlmesh plan # In a realistic setup, this governed by a formal CI/CD process
```