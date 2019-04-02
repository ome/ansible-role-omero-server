import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_service_running_and_enabled(Service):
    service = Service('omero-server')
    assert service.is_running
    assert service.is_enabled


def test_omero_root_login(Command, Sudo):
    with Sudo('data-importer'):
        Command.check_output('%s login %s' % (OMERO, OMERO_LOGIN))


@pytest.mark.parametrize("key,value", [
    ('omero.data.dir', '/OMERO'),
    ('omero.client.ui.tree.type_order',
     '["screen", "plate", "project", "dataset"]'),
    ('omero.policy.binary_access', '-read,-write,-image,-plate'),
])
def test_omero_server_config(Command, Sudo, key, value):
    with Sudo('omero-server'):
        cfg = Command.check_output("%s config get %s", OMERO, key)
    assert cfg == value


def test_omero_datadir(File):
    d = File('/OMERO')
    assert d.is_directory
    assert d.user == 'omero-server'
    assert d.group == 'root'
    assert d.mode == 0o755


def test_omero_managedrepo(File):
    d = File('/OMERO/ManagedRepository')
    assert d.is_directory
    assert d.user == 'omero-server'
    assert d.group == 'importer'
    assert d.mode == 0o2775
