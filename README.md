# Dynamic Host Blocking System
## Author: Nakshathira Bharathi (PES2UG24AM096)
## Problem Statement
Block suspicious hosts dynamically based on traffic behavior.
## Setup
1. Install Mininet, Ryu
2. Run: `ryu-manager src/dynamic_blocker.py`
3. Run: `sudo python3 src/topology.py`
# Dynamic Host Blocking System - SDN Project

**Author:** Nakshathira Bharathi (PES2UG24AM096)

## Problem Statement
Implement an SDN-based system that dynamically detects suspicious hosts based on packet rate and blocks them by installing OpenFlow drop rules.

## Features
- Real-time traffic monitoring (packet counting per source IP)
- Automatic blocking when threshold exceeded (10 packets in 5 seconds)
- OpenFlow match-action: `priority=100,ip,nw_src=10.0.0.1 actions=drop`
- Event logging for auditing
- MAC learning for normal forwarding

## Setup & Execution

### Prerequisites
```bash
sudo apt install mininet openvswitch-switch wireshark iperf3 -y
git clone https://github.com/noxrepo/pox.git
cd pox
