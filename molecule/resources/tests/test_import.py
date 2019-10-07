import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(
        'omero-server-newdep,omero-server-upgradetovenv')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_inplace_import(host):
    fake_file = '/data/import/test.fake'
    with host.sudo('data-importer'):
        outimport = host.check_output(
            '%s %s import --skip=upgrade --transfer=ln_s %s' %
            (OMERO, OMERO_LOGIN, fake_file))

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
            '%s %s hql -q --style plain "%s"' % (OMERO, OMERO_LOGIN, query))

    f = host.file('/OMERO/ManagedRepository/%s' % outhql.split(',', 1)[1])
    assert f.is_symlink
    assert f.linked_to == fake_file
