import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omero-py3')

OMERO = '/opt/omero/server/OMERO.server/bin/omero'
# Need to match 5.6.dev2
# VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')
VERSION_PATTERN = re.compile(r'(\d+)\.(\d+)\.(\w+)')


def test_omero_version(host):
    with host.sudo('data-importer'):
        ver = host.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    assert int(m.group(1)) >= 5
    assert int(m.group(2)) >= 6


def test_postgres_version(host):
    ver = host.check_output("psql --version")
    assert ver.startswith('psql (PostgreSQL) 13')


def test_additional_python(host):
    piplist = host.check_output("/opt/omero/server/venv3/bin/pip list")
    assert "omero-upload" in piplist


def test_running_in_venv(host):
    # host.process may use `ps -Aww -o ...` which truncates some fields
    # https://github.com/philpep/testinfra/blob/3.2.0/testinfra/modules/process.py#L127-L148
    count = 0
    for line in host.check_output('ps -Aww -o pid,comm,user').splitlines()[1:]:
        pid, command, user = line.split()
        if command == 'python' and user == 'omero-server':
            try:
                f = host.file('/proc/%s/environ' % pid)
                env = dict(item.split('=', 1) for item in
                           f.content_string.split('\0') if item)
                assert env.get('PATH').startswith(
                    '/opt/omero/server/venv3/bin:')
                count += 1
            except RuntimeError:
                # Might be a transient unrelated process
                pass
    assert count > 1
