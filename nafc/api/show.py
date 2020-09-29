import click
import os
from nornir import InitNornir
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command as scrapli_send_command
from nornir_scrapli.functions import print_structured_result
from nafc.api.print_table_result import print_table_result
# from nornir_netmiko.tasks import netmiko_send_command


def get_config(task, command):
    # task.run(netmiko_send_command, command_string=f"{command}")
    task.run(scrapli_send_command, command=command)


@click.group(name="show")
def cli_get():
    """Commands to configure interfaces of a device
    """
    pass


@cli_get.command(name="facts", help="Get facts from devices")
@click.option("--command", help="The command to get information")
@click.option(
    "--structured", default=False,
    help="How you want to present data", required=False)
@click.option(
    "--table", default=False,
    help="How you want to present data", required=False)
@click.option("--device", help="Configure only the device", required=False)
@click.option(
    "--group", help="Configure all devices belong to the group")
@click.option(
    "--key", help="Filter the devices to be configured with <key, value>")
@click.option(
    "--value",
    help="Filter the devices to be configured with <key, value>")
def run_get_config(command, structured, table, device, group, key, value):
    config_file = os.environ.get('NORNIR_CONFIG_FILE')
    nr = InitNornir(config_file=f"{config_file}")
    if device:
        nr = nr.filter(name=f"{device}")
    if group:
        nr = nr.filter(F(groups__contains=f"{group}"))
    if (key is not None and value is not None):
        nr = nr.filter(F(ospf_area__contains=0))
    result = nr.run(task=get_config, command=command)
    if structured:
        print_structured_result(result, parser="genie")
    elif table:
        print_table_result(result, parser="genie")
    else:
        print_result(result)

    # breakpoint()
    # print_structured_result(result, parser="textfsm")
    # y = nr.filter(F(ospf_area__contains=0))
