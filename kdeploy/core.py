from utils.docker import split_image, parse_volumes
import docker
from time import sleep

class KDeploy:
    def __init__(self, docker_client : docker.client.DockerClient):
        self.client = docker_client

    def pull_image(self, image):
        img, tag = split_image(image)
        self.client.images.pull(img, tag)

    def get_running_containers_by_name(self):
        containers = self.client.containers.list()
        return self._map_containers(containers)
    
    def get_all_containers_by_name(self):
        containers = self.client.containers.list(all=True)
        return self._map_containers(containers)

    def _map_containers(self, containers):
        cmap = {}
        for c in containers:
            cmap[c.name] = c
        return cmap

    def send_stop_signal(self, container):
        container.kill(signal="SIGTERM")

    def check_and_stop(self, container):
        self.send_stop_signal(container)
        tries = 1
        while tries <= 5:
            if container.name in self.get_running_containers_by_name():
                tries += 1
                sleep(2)
            else:
                return False
        container.kill()
        return True


    def stop_container(self, container):
        container.stop()

    def create(self, image, name, *args, **kwargs):
        if "volumes" in kwargs:
            kwargs["volumes"] = parse_volumes(kwargs.pop("volumes"))
        return self.client.containers.run(image, name=name, detach=True, **kwargs)