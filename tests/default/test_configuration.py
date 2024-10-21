import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_rabbitmq_config_file_permissions_must_be_644(host):
    ansible_vars = host.ansible.get_variables()
    rabbitmq_conf_file = "/etc/rabbitmq/rabbitmq.config"

    if (ansible_vars['rabbitmq_clustering_enabled']):
        with host.sudo():
            rabbitmq_config = host.file(rabbitmq_conf_file)
    else:
        rabbitmq_config = host.file(rabbitmq_conf_file)

    assert rabbitmq_config.exists
    assert rabbitmq_config.is_file
    assert rabbitmq_config.user == 'rabbitmq'
    assert rabbitmq_config.group == 'rabbitmq'
    assert rabbitmq_config.mode == 0o644


def test_rabbitmq_guest_user_not_present(host):
    ansible_vars = host.ansible.get_variables()
    rabbitmqctl_list_users_cmd = "rabbitmqctl list_users"

    if (ansible_vars['rabbitmq_clustering_enabled']):
        with host.sudo():
            rabbitmq_users = host.run(rabbitmqctl_list_users_cmd)
    else:
        rabbitmq_users = host.run(rabbitmqctl_list_users_cmd)

    assert "guest" not in rabbitmq_users.stdout


def test_rabbitmq_rabbit_user_present(host):
    ansible_vars = host.ansible.get_variables()
    rabbitmqctl_list_users_cmd = "rabbitmqctl list_users"

    if (ansible_vars['rabbitmq_clustering_enabled']):
        with host.sudo():
            rabbitmq_users = host.run(rabbitmqctl_list_users_cmd)
    else:
        rabbitmq_users = host.run(rabbitmqctl_list_users_cmd)

    assert "admin" in rabbitmq_users.stdout


def test_rabbitmq_rabbit_local_user_present(host):
    rabbitmq_user = host.user("rabbitmq")
    assert rabbitmq_user.exists
