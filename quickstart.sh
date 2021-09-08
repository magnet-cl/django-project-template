#!/bin/bash
set -e

green="\033[0;32m"
cyan="\033[0;36m"
yellow="\033[0;33m"
red="\033[0;31m"
default="\033[0m"

### Install Ansible
if [[ "$OSTYPE" == "darwin"* ]]; then
  if ! [[ -f ~/.ansible.cfg ]]; then
    blank_cfg=1
  fi
else
  if ! [[ -f /etc/ansible/ansible.cfg ]]; then
    blank_cfg=1
  fi
fi

if ! command -v ansible >/dev/null; then
  echo -e "${green}Installing Ansible${default}"
  # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

  if [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac OS X
    if ! command -v brew >/dev/null; then
      echo -e "${red}Error: Homebrew is not installed (https://brew.sh/#install)${default}"
      exit 1
    fi

    # Install with Homebrew instead of pip because:
    #  - pip could not be installed
    #  - pip could install Ansible somewhere not in PATH
    brew install ansible

  elif grep --quiet -P '^ID="(centos|rhel)"$' /etc/os-release 2>/dev/null; then
    # CentOS / Red Hat
    if grep --quiet -P '^VERSION_ID="7[\D]' /etc/os-release; then
      # CentOS/RHEL version 7
      sudo yum install -y https://releases.ansible.com/ansible/rpm/release/epel-7-x86_64/ansible-2.9.2-1.el7.ans.noarch.rpm   # hardcoded version :(
    else
      echo -e "${red}Automatic Ansible installation available only for CentOS/RHEL 7."
      echo -e "${cyan}Please install Ansible manually:"
      echo -e "https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#latest-release-via-dnf-or-yum"
      echo -e "$default"
      exit 1
    fi

  else    # Assume Ubuntu
    command -v pip3 >/dev/null || sudo apt-get install -y python3-pip
    sudo -H pip3 install ansible
  fi
fi
# Improvement: upgrade if version is too old


### Mac OS X warning
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo
  echo -e "${yellow}Note: quickstart support on Mac OS X is incomplete, because we don't use it too much, and Python configuration is a mess (https://xkcd.com/1987). So you must manually:"
  #  - Install Homebrew -- already checked above
  # shellcheck disable=SC2016
  echo -e '  - install and configure PostgreSQL. This worked for me: brew install postgresql && brew services start postgresql && createdb $USER'
  echo -e "  - create the Pipenv virtualenv: pipenv --python 3.6    (suggestion: use pyenv)"
  echo -e "$default"
fi


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

if [[ -n "$blank_cfg" ]]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    ansible-playbook playbooks/human-readable-output.yaml
  else
    ansible-playbook $ask_become_pass playbooks/human-readable-output.yaml
  fi
fi
ansible-playbook --inventory inventory.yaml --limit localhost --tags quickstart $ask_become_pass playbooks/deploy.yaml
