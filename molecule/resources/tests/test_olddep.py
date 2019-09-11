import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omero-server-olddep')

OMERO = ('/opt/omero/server/OMERO.server/bin/omero')
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_omero_version(host):
    with host.sudo('data-importer'):
        ver = host.check_output("%s version" % OMERO)
    assert re.match('5\.2\.\d+-ice36-', ver)


def test_postgres_version(host):
    ver = host.check_output("psql --version")
    assert ver.startswith('psql (PostgreSQL) 9.4.')


def test_omero_root_login(host):
    with host.sudo('data-importer'):
        host.check_output('%s login %s' % (OMERO, OMERO_LOGIN))


@pytest.mark.parametrize("key,value", [
    ('omero.data.dir', '/OMERO'),
    ('omero.client.ui.tree.type_order',
     '["screen", "plate", "project", "dataset"]'),
    ('omero.policy.binary_access', '-read,-write,-image,-plate'),
])
def test_omero_server_config(host, key, value):
    with host.sudo('omero-server'):
        cfg = host.check_output("%s config get %s" % (OMERO, key))
    assert cfg == value


def test_no_virtualenv(host):
    assert not host.file('/opt/omero/server/venv').exists
