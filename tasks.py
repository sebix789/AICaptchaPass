from invoke import task
import os

def env_prefix(env_vars):
    # Windows
    if os.name == "nt":
        return " ".join([f"set {key}={value} &&" for key, value in env_vars.items()])
    # macOS/Linux
    else:
        return " ".join([f"{key}={value}" for key, value in env_vars.items()])

@task
def run_dev(c):
    env = env_prefix({"FLASK_ENV": "development"})
    print(env)
    c.run(f"{env} flask --app src.flaskr run --debug")

# ON PROD WE WILL SHOULD TO USE WSGI server
@task
def run_prod(c):
    env = env_prefix({"FLASK_ENV": "production"})
    c.run(f"{env} flask --app src.flaskr run")

@task
def run_test(c):
    env = env_prefix({"PYTHONPATH": "src", "FLASK_ENV": "testing"})
    c.run(f"{env} pytest src/tests")

@task
def initial_images(c):
    env = env_prefix({"PYTHONPATH": "src"})
    script_path = os.path.abspath(os.path.join("src", "utils", "functions", "uploadImages.py"))
    print(f"Uruchamianie skryptu: {script_path}")
    c.run(f"{env} python {script_path}")