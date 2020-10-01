import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config
import ipaddress
from constants import config_file


def ospf_config(task):
    ospf_cms = []
    interfaces = task.host['interfaces']
    ospf_advertised = task.host['ospf_advertised']
    router_id = task.host['ospf_router_id']
    for name, _ in interfaces.items():
        if "lo" in name:
            ospf_cms.append(f"interface {name}")
            ospf_cms.append("ip ospf network point-to-point")

    ospf_cms.append("router ospf 1")
    ospf_cms.append(f"router-id 0.0.0.{router_id}")
    for key, values in ospf_advertised.items():
        for v in values:
            nw = ipaddress.ip_network(v)
            cm = f"network {nw.network_address} {nw.hostmask} area {key}"
            ospf_cms.append(cm)
    if task.host.platform == "cisco_xr":
        ospf_cms.append("commit")
    task.run(netmiko_send_config, config_commands=ospf_cms)


def stub_area_config(task, area: int):
    stub_cms = ["router ospf 1", f"area {area} stub"]
    task.run(netmiko_send_config, config_commands=stub_cms)


def not_so_stubby_area_config(task, area: int):
    stub_cms = ["router ospf 1", f"area {area} nssa"]
    task.run(netmiko_send_config, config_commands=stub_cms)


@click.group(name="ospf")
def cli_ospf():
    """Commands for OSPF configuration
    """
    pass


@cli_ospf.command(
    name="configure",
    help="Configure OSPF from the information defined in hosts.yaml")
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", default="ospf", show_default=True,
    help="Configure all devices belong to the group", required=False)
def run_ospf_config(device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=ospf_config)
    print_result(result)


@cli_ospf.command(
    name="stub",
    help="Configure an OSPF area as stub area")
@click.option(
    "--ospf_area", help="Area to be configured", required=True, type=int)
def run_stub_config(ospf_area):
    nr = InitNornir(config_file=f"{config_file}")
    nr = nr.filter(F(ospf_area__contains=int(ospf_area)))
    result = nr.run(task=stub_area_config, area=ospf_area)
    print_result(result)


@cli_ospf.command(
    name="nssa",
    help="Configure an OSPF area as Not-So-Stubby-Area")
@click.option(
    "--ospf_area", help="Area to be configured", required=True, type=int)
def run_nssa_config(ospf_area):
    nr = InitNornir(config_file=f"{config_file}")
    nr = nr.filter(F(ospf_area__contains=int(ospf_area)))
    result = nr.run(task=not_so_stubby_area_config, area=ospf_area)
    print_result(result)
