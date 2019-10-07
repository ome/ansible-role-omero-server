import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omero-server-olddep')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'


def test_omero_version(host):
    with host.sudo('data-importer'):
        ver = host.check_output("%s version" % OMERO)
    assert re.match('5\.2\.\d+-ice36-', ver)


def test_postgres_version(host):
    ver = host.check_output("psql --version")
    assert ver.startswith('psql (PostgreSQL) 9.4.')


def test_no_virtualenv(host):
    assert not host.file('/opt/omero/server/venv').exists
