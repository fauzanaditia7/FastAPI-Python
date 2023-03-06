import subprocess

subprocess.run([
    "uvicorn", "main:app", "--port", "5000", "--reload"
])