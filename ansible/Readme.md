# Ansible playbooks

Initial hint: Make sure you have Ansible configured for human-readable output (`human-readable-output.yaml`). This is automated if Ansible was installed with `quickstart.sh`.

## Configuration

### Project setup

In `group_vars/all.yaml`, change `project_name` and `server_git_url`

### Servers setup

In `inventory.yaml` add each server as an entry in `all.children.remote.hosts`

## Requirements

- [Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). Currently requires Ansible 2.8
- Run `ansible-galaxy install -r requirements.yaml` to install other requirements.

## Usage

### Deploy and update

The two most used tasks have shortcuts.

To deploy to a server, run:
```sh
ansible/deploy.sh [host-or-group]
```
with host-or-group from inventory. If not specified, it targets the `remote` group.

Example: `ansible/deploy.sh development`

To update only:
```sh
ansible/update.sh [host-or-group]
```

### Other scripts

To avoid having too many files in this folder, they were placed inside `playbooks`. They are executed with the `ansible-playbook` command. In addition to the path to the playbook, two more arguments should be used:
- An inventory file. Available servers are stored in `inventory.yaml`. Specify it with `-i inventory.yaml`.
- A subset of the available servers. Use `-l` followed by the name of the server as declared in inventory. (It can also be a list of hosts/groups separated with commas)

For example, to backup the database of the production server, run:
```sh
ansible-playbook -i inventory.yaml -l production playbooks/backup-db.yaml
```

### Working directory

Except for the shortcut scripts, please run Ansible from this directory. It can also be run from other ones, but:
- yaml files require a path
- some tasks use `dirname $PWD` to get the path to the project in localhost

### Quickstart

Because the deploy needs to run the quickstart script, it was converted to an Ansible role. So `quickstart.sh` now installs the requirements and runs only the quickstart role. Some variables are set in `inventory.yaml` to make it work.

### DB

![backup and other operations diagram](backup-diagram.png)

- `backup-db` works as in Fabric.
- `download-db` always takes a new backup and downloads that (if you want to download a previous one, just use `scp`).
- `import-db` by default imports a fresh backup. You can specify a local dump file in the `local_dump` variable (example: `ansible-playbook ... --limit localhost playbooks/import-db.yaml -e local_dump=staging/2019-08-22.dump`).
- `export-db` can be used in two modes:
    - Export local dump to *host_B*: `ansible-playbook ... --limit host_B playbooks/export-db.yaml -e local_dump=staging/2019-08-22.dump`
    - Export remote dump from *host_A* to *host_B*: `ansible-playbook ... --limit host_A,host_B playbooks/export-db.yaml`

Note that the dumps are inside the `playbooks` folder, but paths are relative to it, not `cwd`.

### Media

Same as DB, but replace `local_dump` with `local_archive`

By default previous media files are preserved (like in Fabric). Add `-e delete_previous=yes` to delete them.

### Project helpers

- `run-django-command`: specify the Django command to be run in the variable `django_command`
- `validate-deployment`: runs tests.
- `service-logs`: shows systemd Django service log.
- `migrate-db`: runs Django migrations.
- `reset-db`: resets DB to initial state. `local_settings` must have `DEBUG = True`.

#### Services

Actions are grouped in playbooks and services are tagged. For example, to restart nginx only, run `ansible-playbook ... --tags nginx playbooks/restart-services.yaml`. There's also a `project` tag that targets both gunicorn and nginx.

Available actions are `install-services`, `start-services`, `restart-services`, `stop-services` and `enable-services`.

## Notes

- DB is automatically backed up when pulling changes. Also, DB/Media are automatically backed up on target machine when using `export`. If they are too big, comment those tasks, and make sure to delete old backups.
- Remote DB dumps are assumed to be stored in `~/db_dumps/`, and Media archives in `~`
- Backup/restore Media doesn't support `relative_path`
- Media backed up from S3 in a `.tar` loses its metadata.

## External databases

There's support for external databases not running in the server (like RDS) but some manual setup is required. For example, a DigitalOcean managed database comes only with a `defaultdb` database. You must:

- Create a database called `postgres` (the default of the [`maintenance_db` parameter](https://docs.ansible.com/ansible/latest/modules/postgresql_db_module.html#parameters), and also to be able to use `psql`).
- Set DB connection parameters in `local_settings.py`. Either clone the repository and create local_settings from the default file before running deploy (note: remember to manually set DEBUG to False), or let the deploy succeed with a local DB, and then edit local_settings and run deploy again.

## Testing

Tests of Ansible scripts are made with [Molecule](https://molecule.readthedocs.io), which creates a Vagrant VM (with Ubuntu 18.04 by default). There are two test scenarios:

- `deploy`: deploys the app in the VM, and tests that the home page has no broken links.
- `quickstart`: runs quickstart in the VM, and tests that Django and Webpack (in development mode) return 200. (Note: this tests with files you currently have in your repository folder)

### Setup

- Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads#Debian-basedLinuxdistributions)
- `pip install "molecule[vagrant]>=2.22" "ansible-lint>=4.2.0"`

### Running

From this directory, run:
```sh
molecule test -s <scenario>
```
where `<scenario>` is either `deploy` or `quickstart`

#### Choosing distro to test

Set it in the `MOLECULE_DISTRO` variable when calling `molecule`. By default it is `ubuntu/bionic64` (as specified in `platforms` in `molecule.yml`). To use another Vagrant box, for example CentOS 7, run:
```sh
MOLECULE_DISTRO=centos/7 molecule test -s <scenario>
```

To change distro when the instance is already created, run `MOLECULE_DISTRO=<distro> molecule destroy -s <scenario>`

> Note: if you run `destroy` with the wrong `MOLECULE_DISTRO` set, the VM won't be deleted but its metadata stored by Molecule will, so it can't be deleted by Molecule anymore. To delete it manually: open the VirtualBox GUI (Oracle VM VirtualBox Manager), right click it in the list, "Close", "Power Off", right click, "Remove...", "Delete all files".

#### Debugging

VMs are deleted after a failed `molecule test`. Use `molecule converge` to avoid that (you can also use `molecule test --destroy=never` but it runs more steps). You can then examine the VM with `molecule login`

### Notes

Tests use Vagrant instead of Docker (which is more common) because the second one is not very well suited to using `systemctl` and having a non-root user.

Multiple distro handling method is taken from [here](https://www.jeffgeerling.com/blog/2018/testing-your-ansible-roles-molecule).

Using molecule for the quickstart scenario is slightly overkill, but it was already used to test deploy, and it's an easy way to create and destroy Vagrant boxes. The converge playbook is run with Ansible, which runs quickstart, which installs another Ansible, and runs the deploy playbook inside Vagrant.

TODO: test quickstart in OSX

### Linting everything (TODO)

`ansible-lint` has an [undocumented feature](https://github.com/ansible/ansible-lint/pull/615): running it without supplying playbooks lints all playbooks in the git repository. But `molecule lint` always supplies the `converge` playbook, so that feature cannot be triggered without modifications. TODO: scenarios that test and lint backup/restore playbooks.
