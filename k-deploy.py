#!/usr/bin/env python3
from utils.std import eprint
try:
    import docker
except ImportError:
    eprint("Error: The 'docker' module isn't installed.")
    exit(1)

from utils.kparser import parser
from utils.docker import parse_env, parse_volumes, parse_ports,\
     parse_restart
from kdeploy.core import KDeploy

print("""
K-Deploy (Kuick Deploy)
Developed by Kyriakos Giannakis (kgiannakis@kgiannakis.me). Blame him should \
anything happen (or don't)!
Version 0.1.5
""")


def stop_container(kd, name, raise_exc=True):
    running_containers = kd.get_running_containers_by_name()
    if name not in running_containers:
        if not raise_exc:
            return False
        raise ValueError("Container '{}' not running.".format(name))
    print("Stopping old container.")
    killed = kd.check_and_stop(running_containers[name])
    print(
        "Killed container after not responding." if killed
        else "Container stopped."
        )
    return True


def rm_container(kd, name):
    all_containers = kd.get_all_containers_by_name()
    if name in all_containers:
        c_to_rm = all_containers[name]
        c_to_rm.remove()
        print("Old container removed.")


def pull_image(kd, image, pull=False, debug=False):
    if not pull:
        if kd.is_image_present(image) is not None:
            print("Using already existing image.")
            return
        print("Image {} not found locally.".format(image))
    print("Pulling {}".format(image))
    try:
        kd.pull_image(image)
    except docker.errors.ImageNotFound:
        eprint(
            "Error: Image not found. Either the image doesn't exist or you \
            need to 'docker login' first."
            )
        exit(1)
    except docker.errors.APIError as e:
        eprint(
            "An error has occured. Have you tried logging in to the registry? (docker login ...)"
        )
        if debug:
            print(e)
        exit(1)


client = docker.from_env()
kd = KDeploy(client)

extra_args = {}
if parser.volumes:
    extra_args["volumes"] = parse_volumes(
        parser.volumes.split(" "),
        parser.debug
        )

if parser.network:
    if parser.debug:
        print(
            "Container will join network '{}'"
            .format(parser.network.lstrip())
            )
    extra_args["network"] = parser.network.lstrip()
if parser.ports:
    extra_args["ports"] = parse_ports(parser.ports.split(" "), parser.debug)
if parser.env:
    extra_args["environment"] = parse_env(parser.env)
if parser.restart:
    extra_args["restart_policy"] = parse_restart(parser.restart.lstrip())
if parser.command:
    extra_args["command"] = parser.command.strip()
    if parser.debug:
        print(
            "Executing the following command:\n{}"
            .format(extra_args["command"])
        )

if parser.mode not in ['up', 'down']:
    raise ValueError("Invalid mode. Valid options are 'up', 'down'.")

name = parser.name.lstrip()
running_containers = kd.get_running_containers_by_name()


if parser.mode == "up":
    if not parser.image or not parser.name:
        raise ValueError("Please give a valid image and container name.")
    image = parser.image.lstrip()
    pull_image(kd, image, pull=parser.pull, debug=parser.debug)
    stop_container(kd, name, False)
    rm_container(kd, name)

    print("Creating new container...")

    c_new = kd.create(
        image, name, **extra_args
        )
    print("Container created successfully: ")
    print(c_new.id)
else:
    stop_container(kd, name, False)
    rm_container(kd, name)
