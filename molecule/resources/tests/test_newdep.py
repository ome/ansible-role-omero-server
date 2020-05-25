import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(
        'omero-server-newdep,omero-server-upgradetovenv')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)\.(\d+)-ice36-')


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


def test_additional_python(host):
    piplist = host.check_output("/opt/omero/server/venv/bin/pip list")
    assert "omero-upload" in piplist


def test_running_in_venv(host):
    # host.process may use `ps -Aww -o ...` which truncates some fields
    # https://github.com/philpep/testinfra/blob/3.2.0/testinfra/modules/process.py#L127-L148
    count = 0
    for line in host.check_output('ps -Aww -o pid,comm,user').splitlines()[1:]:
        pid, command, user = line.split()
        if command == 'python' and user == 'omero-server':
            count += 1
            f = host.file('/proc/%s/exe' % pid)
            assert f.linked_to == '/opt/omero/server/venv/bin/python'
    assert count > 1
