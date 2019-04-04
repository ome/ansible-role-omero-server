import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    '.molecule/ansible_inventory').get_hosts('omero-server-newdep')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
OMERO_LOGIN = '-C -s localhost -u root -w omero'


def test_inplace_import(Command, File, Sudo):
    fake_file = '/data/import/test.fake'
    with Sudo('data-importer'):
        outimport = Command.check_output(
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
    with Sudo('data-importer'):
        outhql = Command.check_output(
            '%s %s hql -q --style plain "%s"' % (OMERO, OMERO_LOGIN, query))

    f = File('/OMERO/ManagedRepository/%s' % outhql.split(',', 1)[1])
    assert f.is_symlink
    assert f.linked_to == fake_file
