OMERO Server
============

[![Build Status](https://travis-ci.org/ome/ansible-role-omero-server.svg)](https://travis-ci.org/ome/ansible-role-omero-server)
[![Ansible Role](https://img.shields.io/ansible/role/41085.svg)](https://galaxy.ansible.com/ome/omero_server/)

Installs and configures OMERO.server.

**Warning:** This defaults to Python 3.
Upgrades from OMERO.server 5.5 Python 2.7 to OMERO.server 5.6+ Python 3.6 are handled.
See [`CHANGES.md`](./CHANGES.md) for details.


Dependencies
------------

A PostgreSQL server is required.



Role Variables
--------------

All variables are optional, see `defaults/main.yml` for the full list

OMERO.server version.
- `omero_server_release`: The OMERO release, e.g. `5.6.0`.
  The default is `present` which will install the latest server if no server is installed, but will not modify an existing server.
  Use `latest` to automatically upgrade when a new version is released.
- `omero_server_python3`: Use Python 3, default `true`

Database connection parameters and initialisation.
- `omero_server_dbhost`: Database host
- `omero_server_dbuser`: Database user
- `omero_server_dbname`: Database name
- `omero_server_dbpassword`: Database password
- `omero_server_rootpassword`: OMERO root password, default `omero`.
  This is only used when initialising a new database.

OMERO.server configuration.
- `omero_server_config_set`: A dictionary of `config-key: value` which will be used for the initial OMERO.server configuration, default empty.
  `value` can be a string, or an object (list, dictionary) that will be automatically converted to quoted JSON.
  Note configuration can also be done pre/post installation using the `server/config` conf.d style directory.

OMERO system user, group, permissions, and data directory.
You may need to change these for in-place imports.
- `omero_server_system_user`: OMERO.server system user, default `omero-server`.
- `omero_server_system_user_manage`: Create or update the OMERO.server system user if necessary, default `True`.
- `omero_server_system_uid`: OMERO system user ID (default automatic)
- `omero_server_system_umask`: OMERO system user umask, may need to be changed for in-place imports
- `omero_server_system_managedrepo_group`: OMERO system group for the `ManagedRepository`
- `omero_server_datadir_mode`: Permissions for OMERO data directories apart from `ManagedRepository`
- `omero_server_datadir_managedrepo_mode`: Permissions for OMERO `ManagedRepository`
- `omero_server_datadir`: OMERO data directory, default `/OMERO`
- `omero_server_datadir_managedrepo`: OMERO ManagedRepository directory

OMERO.server systemd configuration.
- `omero_server_systemd_setup`: Create and start the `omero-server` systemd service, default `True`
- `omero_server_systemd_limit_nofile`: Systemd limit for number of open files (default ignore)
- `omero_server_systemd_after`: A list of strings with additional service names to appear in systemd unit file "After" statements. Default empty/none.
- `omero_server_systemd_requires`: A list of strings with additional service names to appear in systemd unit file "Requires" statements. Default empty/none.
- `omero_server_systemd_environment`: Dictionary of additional environment variables.

Python virtualenv
- `omero_server_virtualenv`: Use a virtualenv for most OMERO.server dependencies, ignored on Python 3 (a virtualenv is always used).
- `omero_server_python_addons`: List of additional Python packages to be installed into virtualenv.
  Alternatively you can install packages into `/opt/omero/server/venv` independently from this role.
  Requires `omero_server_virtualenv: True`.

Backups
- `omero_server_database_backupdir`: Dump the OMERO database to this directory before upgrading, default empty (disabled)


Configuring OMERO.server
------------------------

This role regenerates the OMERO configuration file using the configuration files and helper script in `/opt/omero/server/config`.
`omero_server_config_set` can be used for simple configurations, for anything more complex consider creating one or more configuration files under: `/opt/omero/server/config/` with the extension `.omero`.

Manual configuration changes (`omero config ...`) will be lost following a restart of `omero-server` with systemd, you can disable this by setting `omero_server_always_reset_config: false`.
Manual configuration changes will never be copied during an upgrade.

See https://github.com/ome/design/issues/70 for a proposal to add support for a conf.d style directory directly into OMERO.


Example Playbooks
-----------------

    # Install the latest release, including PostgreSQL on the same server
    - hosts: localhost
      roles:

      - role: ome.postgresql
        postgresql_version: "10"
        postgresql_databases:
          - name: omero
        postgresql_users:
          - user: omero
            password: omero
            databases: [omero]

      - role: ome.omero-server


    # Install or upgrade to a particular version, with an external database
    - hosts: localhost
      roles:
      - ome.omero-server
        omero_server_release: 5.6.0
        omero_server_dbhost: postgres.example.org
        omero_server_dbuser: db_user
        omero_server_dbname: db_name
        omero_server_dbpassword: db_password
        # Version required for the psql client
        postgresql_version: "10"


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
