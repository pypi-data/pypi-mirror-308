import os
import sys
import argparse
import shutil
from jinja2 import Environment, FileSystemLoader
import subprocess

# get python version
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"


def write_file(dir, name, content):
    with open(os.path.join(dir, name), "w") as f:
        f.write(content)


def get_template(name, template_dir):
    env = Environment(loader=FileSystemLoader(template_dir))
    return env.get_template(name)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Create a new fastapi project.")
    parser.add_argument('-n', "--name", help="The name of the project.")
    parser.add_argument(
        '-p',
        "--poetry", action="store_true", help="Use poetry for managing dependencies."
    )
    parser.add_argument(
        '-i',
        "--install",
        action="store_true",
        help="Install the dependencies after creating the project.",
    )
    parser.add_argument(
        '-v',
        "--version", action="version", version=f"%(prog)s {get_version()}"
    )
    return parser.parse_args()


def create_pyproject_toml(name, template_dir):
    template = get_template("pyproject_template.toml", template_dir)
    output = template.render(name=name, py_version=py_version)
    write_file(name, "pyproject.toml", output)


def create_dockerfile_template(name, template_dir):
    template = get_template("Dockerfile_template", template_dir)
    output = template.render(name=name)
    write_file(name, "Dockerfile", output)


def create_readme(name, template_dir):
    template = get_template("README_template.md", template_dir)
    output = template.render(name=name)
    write_file(name, "README.md", output)


def create_github_template(name, template_dir):
    shutil.copytree(
        os.path.join(template_dir, "github_template"), os.path.join(name, ".github")
    )


def create_gitignore(name, template_dir):
    template = get_template(".gitignore_template", template_dir)
    output = template.render()
    write_file(name, ".gitignore", output)


def create_src(args, template_dir):
    shutil.copytree(
        os.path.join(template_dir, "src_template"), os.path.join(args.name, "src")
    )


def create_tests(args, template_dir):
    shutil.copytree(
        os.path.join(template_dir, "tests_template"), os.path.join(args.name, "tests")
    )
    template = get_template("pytest_template.ini", template_dir)
    write_file(args.name, "pytest.ini", template.render())


def create_conf(args, template_dir):
    shutil.copytree(
        os.path.join(template_dir, "confs_template"), os.path.join(args.name, "confs")
    )


def create_project_settings(args, template_dir):
    name = args.name
    template_dir = os.path.join(template_dir, "poetry") if args.poetry else template_dir
    create_pyproject_toml(name, template_dir)
    create_dockerfile_template(name, template_dir)
    create_readme(name, template_dir)

    if not args.poetry:
        # pip
        template = get_template("requirements_template.txt", template_dir)
        write_file(name, "requirements.txt", template.render())
    else:
        # poetry
        template = get_template("poetry_template.toml", template_dir)
        write_file(name, "poetry.toml", template.render(name=name))


def create_main(args):
    # Check Python version
    if sys.version_info >= (3, 10):
        import importlib.resources

        if importlib.resources.is_resource("src", "templates"):
            with importlib.resources.path("src", "templates") as template_dir:
                template_dir = str(template_dir)
        else:
            template_dir = str(importlib.resources.files("src").joinpath("templates"))
    else:
        import importlib_resources

        template_dir = str(importlib_resources.files("src").joinpath("templates"))

    if not os.path.isdir(template_dir):
        template_dir = os.path.join(template_dir, "templates")
    os.makedirs(args.name, exist_ok=True)

    create_gitignore(args.name, template_dir)
    create_src(args, template_dir)
    create_tests(args, template_dir)
    create_conf(args, template_dir)
    create_github_template(args.name, template_dir)
    create_project_settings(args, template_dir)

def get_version():
    import importlib.resources

    if importlib.resources.is_resource("src", "version.py"):
        with importlib.resources.path("src", "version.py") as f:
            version_path = str(f)
            with open(version_path, "r") as f:
                return f.readline().strip()


def install(args):
    if args.poetry:
        subprocess.run(
            f"cd {args.name} && poetry env use python{py_version} && poetry install",
            shell=True,
            check=True,
        )

    else:
        subprocess.run(
            f"cd {args.name} && python{py_version} -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt",
            shell=True,
            check=True,
        )


def post_install(args):
    if args.poetry:
        subprocess.run(
            f"cd {args.name} && poetry run ruff format && poetry run ruff check --fix",
            shell=True,
            check=True,
        )
    else:
        subprocess.run(
            f"cd {args.name} && . .venv/bin/activate && ruff format && ruff check --fix",
            shell=True,
            check=True,
        )


def init_git(args):
    os.system(f"cd {args.name} && git init")


def main():
    args = parse_arguments()

    if not args.name:
        print("Please provide a name for the project with --name.")
        exit(1)

    create_main(args)

    if args.install:
        install(args)
        post_install(args)

    init_git(args)

    print("\nProject created successfully.")


if __name__ == "__main__":
    main()
