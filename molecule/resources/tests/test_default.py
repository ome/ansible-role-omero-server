import os
import pytest
import testinfra.utils.ansible_runner
from time import time

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

# Ubuntu sudo doesn't set HOME so it tries to write to /root
ENV = 'OMERO_USERDIR=/home/data-importer/omero-{}'.format(time())
OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_service_running_and_enabled(host):
    assert host.service('omero-server').is_running
    assert host.service('omero-server').is_enabled


def test_omero_root_login(host):
    with host.sudo('data-importer'):
        host.check_output('%s %s login %s' % (ENV, OMERO, OMERO_LOGIN))


@pytest.mark.parametrize("key,value", [
    ('omero.data.dir', '/OMERO'),
    ('omero.client.ui.tree.type_order',
     '["screen", "plate", "project", "dataset"]'),
    ('omero.policy.binary_access', '-read,-write,-image,-plate'),
])
def test_omero_server_config(host, key, value):
    with host.sudo('omero-server'):
        cfg = host.check_output('%s %s config get %s' % (ENV, OMERO, key))
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


def test_inplace_import(host):
    fake_file = '/data/import/test.fake'
    with host.sudo('data-importer'):
        outimport = host.check_output(
            '%s %s %s import --skip=upgrade --transfer=ln_s %s' %
            (ENV, OMERO, OMERO_LOGIN, fake_file))

    imageid = int(outimport.split(':', 1)[1])
    assert imageid

    query = ('SELECT concat(ofile.path, ofile.name) '
             'FROM FilesetEntry AS fse '
             'JOIN fse.fileset AS fileset '
             'JOIN fse.originalFile AS ofile '
             'JOIN fileset.images AS image '
             'WHERE image.id = %d' % imageid)
    with host.sudo('data-importer'):
        outhql = host.check_output(
            '%s %s %s hql -q --style plain "%s"' %
            (ENV, OMERO, OMERO_LOGIN, query))

    f = host.file('/OMERO/ManagedRepository/%s' % outhql.split(',', 1)[1])
    assert f.is_symlink
    assert f.linked_to == fake_file
