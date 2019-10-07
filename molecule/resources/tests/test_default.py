import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_service_running_and_enabled(host):
    assert host.service('omero-server').is_running
    assert host.service('omero-server').is_enabled


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
        cfg = host.check_output("%s config get %s", OMERO, key)
    assert cfg == value


def test_omero_datadir(host):
    d = host.file('/OMERO')
    assert d.is_directory
    assert d.user == 'omero-server'
    assert d.group == 'root'
    assert d.mode == 0o755


def test_omero_managedrepo(host):
    d = host.file('/OMERO/ManagedRepository')
    assert d.is_directory
    assert d.user == 'omero-server'
    assert d.group == 'importer'
    assert d.mode == 0o2775
