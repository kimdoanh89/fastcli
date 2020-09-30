import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
# from nornir_scrapli.tasks import send_configs as scrapli_send_configs
# from nornir_napalm.plugins.tasks import napalm_configure
from nornir_netmiko.tasks import netmiko_send_config
import os


def bgp_config(task):
    bgp_cms = []
    asn = task.host['asn']
    bgp_neighbors = task.host['bgp_neighbors']
    bgp_advertised = task.host['bgp_advertised']
    bgp_cms.append(f"router bgp {asn}")
    for nw in bgp_advertised:
        bgp_cms.append(f"network {nw}")
    for key, values in bgp_neighbors.items():
        for v in values:
            bgp_cms.append(f"neighbor {v} remote-as {key}")
    task.run(netmiko_send_config, config_commands=bgp_cms)


@click.group(name="bgp")
def cli_bgp():
    """Commands to configure interfaces of a device
    """
    pass


@cli_bgp.command(
    name="configure",
    help="Configure the Interfaces from the dictionary defined in hosts.yaml")
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", default="bgp", show_default=True,
    help="Configure all devices belong to the group", required=False)
def run_bgp_config(device, group):
    config_file = os.environ.get('NORNIR_CONFIG_FILE')
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=bgp_config)
    print_result(result)
