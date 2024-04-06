#!/usr/bin/env python3
"""
TODO:
- setting remote dev server
"""
import subprocess
from sys import argv
from typing import Union

CONTAINER_TYPES = [
    "base",
    "python"
]

CONTAINER_NAMES = {
    "base": "devtainer_base",
    "python": "devtainer_python"
}


def parse_args(args: list[str]):
    # would be nice to use typer or click, but i want to avoid deps
    if len(argv) > 1:
        command = argv[1]
    else:
        command = None

    if len(argv) > 2:
        args_out = argv[2:]
    else:
        args_out = None

    return command, args_out


def build_container(args: Union[list[str], None]) -> None:
    if args:
        container_type = args[0]
    else:
        print("Not enough arguments provided")
        return

    # check if the commands should be run remote or locally
    remote_str = ""
    if "--remote" in args:
        remote_flag_index = args.index("--remote")
        remote_str = "ssh " + args[remote_flag_index+1] + " "

    container_name = f"{CONTAINER_NAMES[container_type]}"

    if container_type in CONTAINER_TYPES:
        # build the base container
        print("Building base container first")
        docker_build_str = f"{remote_str}docker build -t {CONTAINER_NAMES['base']} base/"
        subprocess.run(docker_build_str.split())

        # build the specified container
        print(f"Building container type: {container_type}")
        docker_build_str = f"{remote_str}docker build -t {container_name} {container_type}/"
        subprocess.run(docker_build_str.split())

    else:
        container_type_string = '\n'.join(CONTAINER_TYPES)
        print(f"Not a valid container type: {container_type}. Available container types are:\n{container_type_string}")


def open_container(args: Union[list[str], None]) -> None:
    if args:
        container_type = args[0]
    else:
        print("Not enough arguments provided")
        return

    # did we name the container something else?
    if "--name" in args:
        name_index = args.index("--name")
        container_type = args[name_index+1]

    # TODO: check and see if the container was running, error if not
    # TODO: check if we even have a container named what it is?
    print(f"Running container type: {container_type}")
    docker_run_str = f"docker exec -w /root -it {container_type} zsh"
    subprocess.run(docker_run_str.split())


def run_container(args: Union[list[str], None]) -> None:
    if args:
        container_type = args[0]
    else:
        print("Not enough arguments provided")
        return

    # did we name the container something else?
    container_name = f"{CONTAINER_NAMES[container_type]}"
    if "--name" in args:
        name_index = args.index("--name")
        container_name = args[name_index+1]

    if container_type in CONTAINER_TYPES:
        # TODO: check and see if the container was already running
        print(f"Running container type: {container_type}")
        docker_run_str = f"docker run -d --name {container_name} {CONTAINER_NAMES[container_type]}"
        subprocess.run(docker_run_str.split())

    else:
        container_type_string = '\n'.join(CONTAINER_TYPES)
        print(f"Not a valid container type: {container_type}. Available container types are:\n{container_type_string}")


if __name__ == "__main__":
    help_str = """devtainers.py
    Commands:
        build - build a specific devtainer
        list - list the available devtainers
        run - run a container
        open - open a shell to a container
    """
    command, args = parse_args(argv)

    command_funcs = {
        "build": build_container,
        "run": run_container,
        "open": open_container,
    }

    if command and command in command_funcs:
        command_funcs[command](args)
    else:
        print(help_str)
