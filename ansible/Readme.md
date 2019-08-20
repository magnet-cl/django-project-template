# Ansible playbooks

## Configuration

### Project setup

In `group_vars/all.yaml`, change `project_name` and `server_git_url`

### Servers setup

In `inventory.yaml` add each server as an entry in `all.children.remote.hosts`

## Requirements

- [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). Currently requires Ansible 2.8
- Run `ansible-galaxy install -r requirements.yaml` to install other requirements.
## Usage

To setup or update a server, run:
```sh
ansible-playbook -i inventory.yaml -l <host_or_group> deploy.yaml
```
with host_or_group from inventory. (It can also be run from another directories, but requires paths for yaml files)

### Quickstart

Because the deploy needs to run the quickstart script, it was converted to an Ansible role. So `quickstart.sh` now installs the requirements and runs only the quickstart role. Some variables are set in `inventory.yaml` to make it work.
