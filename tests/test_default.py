import testinfra.utils.ansible_runner
import pytest
import re

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize("name", ["omero", "omero-web", "nginx"])
def test_services_running_and_enabled(Service, name):
    service = Service(name)
    assert service.is_running
    assert service.is_enabled


def test_omero_version(Command, Sudo, TestinfraBackend):
    host = TestinfraBackend.get_hostname()
    with Sudo('omero'):
        ver = Command.check_output(
            "/home/omero/OMERO.server/bin/omero version")
    if host == 'omero-server-ice35':
        assert re.match('\d+\.\d+\.\d+-ice35-', ver)
    else:
        assert re.match('\d+\.\d+\.\d+-ice36-', ver)


def test_omero_root_login(Command, Sudo):
    with Sudo('omero'):
        Command.run_expect(
            [0],
            "/home/omero/OMERO.server/bin/omero login -C "
            "-s localhost -u root -w omero")


def test_omero_datadir(File):
    d = File('/OMERO')
    assert d.is_directory
    assert d.user == 'omero'
    assert d.group == 'root'
    assert d.mode == 0o755


def test_omero_managedrepo(File):
    d = File('/OMERO/ManagedRepository')
    assert d.is_directory
    assert d.user == 'omero'
    assert d.group == 'importer'
    assert d.mode == 0o2775
