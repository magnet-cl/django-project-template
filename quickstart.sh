#!/bin/bash
set -e

green="\033[0;32m"
cyan="\033[0;36m"
default="\033[0m"

### Install Ansible
if ! command -v ansible >/dev/null; then
  echo -e "${green}Installing Ansible${default}"

  # Improvement: support for other OS
  # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-releases-via-apt-ubuntu
  sudo apt update
  sudo apt install -y software-properties-common
  sudo apt-add-repository -y ppa:ansible/ansible
  sudo apt install -y ansible
fi
# Improvement: upgrade if version is too old


### Install roles and run Ansible
cd "$(dirname "$0")/ansible"

# Without --force it never updates (just warns), but with --force it downloads every time...
ansible-galaxy install -r requirements.yaml

if sudo --non-interactive true 2>/dev/null; then
  # sudo worked without password!
  # Let's hope it will last until Ansible finishes, so don't show the hint.
  : # noop
else
  ask_become_pass="--ask-become-pass"
  echo -e "${green}In ${cyan}BECOME password${green} you have to type your sudo password${default}"
fi

ansible-playbook -i inventory.yaml -l localhost --tags quickstart $ask_become_pass deploy.yaml
