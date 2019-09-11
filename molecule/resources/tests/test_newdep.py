import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(
        'omero-server-newdep,omero-server-upgradetovenv')

OMERO = ('/opt/omero/server/venv/bin/python '
         '/opt/omero/server/OMERO.server/bin/omero')
OMERO_LOGIN = '-C -s localhost -u root -w omero'
VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')


def test_omero_version(host):
    with host.sudo('data-importer'):
        ver = host.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    assert int(m.group(1)) >= 5
    assert int(m.group(2)) > 2


def test_postgres_version(host):
    ver = host.check_output("psql --version")
    assert ver.startswith('psql (PostgreSQL) 9.6.')


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


def test_additional_python(host):
    piplist = host.check_output("/opt/omero/server/venv/bin/pip list")
    assert "omero-upload" in piplist
