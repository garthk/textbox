import nox


@nox.session(reuse_venv=True)
def fmt(session: nox.Session) -> None:
    session.install("black", "ruff")
    session.run("ruff", "check", "--fix-only", ".")
    session.run("black", ".")


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    session.install("black", "mypy", "nox", "ruff")
    session.run("ruff", "check", ".")
    session.run("mypy", "--strict")
    session.run("black", "--check", ".")


@nox.session(reuse_venv=True)
def test(session: nox.Session) -> None:
    session.install("pytest", ".")
    session.run("pytest")


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    session.install(".[docs]")
    session.run(
        "sphinx-build",
        "-n",
        "-b",
        "html",
        "-d",
        "docs/_build/doctrees",
        "docs",
        "docs/_build/html",
    )
