import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config
from constants import config_file


def rip_config(task):
    rip_cms = []
    rip_cms.append("router rip")
    rip_cms.append("version 2")
    rip_cms.append("no auto")
    rip_advertised = task.host['rip_advertised']
    for nw in rip_advertised:
        rip_cms.append(f"network {nw}")
    task.run(netmiko_send_config, config_commands=rip_cms)


@click.group(name="rip")
def cli_rip():
    """Command for RIP configuration
    """
    pass


@cli_rip.command(
    name="configure",
    help="Configure RIP from the information defined in hosts.yaml")
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", default="rip", show_default=True,
    help="Configure all devices belong to the group", required=False)
def run_eigrp_config(device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=rip_config)
    print_result(result)
