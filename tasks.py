from invoke import task


@task
def run_dev(c):
    c.run("FLASK_ENV=development flask --app src.flaskr run --debug")


# ON PROD WE WILL SHOULD TO USE WSGI server
@task
def run_prod(c):
    c.run("FLASK_ENV=production flask --app src.flaskr run")


@task
def run_test(c):
    c.run("PYTHONPATH=src FLASK_ENV=testing pytest src/tests")
