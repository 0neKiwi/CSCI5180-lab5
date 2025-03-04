import json
from easysnmp import Session

hosts = ["198.51.101.1", "10.1.1.12", "10.1.1.13", "198.51.100.4", "10.1.1.5"]
addresses = {}
statuses = {}

def NMsnmp(file, hosts):
    addresses = {}
    status = {}
    for host in hosts:
        s = Session(hostname=host, community="public", version=2)
        hostname = s.get("sysName.0").value
        if_items = s.walk("ifDescr")
        ifaces = [i.value for i in if_items]
        if_items = s.walk("ipAdEntIfIndex")
        addresses[hostname] = {"addresses":{ifaces[int(i.value)-1]:i.oid_index for i in if_items}}
        if_oitems = s.walk("ifOperStatus")
        statuses[hostname] = {ifaces[int(i.oid_index)-1]:"up" if (i.value == '1') else "down" for i in if_oitems}
        ipv6_items1 = s.walk("ipAddressType.ipv6")
        ipv6_items2 = s.walk("ipAddressType.ipv6z")
    with open(file, "w") as f:
        json.dump(addresses, f, indent=1)
        json.dump(statuses, f, indent=1)
    return addresses, statuses

if __name__ == "__main__":
    NMsnmp("json.txt", hosts)
