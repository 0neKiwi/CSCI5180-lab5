import napalm
import re
from netmiko import ConnectHandler

ip_r4 = "198.51.100.4"
cred = "abc"
client_ids = ["0072.32", "0072.33"]
macs = ["01ca.0231.b100.00", "01ca.0331.c000.00"]

def NMdhcpserver(ip_r4, u, p, custom=True):
    name_r5 = "R5"
    ip_r5 = "N/A"
    driver = napalm.get_network_driver("ios")
    r4 = driver(hostname=ip_r4, username=u, password=p)
    r4.open()
    res = list(r4.cli(["show cdp neighbors"]).values())[0]
    for line in res.splitlines():
        if re.match(r"^R5", line) is not None:
            name_r5 = line.split()[0]
            break
    res = list(r4.cli(["show cdp entry %s" % (name_r5)]).values())[0]
    for line in res.splitlines():
        if re.match(r"[ ]*IPv6 address:.*(global unicast)", line) is not None:
            ip_r5 = line.split()[2].lower()
            break
    r4.close()
    try:
        r5 = ConnectHandler(host=ip_r5, username=cred, password=cred, device_type="cisco_ios")
    except:
        raise RuntimeError("Could not SSH into %s" % (ip_r5))
    ids = client_ids if custom else macs
    res = r5.send_config_set(["ip dhcp pool r2", "host 10.1.1.12 255.255.255.0", "client-identifier %s" % (ids[0])])
    res = r5.send_config_set(["ip dhcp pool r3", "host 10.1.1.13 255.255.255.0", "client-identifier %s" % (ids[1])])
    res = r5.send_config_set(["ip dhcp pool 5180", "network 10.1.1.0 /24"])
    res = r5.send_config_set(["int fa0/0", "no shutdown", "ip address 10.1.1.5 255.255.255.0"])
    res = r5.send_command("show ip dhcp binding")
    r5.disconnect()
    ips = []
    for line in res.splitlines():
        if re.match(r"^10.1.1.[0-9]*.*", line) is not None:
            ips.append(line.split()[0])
    return ips

if __name__ == "__main__":
    print(NMdhcpserver(ip_r4, cred, cred))

