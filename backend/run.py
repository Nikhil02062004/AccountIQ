import os
import sys

# Ensure repository root is on sys.path and PYTHONPATH so 'backend' package is resolvable
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set PYTHONPATH in os.environ so uvicorn reloader subprocess inherits it
existing_pythonpath = os.environ.get("PYTHONPATH", "")
if project_root not in existing_pythonpath:
    os.environ["PYTHONPATH"] = f"{project_root}{os.pathsep}{existing_pythonpath}" if existing_pythonpath else project_root

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

