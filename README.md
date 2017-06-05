OMERO Server
============

Installs and configures OMERO.server.


Dependencies
------------

A PostgreSQL server is required.



Role Variables
--------------

All variables are optional, see `defaults/main.yml` for the full list

OMERO.server version.
- `omero_server_release`: The OMERO release, e.g. `5.2.2`.
This defaults to `latest`, but due to the broken registry a proper upgrade check has not been implemented so this will not have the expected effect (it will always attempt to upgrade even if the current server is the latest).
You are advised to change this to an actual release version.
- `omero_server_upgrade`: Upgrade OMERO.server if the current version does not match `omero_server_release`.
  This is a workaround for the inability to check for the latest version when `omero_server_release: latest`.
  At present this will skip an available upgrade if `False` but in future this will be changed to fail if the currently installed version does not match `omero_server_release`.
- `omero_server_ice_version`: The ice version.

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
- `omero_server_systemd_require_network`: Should omero systemd services require a network before starting? Default `True`.

- `omero_server_database_backupdir`: Dump the OMERO database to this directory before upgrading, default empty (disabled)


Unstable features
-----------------

Variables :
- `omero_server_datadir_chown`: Recursively set the owner on the OMERO data directory, use if the directory has been copied with an incorrect owner, default `False`
- `omero_server_database_manage`: Initialise or upgrade the OMERO database if required, default `True`, if `False` the database will not be modified and all `omero_server_db*` will be ignored (`omero.db.*` OMERO configuration parameters will not be updated with the corresponding `omero_server_db*` values)
- `omero_server_systemd_start`: Automatically enable and start/restart systemd omero-server service, default `True`.
  This is intended for use in server images where installation may be separate from configuration and execution.
- `omero_server_always_reset_config`: Clear the existing configuration before regenerating, default `True`.



Configuring OMERO.server
------------------------

This role regenerates the OMERO configuration file using the configuration files and helper script in `/opt/omero/server/config`.
`omero_server_config_set` can be used for simple configurations, for anything more complex consider creating one or more configuration files under: `/opt/omero/server/config/` with the extension `.omero`.

Manual configuration changes (`omero config ...`) will be lost following a restart of `omero-server` with systemd, you can disable this by setting `omero_server_always_reset_config: False`.
Manual configuration changes will never be copied during an upgrade.

See https://github.com/openmicroscopy/design/issues/70 for a proposal to add support for a conf.d style directory directly into OMERO.


Example Playbooks
-----------------

    # Install the latest release, including PostgreSQL on the same server
    - hosts: localhost
      roles:
      - role: openmicroscopy.omero-server
        postgresql_users_databases:
        - user: omero
          password: omero
          databases: [omero]

    # Install or upgrade to a particular version, use an external database
    - hosts: localhost
      roles:
      - openmicroscopy.omero-server
        omero_server_upgrade: True
        omero_server_release: 5.3.1
        omero_server_dbhost: postgres.example.org
        omero_server_dbuser: db_user
        omero_server_dbname: db_name
        omero_server_dbpassword: db_password


Author Information
------------------

ome-devel@lists.openmicroscopy.org.uk
