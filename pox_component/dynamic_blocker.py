# pox/ext/dynamic_blocker.py
# Dynamic Host Blocking System - Corrected version
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import dpid_to_str
import time

log = core.getLogger()

class DynamicBlocker(object):
    def __init__(self):
        core.openflow.addListeners(self)
        # Store MAC learning tables per datapath ID (dpid)
        self.mac_tables = {}      # dpid -> {mac: port}
        # Packet counters per source IP
        self.packet_count = {}
        self.blocked_ips = set()
        self.THRESHOLD = 10
        self.INTERVAL = 5
        self.last_reset = time.time()
        log.info("Dynamic Host Blocker Started (Threshold: %d pkts/%d sec)", 
                 self.THRESHOLD, self.INTERVAL)

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s connected", dpid_to_str(event.dpid))
        # Initialize MAC table for this switch
        self.mac_tables[event.dpid] = {}
        # Install default table-miss flow: send all packets to controller
        msg = of.ofp_flow_mod()
        msg.priority = 0
        msg.actions.append(of.ofp_action_output(port=of.OFPP_CONTROLLER))
        event.connection.send(msg)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port
        conn = event.connection
        dpid = conn.dpid

        # Learn MAC address
        src_mac = packet.src
        self.mac_tables[dpid][src_mac] = in_port
        log.debug("Learned MAC %s on port %d", src_mac, in_port)

        # Handle IPv4 packets for blocking logic
        ip_pkt = packet.find('ipv4')
        if ip_pkt:
            src_ip = str(ip_pkt.srcip)
            dst_ip = str(ip_pkt.dstip)

            # Check if source IP is blocked
            if src_ip in self.blocked_ips:
                log.info("Dropping packet from blocked host %s", src_ip)
                return  # Drop silently

            # Packet counting
            now = time.time()
            if now - self.last_reset > self.INTERVAL:
                self.packet_count.clear()
                self.last_reset = now
                log.debug("Reset packet counters")

            self.packet_count[src_ip] = self.packet_count.get(src_ip, 0) + 1
            count = self.packet_count[src_ip]
            log.debug("Packet from %s -> %s (count: %d)", src_ip, dst_ip, count)

            # Check threshold
            if count >= self.THRESHOLD:
                self.blocked_ips.add(src_ip)
                # Install drop flow on the switch
                flow = of.ofp_flow_mod()
                flow.priority = 100
                flow.match.dl_type = 0x0800  # IPv4
                flow.match.nw_src = IPAddr(src_ip)
                # No actions = drop
                conn.send(flow)
                log.warning("BLOCKED: %s (drop flow installed)", src_ip)
                # Log to file
                try:
                    with open("/home/nakshathira/sdn-host-blocking/logs/blocked.log", "a") as f:
                        f.write("%s - BLOCKED: %s\n" % (time.ctime(), src_ip))
                except:
                    pass
                return  # Don't forward this packet

        # Forward the packet (MAC learning based)
        dst_mac = packet.dst
        if dst_mac in self.mac_tables[dpid]:
            out_port = self.mac_tables[dpid][dst_mac]
            log.debug("Forwarding to known port %d", out_port)
        else:
            out_port = of.OFPP_FLOOD
            log.debug("Unknown MAC, flooding")

        # Create packet_out message
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = event.ofp
        msg.in_port = in_port
        conn.send(msg)

def launch():
    core.registerNew(DynamicBlocker)
