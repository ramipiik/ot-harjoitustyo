from invoke import task

@task
def test(ctx):
    print("moi")
    ctx.run("pytest src")

