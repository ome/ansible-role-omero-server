# Changes in Version 6

## Summary of breaking changes

-  Install self-signed certificates by default

# Changes in Version 5

## Summary of breaking changes

-  Remove support for CentOS 7 and Ubuntu 20.04
-  Add support for RHEL/RockyLinux 9 and Ubuntu 202.04

# Changes in Version 4

## Summary of breaking changes

-   Python 2 support is now dropped
-   `omero_server_python_requirements_ice_package` is now a nested dictionary
    to support multiple versions per distribution

## Removed variables

- `omero_server_python3`: the role only installs the server with Python 3
- `omero_server_virtualenv`: a virtual environment is created unconditionally
- `omero_server_systemd_require_network`

# Changes in Version 3

## Summary of breaking changes
- Default to installing and running under Python 3.6.
  Set `omero_server_python3: false` to use Python 2.7.
- The server always uses a virtualenv `/opt/omero/server/venv3` and does not include system-site-packages.

## Removed variables
- `omero_server_ice_version`: This is now an internal variable and must always be `3.6`.


# Changes in Version 2

## Summary of breaking changes
- All variables are prefixed with `omero_server`.
- OMERO.web has been moved to an independent role `omero-web`, it is no longer setup by this role.
- The OMERO data directory creation logic is simplified.
- Some configuration variables and handlers have been moved to a dependent role `omero-common`.
- `omego` is in a dependent role.
- The `omero` system user is renamed `omero-server` and has a minimal home directory `/opt/omero/server`.
- The `omero` systemd service is renamed to `omero-server`.
- Systemd is setup by default.
- If you disable systemd setup OMERO.server is not automatically started.
- PostgreSQL server is not installed by this role (the clients are still installed).
- The database is not backed-up by default since you probably want the backup to go to a custom path (set `omero_server_database_backupdir`).
- Manual configuration changes are not copied when the server is upgraded.
- Configuration should be done using a conf.d style directory.
- This role requires Ansible 2.2.

## Removed variables
- `omero_datadir_create`: OMERO data directories are always created and the top-level owner/group/permissions reset
- `omero_db_create`: A PostgreSQL database must be setup independently of this role
- `omero_omego_venv`: Replaced by `omero_server_omego` which is the path to the executable
- `omero_prestart_file`: Replaced by a config directory
- `omero_reinstall_on_error`: Never implemented
- `omero_selinux_setup`: Only used by the OMERO.web tasks
- `omero_serverdir`: Same as `omero_server_basedir`
- `omero_systemd_restart`: The systemd restart policy is now always `no`
- `omero_web_install`: OMERO.web is no longer managed by this role

## Renamed variables
- `omero_basedir`: `omero_server_basedir`

- `omero_database_backupdir`: `omero_server_database_backupdir`

- `omero_datadir_managedrepo_mode`: `omero_server_datadir_managedrepo_mode`
- `omero_datadir`: `omero_server_datadir`
- `omero_datadir_chown`: `omero_server_datadir_chown`
- `omero_datadir_managedrepo`: `omero_server_datadir_managedrepo`
- `omero_datadir_mode`: `omero_server_datadir_mode`

- `omero_dbhost`: `omero_server_dbhost`
- `omero_dbuser`: `omero_server_dbuser`
- `omero_dbname`: `omero_server_dbname`
- `omero_dbpassword`: `omero_server_dbpassword`

- `omero_omego_additional_args`: `omero_server_omego_additional_args`
- `omero_omego_verbosity`: `omero_server_omego_verbosity`

- `omero_release`: `omero_server_release`

- `omero_rootpassword`: `omero_server_rootpassword`

- `omero_system_uid`: `omero_server_system_uid`
- `omero_system_user`: `omero_server_system_user`
- `omero_system_umask`: `omero_server_system_umask`
- `omero_system_managedrepo_group`: `omero_server_system_managedrepo_group`

- `omero_systemd_setup`: `omero_server_systemd_setup`
- `omero_server_limit_nofile`: `omero_server_systemd_limit_nofile`

- `omero_server_config`: `omero_server_config_set`

- `omero_upgrade`: `omero_server_upgrade`



## Handlers
- Handlers that are intended to be used outside this role have been moved to the `omero-common` role so they can be used in other playbooks and roles without depending on this role.
