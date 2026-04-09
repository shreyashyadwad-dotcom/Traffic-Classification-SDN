from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4

log = core.getLogger()

# MAC learning table
mac_to_port = {}

# Counters
tcp_count = 0
udp_count = 0
icmp_count = 0

def _handle_PacketIn(event):
    global tcp_count, udp_count, icmp_count

    packet = event.parsed
    if not packet:
        return

    in_port = event.port

    # Learn MAC address
    mac_to_port[packet.src] = in_port

    # Get IPv4 packet
    ip = packet.find('ipv4')

    if ip:
        if ip.protocol == 6:
            tcp_count += 1
            proto = "TCP"
        elif ip.protocol == 17:
            udp_count += 1
            proto = "UDP"
        elif ip.protocol == 1:
            icmp_count += 1
            proto = "ICMP"
        else:
            proto = "OTHER"

        log.info("Packet: %s", proto)
        log.info("Stats -> TCP: %d, UDP: %d, ICMP: %d",
                 tcp_count, udp_count, icmp_count)

    # Decide output port
    if packet.dst in mac_to_port:
        out_port = mac_to_port[packet.dst]
    else:
        out_port = of.OFPP_FLOOD

    # Install flow rule
    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet, in_port)
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Traffic Classifier POX Controller Started")
