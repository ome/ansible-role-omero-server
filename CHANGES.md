# Changes in Version 2

## Summary of breaking changes
- All variables are prefixed with `omero_server`.
- OMERO.web has been moved to an independent role, it is no longer setup by this role.
- The OMERO data directory creation logic is simplified.
- Some configuration variables and handlers have been moved to a dependent role `omero-common`.
- `omego` is in a dependent role.
- The `omero` system user has a minimal home directory: `/opt/omero/server`.
- The `omero` systemd service has is renamed to `omero-server`.
- Systemd is setup by default.
- If you disable systemd setup OMERO.server is not automatically started.

## Removed variables
- `omero_datadir_create`: OMERO data directories are always created and the top-level owner/group/permissions reset
- `omero_omego_venv`: Replaced by `omero_server_omego` which is the path to the executable
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

- `omero_db_create`: `omero_server_db_create`

- `omero_dbhost`: `omero_server_dbhost`
- `omero_dbuser`: `omero_server_dbuser`
- `omero_dbname`: `omero_server_dbname`
- `omero_dbpassword`: `omero_server_dbpassword`

- `omero_omego_additional_args`: `omero_server_omego_additional_args`
- `omero_omego_verbosity`: `omero_server_omego_verbosity`

- `omero_prestart_file`: `omero_server_prestart_file`

- `omero_release`: `omero_server_release`

- `omero_rootpassword`: `omero_server_rootpassword`

- `omero_system_uid`: `omero_server_system_uid`
- `omero_system_user`: `omero_server_system_user`
- `omero_system_umask`: `omero_server_system_umask`
- `omero_system_managedrepo_group`: `omero_server_system_managedrepo_group`

- `omero_systemd_setup`: `omero_server_systemd_setup`

- `omero_upgrade`: `omero_server_upgrade`



## Handlers
- These have been moved to the `omero-common` role so they can be used in other playbooks and roles without depending on this role.
