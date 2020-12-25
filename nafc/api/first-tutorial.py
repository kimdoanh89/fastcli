from nornir import InitNornir
from nornir.core.filter import F
import ipaddress
from constants import config_file


def has_long_name(host):
    return len(host.name) == 3


def in_area0(host):
    return host.data["ospf_area"] == 0


select_hosts = ["R1", "R2"]

nr = InitNornir(config_file=f"{config_file}")

print("Hosts: ", nr.inventory.hosts)
print("Groups: ", nr.inventory.groups)
print("Hosts of Group area0: ", nr.inventory.children_of_group("area0"))
print("Hosts of Group area10: ", nr.inventory.children_of_group("area10"))

print("network Advertised of router R6: ", nr.inventory.hosts["R6"]["nw_advertised"])

for key, values in nr.inventory.hosts["R6"]["nw_advertised"].items():
    for v in values:
        print("Area", key, ":", v)
        nw = ipaddress.ip_network(v)
        print("network {} {} area {}".format(nw.network_address, nw.hostmask, key))


nr1 = nr.filter(filter_func=has_long_name)
breakpoint()
nr3 = nr.filter(filter_func=lambda h: h.name in select_hosts)
nr5 = nr.filter(filter_func=lambda h: h.data["ospf_area"] == 0)
nr4 = nr.filter(F(hostname__any=["R1", "R2"]))
nr2 = nr.filter(filter_func=in_area0)

breakpoint()
