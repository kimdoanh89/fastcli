import click
from nafc.api.interfaces import cli_interfaces
from nafc.api.show import cli_get
from nafc.api.ospf import cli_ospf
from nafc.api.eigrp import cli_eigrp
from nafc.api.rip import cli_rip
from nafc.api.bgp import cli_bgp


@click.group()
def cli():
    """CLI tool for fast configuration of the network, powerd by Nornir 3.0."""
    pass


cli.add_command(cli_interfaces)
cli.add_command(cli_get)
cli.add_command(cli_ospf)
cli.add_command(cli_eigrp)
cli.add_command(cli_rip)
cli.add_command(cli_bgp)


if __name__ == "__main__":
    cli()
