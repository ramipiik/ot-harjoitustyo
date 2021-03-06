from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/main.py")

@task
def start_gui(ctx):
    ctx.run("python3 src/main_gui.py")

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def initiate_db(ctx):
    ctx.run("python3 src/initiate_db.py")
