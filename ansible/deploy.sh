#!/bin/bash
set -e
cd "$(dirname "$0")"

if [[ -n $1 ]]; then
  limit="$1"
else
  limit="remote"
fi

if [[ "$(basename "$0")" == "update.sh" ]]; then    # have you ever seen busybox?
  tags=(--tags update)
fi

ansible-playbook --inventory inventory.yaml --limit "$limit" "${tags[@]}" playbooks/deploy.yaml
