from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_send_config
import os


def redistribute_at_R1_config(task):
    redis_cms = ["router eigrp 100",
                 "redistribute ospf 1 metric 10 10 1 1 1",
                 "router ospf 1",
                 "redistribute eigrp 100 subnets"]
    task.run(netmiko_send_config, config_commands=redis_cms)


def redistribute_at_R6_config(task):
    redis_cms = ["router rip",
                 "redistribute ospf 1 metric 1",
                 "router ospf 1",
                 "redistribute rip"]
    task.run(netmiko_send_config, config_commands=redis_cms)


def route_summarization_at_R1(task):
    summarize_cms = ["router ospf 1",
                     "summary-address 207.1.4.0 255.255.252.0",
                     "summary-address 208.1.4.0 255.255.252.0"]
    task.run(netmiko_send_config, config_commands=summarize_cms)


def route_summarization_at_R6(task):
    summarize_cms = ["router ospf 1",
                     "summary-address 109.1.4.0 255.255.252.0"]
    task.run(netmiko_send_config, config_commands=summarize_cms)


def main():
    config_file = os.environ.get('NORNIR_CONFIG_FILE')
    nr = InitNornir(config_file=f"{config_file}")
    # Redistribute routes at R1
    nr5 = nr.filter(name="R1")
    result = nr5.run(task=redistribute_at_R1_config)
    print_result(result)
    # Redistribute routes at R6
    nr6 = nr.filter(name="R6")
    result = nr6.run(task=redistribute_at_R6_config)
    print_result(result)
    # Summarize routes at R1
    nr7 = nr.filter(name="R1")
    result = nr7.run(task=route_summarization_at_R1)
    print_result(result)
    # Summarize routes at R6
    nr8 = nr.filter(name="R6")
    result = nr8.run(task=route_summarization_at_R6)
    print_result(result)


if __name__ == "__main__":
    main()
