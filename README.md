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