import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_configs as scrapli_send_configs
# from nornir_napalm.plugins.tasks import napalm_configure
# from nornir_netmiko.tasks import netmiko_send_config
import ipaddress
from constants import config_file
import os


def get_env_vars(ctx, args, incomplete):
    return [k for k in os.environ.keys() if incomplete in k]


def interfaces_config(task):
    interfaces_cms = []
    interfaces = task.host['interfaces']
    for name, interface in interfaces.items():
        cm = f"interface {name}"
        interfaces_cms.append(cm)
        if "lo" not in name.lower():
            interfaces_cms.append("no shut")
        interface = ipaddress.IPv4Interface(interface)
        cm = f"ip address {interface.ip} {interface.network.netmask}"
        interfaces_cms.append(cm)
    if task.host.platform == "cisco_xr":
        interfaces_cms.append("commit")
    # task.run(netmiko_send_config, config_commands=interfaces_cms)
    task.run(scrapli_send_configs, configs=interfaces_cms)
    # task.run(napalm_configure, configuration=interfaces_cms, replace=False)


@click.group(name="interfaces")
def cli_interfaces():
    """Command for interfaces configuration
    """
    pass


@cli_interfaces.command(
    name="configure",
    help="Configure the Interfaces from the dictionary defined in hosts.yaml")
# @click.argument("device2", type=click.STRING, autocompletion=get_env_vars)
@click.option(
    "--device", help="Configure only the device", required=False,
    autocompletion=get_env_vars)
@click.option(
    "--group",
    help="Configure all devices belong to the group", required=False)
def run_interfaces_config(device, group):
    # config_file = os.environ.get('NORNIR_CONFIG_FILE')
    # os.chdir('../')
    # os.getcwd()
    # breakpoint()
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=interfaces_config)
    print_result(result)
