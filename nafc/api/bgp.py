import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config
from constants import config_file
import ipaddress


def bgp_config(task):
    bgp_cms = []
    asn = task.host['asn']
    bgp_neighbors = task.host['bgp_neighbors']
    bgp_advertised = task.host['bgp_advertised']
    bgp_cms.append(f"router bgp {asn}")
    for nw in bgp_advertised:
        nw = ipaddress.ip_network(nw)
        bgp_cms.append(f"network {nw.network_address} mask {nw.netmask}")
    for key, values in bgp_neighbors.items():
        for v in values:
            bgp_cms.append(f"neighbor {v} remote-as {key}")
    task.run(netmiko_send_config, config_commands=bgp_cms)


def ibgp_config(task):
    """ Configure ibgp Neighbor Relationship based on the Loopback
    ibgp_neighbors: {"remote-as": ["list of remote AS's ip address"], ...}
    At R2:
    ibgp_neighbors: {"1000": ["10.1.1.1", "10.3.3.3"]} means that
    the current host R2 will have ibgp neighbor relationship with
    R1 (10.1.1.1) and R3 (10.3.3.3)
    ibgp_update_source: {"lo11": ["10.1.1.1", "10.3.3.3"]} means that
    loopback 11 will be used as update-source for 10.1.1.1 and 10.3.3.3
    route_relector_clients: ["10.1.1.1", "10.3.3.3"]
    Set R1 and R3 as route reflector clients, this will automatically
    enable R2 as Route Reflector.
    """
    ibgp_cms = []
    asn = task.host['asn']
    ibgp_neighbors = task.host['ibgp_neighbors']
    ibgp_update_source = task.host['ibgp_update_source']
    ibgp_cms.append(f"router bgp {asn}")
    for key, values in ibgp_neighbors.items():
        for v in values:
            ibgp_cms.append(f"neighbor {v} remote-as {key}")
            ibgp_cms.append(f"neighbor {v} next-hop-self")
    for key, values in ibgp_update_source.items():
        for v in values:
            ibgp_cms.append(f"neighbor {v} update-source {key}")
    try:
        route_relector_clients = task.host['route_relector_clients']
        if route_relector_clients is not None:
            for route_relector_client in route_relector_clients:
                cm = f"neighbor {route_relector_client} route-reflector-client"
                ibgp_cms.append(cm)
    except KeyError:
        pass
    finally:
        task.run(netmiko_send_config, config_commands=ibgp_cms)


@click.group(name="bgp")
def cli_bgp():
    """Command for BGP configuration
    """
    pass


@cli_bgp.command(
    name="external",
    help="Configure eBGP from the information defined in hosts.yaml")
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", default="bgp", show_default=True,
    help="Configure all devices belong to the group", required=False)
def run_bgp_config(device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=bgp_config)
    print_result(result)


@cli_bgp.command(
    name="internal",
    help="Configure iBGP from the information defined in hosts.yaml")
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", default="ibgp", show_default=True,
    help="Configure all devices belong to the group", required=False)
def run_ibgp_config(device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=ibgp_config)
    print_result(result)
