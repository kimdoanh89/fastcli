# Nornir-3.0 - Network Automation Fast Configuration (NAFC)

## Requirements

To use this code you will need:

- Python 3.8+

## Install and Setup
Clone the code to local machine.
```bash
git clone https://github.com/kimdoanh89/fastcli
cd fastcli
```

Setup Python Virtual Environment (requires Python 3.8+)
```bash
python3.8 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

The environment `NORNIR_CONFIG_FILE` needs to be configure before running:
```bash
export NORNIR_CONFIG_FILE=inventory/tutorial-1/config.yaml
```
Some configuration files are under `inventory/tutorial-1` folder.
- defaults.yaml
- groups.yaml
- hosts.yaml

Changes the `hosts.yaml` depending on your network topology.

## Some commands supported
| fastcli commands                                     	| Usage                                                                                                                 	|
|------------------------------------------------------	|-----------------------------------------------------------------------------------------------------------------------	|
| python fastcli.py interfaces configure               	| configure the Interfaces of all the devices, can be <br>  filtered with the keywords: --device, --group               	|
| python fastcli.py show facts --command "any command" 	| show facts with a given command, can be filtered with <br>  --device, --group, show structured data with --structured 	|
| python fastcli.py ospf configure --ospf_area 0       	| configure OSPF routing of all the OSPF routers, can <br>  configure each area with keyword: --ospf_area               	|
| python fastcli.py ospf stub --ospf_area 0            	| configure an OSPF area as stub area                                                                                   	|
| python fastcli.py ospf nssa --ospf_area 0            	| configure an OSPF area as Not-So-Stubby-Area                                                                          	|
| python fastcli.py eigrp configure                    	| configure EIGRP routing of all the EIGRP routers                                                                      	|
| python fastcli.py rip configure                      	| configure RIP routing of all the RIP routers                                                                          	|

## Output

### Configure interfaces

![Alt text](images/00_configure_interfaces.png)

### Configure ospf

![Alt text](images/01_configure_ospf.png)

### Collect facts and present in a table
**NOTE**: This table formatting currently works only for `sh version` command.

![Alt text](images/04_sh_version_table.PNG)