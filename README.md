# K-Deploy

## Install:
0. Install the requirements:
```bash
sudo pip3 install -r requirements.txt
```
1. Copy the K-Deploy directory inside `/opt/kdeploy`:
```bash
sudo mkdir /opt/kdeploy
sudo cp -r . /opt/kdeploy
```
2. Change the permissions of k-deploy.py so that it's executable:
```bash
sudo chmod o+x /opt/kdeploy/k-deploy.py
```
3. Link `k-deploy.py` to `/usr/local/bin` in order to be able to execute it from anywhere:
```bash
sudo ln -s /opt/kdeploy/k-deploy.py /usr/local/bin/k-deploy
```

## Usage:

### Argument Syntax:
```bash
k-deploy {mode} {image} {container_name} [extra_args]
```

### Spin up an nginx container:
```bash
k-deploy up nginx:latest some_nginx_container -p 8080:80
```

### Spin up an image located in another registry:
```bash
docker login ...

k-deploy up registry.gitlab.com/someuser/someimage:latest another_container -p 1234:4567
```

When the image gets updated (ie you commit something new and it gets rebuilt and released), you just need to issue the same command as above, followed by the `--pull` argument. K-Deploy will pull the new image, stop the old container (or kill it if it doesn't respond), delete it and spin a new one:

```bash
docker login ...

k-deploy up registry.gitlab.com/someuser/someimage:latest another_container --pull -p 1234:4567
```

### Spin down a container:

```bash
k-deploy stop another_container
```

Or, you can do it using the old fashioned way using `docker stop`. Whatever floats your boat. The only difference is that K-Deploy will `docker rm` the old container.

### Arguments:

- `mode`: Operational mode. Can be either `up` or `down`.
- `image`: Image name. A tag can be specified too. (**WARNING**: Does NOT support registries binded on non-default ports yet.)
- `container_name`: Self explanatory.
- `--pull`: Always pull the latest image from the registry. By default, it looks for an image locally, and only if it isn't located, it tries to pull it.
- `-p <host_side>:<container_side>`: Bind a port from the container to the host. Example: `-p 8080:80` will bind port 80 from the container to the host's port 8080. Add more with spaces in between (eg: `8080:80 2043:443`).
- `-v <host_side_directory>:<container_side_directory>:<mode>`: Bind a volume. You can ommit the mode directive (it'll be set to `rw`). Add more with spaces in between (same as above).
- `-e <ENV_VAR_NAME>=<content>`: Pass an environment variable to a container. The env name must be `ALL_CAPS`. Add more with spaces in between (same as above).
- `--restart {always|on-failure}`: Restart policy.
- `-n some_network`: Connect the container to a specific network.
- `--debug`: Debug mode. Prints out what's gonna be binded and where.
