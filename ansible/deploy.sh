#!/bin/bash
set -e
cd "$(dirname "$0")"

while [[ $# -gt 0 ]]; do
  case $1 in
    -f|--force)
      force=1
      ;;
    *)
      limit=$1
      ;;
  esac
  shift
done

if [[ "$(basename "$0")" == "update.sh" ]]; then    # have you ever seen busybox?
  tags="--tags update"
fi

if [[ "$force" = "1" ]]; then
  skip_tags="--skip-tags validate-deployment"
fi

# shellcheck disable=SC2086
ansible-playbook --inventory inventory.yaml --limit "${limit:-remote}" $tags $skip_tags playbooks/deploy.yaml
