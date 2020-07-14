#!/bin/env python3
import os, sys
import argparse
try:
    import docker
except ImportError:
    print("Error: The 'docker' module isn't installed.", file=sys.stderr)
    exit(1)

from utils.kparser import parser
from utils.docker import split_image
from kdeploy.core import KDeploy
from utils.std import eprint

print("""
K-Deploy (Kuick Deploy)
Developed by Kyriakos Giannakis (kgiannakis@kgiannakis.me). Blame him should anything happen (or don't)!

""")

def stop_container(kd, name, raise_exc=True):
    running_containers = kd.get_running_containers_by_name()
    if name not in running_containers:
        if not raise_exc:
            return
        raise ValueError("Container '{}' not running.".format(name))
    print("Stopping old container.")
    killed = kd.check_and_stop(running_containers[name])
    print("Killed container after not responding." if killed else "Container stopped.")

def rm_container(kd, name):
    all_containers = kd.get_all_containers_by_name()
    if name in all_containers:
        c_to_rm = all_containers[name]
        c_to_rm.remove()
        print("Old container removed.")

def pull_image(kd, image):
    print("Pulling {}".format(image))
    try:
        kd.pull_image(image)
    except docker.errors.ImageNotFound:
        eprint("Error: Image not found. Either the image doesn't exist or you need to 'docker login' first.")
        exit(1)

client = docker.from_env()
kd = KDeploy(client)

if parser.mode not in ['up', 'down']:
    raise ValueError("Invalid mode. Valid options are 'up', 'down'.")

name = parser.name.lstrip()
running_containers = kd.get_running_containers_by_name()


if parser.mode == "up":
    if not parser.image or not parser.name:
        raise ValueError("Please give a valid image and container name.")
    image = parser.image.lstrip()

    pull_image(kd, image)
    stop_container(kd, name, False)
    rm_container(kd, name)

    print("Creating new container...")
    extra_args = {}
    if parser.volumes:
        extra_args["volumes"] = parser.volumes.split(" ")[1:]
    if parser.network:
        extra_args["network"] = parser.network.lstrip()
    if parser.ports:
        extra_args["ports"] = parser.ports.split(" ")[1:]

    c_new = kd.create(image, name, \
                    **extra_args)
    print("Container created successfully: ")
    print(c_new.id)
else:
    stop_container(kd, name)
    rm_container(kd, name)