import json
import time
from easysnmp import Session
from matplotlib import pyplot as plt

hosts = ["198.51.101.1", "10.1.1.12", "10.1.1.13", "198.51.100.4", "10.1.1.5"]
addresses = {}
statuses = {}

#(int, oid_id) -> int: {v4 oid: oids, v6 oid: oids}
def add_ip_from_oid(address_dict, interface, oid_id):
    if interface not in address_dict.keys():
        address_dict[interface] = {}
    interface_dict = address_dict[interface]
    ps = oid_id.split(".")
    prefix = ".".join(ps[:2])
    if prefix == "1.4":
        ip = (".".join(ps[2:]))
        if "v4" not in interface_dict.keys():
            interface_dict["v4"] = [ip]
        else:
            interface_dict["v4"].append(ip)
        return ip
    if prefix in ("4.20", "2.16"):
        body = ps[2:2+8*2]
        body_str = ["%02x%s" % (int(body[i]), ":" if i%2 else "") for i in range(len(body))]
        ip = ("".join(body_str)[:-1])
        if "v6" not in interface_dict.keys():
            interface_dict["v6"] = [ip]
        else:
            interface_dict["v6"].append(ip)
        return ip

def write_snmp_to_file(file, hosts):
    res1 = {}
    res2 = {}
    for host in hosts:
        s = Session(hostname=host, community="public", version=2)
        hostname = s.get("sysName.0").value
        res1[hostname] = {"addresses": {}}
        h_addresses = res1[hostname]["addresses"]
        interface_items = s.walk("ifDescr")
        interfaces = [i.value for i in interface_items]
        address_items = s.walk("ipAddressIfIndex")
        for i in address_items:
            add_ip_from_oid(h_addresses, interfaces[int(i.value)-1], i.oid_index)
        oper_items = s.walk("ifOperStatus")
        res2[hostname] = {interfaces[int(i.oid_index)-1]:"up" if (i.value == '1') else "down" for i in oper_items}
    with open(file, "w") as f:
        json.dump(res1, f, indent=1)
        f.write("\n")
        json.dump(res2, f, indent=1)
        f.write("\n")

def plot_cpu(file, host):
    s = Session(hostname=host, community="public", version=2)
    x = []
    y = []
    t = time.time()
    for _ in range(12*2):
        x.append(time.time()-t)
        y.append(float(s.walk("cpmCPUTotal5secRev")[0].value))
        time.sleep(5)
    plt.plot(x, y)
    plt.title("CPU Utilization For R1 Over 2 Minutes")
    plt.xlabel("Time (sec)")
    plt.ylabel("CPU Utilization")
    plt.savefig(file)

def NMsnmp(files, hosts):
    json_file, img_file = files
    print("Writing SNMP for %d hosts to %s" % (len(hosts), json_file))
    write_snmp_to_file(json_file, hosts)
    print("Generating and saving CPU figure for %s to %s" % (hosts[0], img_file))
    plot_cpu(img_file, hosts[0])

if __name__ == "__main__":
    NMsnmp(("json.txt", "cpu.jpg"), hosts)
