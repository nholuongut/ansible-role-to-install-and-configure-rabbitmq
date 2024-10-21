import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_libselinux_python_is_installed(host):
    libselinux_python = host.package("libselinux-python")
    assert libselinux_python.is_installed
