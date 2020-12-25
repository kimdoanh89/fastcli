import click
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command as scrapli_send_command
from nornir_scrapli.functions import print_structured_result
from nafc.api.print_table_result import print_table_result

# from nornir_netmiko.tasks import netmiko_send_command
from constants import config_file


def get_config(task, command):
    # task.run(netmiko_send_command, command_string=f"{command}")
    task.run(scrapli_send_command, command=command)


@click.group(name="show")
def cli_get():
    """Get information from all devices [], filtered by name or group"""
    pass


@cli_get.command(name="facts", help="Get facts from devices")
@click.option("--command", help="The command to get information")
@click.option(
    "--structured/--no-structrued",
    default=False,
    help="present structured data",
    required=False,
)
@click.option(
    "--table/--no-table", default=False, help="present data in a table", required=False
)
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", help="Configure all devices belong to the group", required=False
)
def run_get_config(command, structured, table, device, group):
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    result = nr.run(task=get_config, command=command)
    # breakpoint()
    if structured:
        print_structured_result(result, parser="genie")
    elif table:
        print_table_result(result, parser="genie")
    else:
        print_result(result)
    return result
