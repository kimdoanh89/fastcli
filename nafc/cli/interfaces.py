from fastlab.api.interfaces import interfaces_config
import click


@click.group(name="interfaces")
def cli_interfaces():
    """Commands to monitor omp: tlocs, tloc-paths
    """
    pass


@cli_interfaces.command(
    name="configure", help="Configure the Interfaces from the dictionary defined in hosts.yaml")
@click.option("--system_ip", help="System IP of the WAN Edge")
def run_interfaces_config(system_ip):
    pass
