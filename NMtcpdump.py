from scapy.all import rdpcap
import sys

def NMtcpdump(file, ip):
    pkts = rdpcap(file)
    if ip == "4":
        arp_pkts = [pkt for pkt in pkts if "ARP" in pkt]
        macs = []
        for pkt in arp_pkts:
            if "who has" in pkt.summary():
                #packet is from C1
                macs.append(pkt["Ether"].dst)
        return macs
    elif ip == "6":
        icmp_pkts = [pkt for pkt in pkts if "ICMP" in pkt.summary()]
        macs = []
        for pkt in icmp_pkts:
            if "Echo Request" in pkt.summary():
                #packet is from router
                #prefix is 2001:db8:2:0
                parts = pkt["IPv6"].src[13:].split(":")
                p1 = hex(int(parts[0][:2],16) ^ 1 << 1)[2:]
                p2 = parts[0][2:]
                p3 = parts[1][:2]
                p4 = parts[2][2:]
                p5 = parts[3].zfill(4)[:2]
                p6 = parts[3].zfill(4)[2:]
                ipv6 = ":".join([p1,p2,p3,p4,p5,p6])
                if ipv6 not in macs:
                    macs.append(ipv6)
        return macs
if __name__ == "__main__":
    if (len(sys.argv) != 2) or (sys.argv[1] not in ("4", "6")):
        print("Usage: NMtcpdump.py {4 | 6}")
        exit(-1)
    if sys.argv[1] == "4":
        print(NMtcpdump("lab5.pcap", "4"))
    elif sys.argv[1] == "6":
        print(NMtcpdump("lab5v6.pcap", "6"))

