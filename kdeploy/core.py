from utils.docker import split_image
import docker
from time import sleep


class KDeploy:
    def __init__(self, docker_client: docker.client.DockerClient):
        self.client = docker_client

    def get_images_by_name(self):
        im_out = {}
        for im in self.client.images.list():
            try:
                im_out[im.tags[0]] = im
            except IndexError:
                continue
        return im_out

    def get_images_by_digest(self):
        im_out = {}
        for im in self.client.images.list():
            try:
                im_out[im.id] = im
            except IndexError:
                continue
        return im_out

    def is_image_present(self, name):
        images = self.get_images_by_name()
        for k, im in images.items():
            if name in im.tags:
                return im
        return None

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

    def get_networks_by_name(self):
        n_out = {}
        for n in self.client.networks.list():
            n_out[n.name] = n
        return n_out

    def stop_container(self, container):
        container.stop()

    def create(self, image, name, *args, **kwargs):
        if "network" in kwargs:
            if kwargs["network"] not in self.get_networks_by_name():
                raise ValueError(
                            "Error: Container network '{}' does not exist."
                            .format(kwargs["network"])
                            )

        return self.client.containers.run(
            image, name=name, detach=True,
            **kwargs
            )
