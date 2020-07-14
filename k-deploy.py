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

client = docker.from_env()
kd = KDeploy(client)
print("Pulling {}".format(parser.image))
try:
    kd.pull_image(parser.image)
except docker.errors.ImageNotFound:
    eprint("Error: Image not found. Either the image doesn't exist or you need to 'docker login' first.")
    exit(1)

running_containers = kd.get_running_containers_by_name()

if parser.name in running_containers:
    print("Stopping old container.")
    killed = kd.check_and_stop(running_containers[parser.name])
    if killed: 
        print("Killed container after not responding.")

all_containers = kd.get_all_containers_by_name()
if parser.name in all_containers:
    c_to_rm = all_containers[parser.name]
    c_to_rm.remove()
    print("Old container removed.")

print("Creating new container...")
extra_args = {}
if parser.volumes:
    extra_args["volumes"] = parser.volumes.split(" ")[1:]
if parser.network:
    extra_args["network"] = parser.network
if parser.ports:
    extra_args["ports"] = parser.ports.split(" ")[1:]

c_new = kd.create(parser.image, parser.name, \
                **extra_args)
print("Container created successfully: ")
print(c_new.id)