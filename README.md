Traffic Classification System using SDN (POX)


 Problem Statement:
Design and implement a Software Defined Networking (SDN) solution to classify network traffic based on protocol type. The system should identify TCP, UDP, and ICMP packets, maintain statistics, and analyze traffic distribution using an OpenFlow controller.

 Objectives:
Classify packets into TCP, UDP, and ICMP
Maintain and display real-time traffic statistics
Demonstrate controller–switch interaction
Implement flow rules using OpenFlow
Analyze traffic behavior in a virtual network

 Tools & Technologies:
Mininet – Network emulator
POX Controller – SDN controller
OpenFlow Protocol – Flow rule management
Python – Controller implementation
Ubuntu (VM) – Execution environment
 System Overview

The POX controller listens for PacketIn events from the OpenFlow switch. For each incoming packet:

The controller extracts the IP header
Identifies protocol (TCP/UDP/ICMP)
Updates corresponding counters
Installs flow rules for efficient forwarding
Forwards packets based on learned MAC addresses


 Setup & Execution:
▶️ Start Controller
cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 traffic_classifier.traffic_classifier_pox

▶️ Run Mininet Topology
sudo mn --topo single,2 --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk
 Traffic Generation
🔹 ICMP (Ping)
mininet> h1 ping -c 3 h2
🔹 TCP Traffic
mininet> h2 iperf -s &
mininet> h1 iperf -c h2
🔹 UDP Traffic
mininet> h1 iperf -u -c h2

Expected Output:
Controller Logs
Packet: ICMP
Packet: TCP
Packet: UDP

Stats -> TCP: X, UDP: Y, ICMP: Z
Flow Table Verification
sudo ovs-ofctl dump-flows s1


 Proof of Execution:
Controller Running




ICMP Test




TCP Traffic




UDP Traffic




Flow Table




 Performance Observation:
Efficient packet classification in real-time
Reduced controller load after flow installation
Accurate tracking of traffic distribution

Filters:
icmp → ICMP packets
tcp → TCP packets
udp → UDP packets

 Conclusion:
The project demonstrates how SDN enables centralized traffic monitoring and classification. The POX controller dynamically processes packets, installs flow rules, and maintains protocol-wise statistics, ensuring efficient network behavior.

 References:
POX Controller Documentation
Mininet Documentation
OpenFlow Specification
