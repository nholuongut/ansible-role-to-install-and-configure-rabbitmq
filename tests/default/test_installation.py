import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_rabbitmq_is_installed(host):
    rabbitmq = host.package("rabbitmq-server")
    ansible_vars = host.ansible.get_variables()

    rabbitmq_version = "{}.{}.{}".format(
        ansible_vars['rabbitmq_major'],
        ansible_vars['rabbitmq_minor'],
        ansible_vars['rabbitmq_patch']
    )

    assert rabbitmq.is_installed
    assert rabbitmq.version.startswith(rabbitmq_version)


def test_earlang_is_installed(host):
    erlang = host.package("erlang")
    assert erlang.is_installed


def test_rabbitmq_running_and_enabled(host):
    rabbitmq = host.service("rabbitmq-server")
    assert rabbitmq.is_enabled
    assert rabbitmq.is_running


def test_amqp_port_is_listening(host):
    amqp_port = host.socket("tcp://:::5672")
    assert amqp_port.is_listening


def test_tls_port_is_listening(host):
    amqp_port = host.socket("tcp://:::5671")
    assert not amqp_port.is_listening


def test_management_port_is_listening(host):
    amqp_port = host.socket("tcp://0.0.0.0:15672")
    assert amqp_port.is_listening
