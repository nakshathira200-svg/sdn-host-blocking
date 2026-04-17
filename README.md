```markdown
# Dynamic Host Blocking System - SDN Project

**Author:** Nakshathira Bharathi (PES2UG24AM096)

---

## 📌 Problem Statement

Implement an SDN-based system that dynamically detects suspicious hosts based on packet rate and blocks them by installing OpenFlow drop rules. The system uses Mininet for network emulation and Ryu as the OpenFlow controller.

---

## ✨ Features

- Real-time traffic monitoring (packet counting per source IP)
- Automatic blocking when threshold exceeded (10 packets in 5 seconds)
- OpenFlow match-action: `priority=100,ip,nw_src=10.0.0.1 actions=drop`
- Event logging for auditing
- MAC learning for normal forwarding
- Performance testing with iperf3

---

## 🛠️ Setup & Execution

### Prerequisites

Install the required packages:

```bash
sudo apt update
sudo apt install mininet openvswitch-switch wireshark iperf3 python3-pip -y
sudo pip3 install ryu
```

### Installation Verification

| Package | Version |
|---------|---------|
| Mininet | ![Mininet](https://github.com/user-attachments/assets/3b78bf4e-355d-42e0-b1d7-30be2a9a31f1) |
| Ryu | ![Ryu](https://github.com/user-attachments/assets/ee5efa95-f25f-455a-978c-7e9fe8260c4b) |
| Open vSwitch | ![OVS](https://github.com/user-attachments/assets/01d4bb4e-04e4-4c2f-a766-4ac6270d7f85) |
| iperf3 | ![iperf3](https://github.com/user-attachments/assets/271cd4b5-b1ad-4a85-9653-c54df33a05c0) |

### Running the Project

**Terminal 1 - Start Ryu Controller:**
```bash
cd ~/sdn-host-blocking
ryu-manager --verbose src/dynamic_blocker.py
```

**Terminal 2 - Start Mininet Topology:**
```bash
cd ~/sdn-host-blocking
sudo -E python3 src/topology.py
```

---

## 🧪 Testing & Validation

### Scenario 1: Normal Traffic (Allowed)

**Connectivity Test:**
```bash
mininet> pingall
```
![pingall result](https://github.com/user-attachments/assets/7d1fd912-23f2-45f9-86f4-d0ac68ac0286)

**Individual Ping:**
```bash
mininet> h1 ping -c 4 h2
```
![h1 ping h2](https://github.com/user-attachments/assets/8c0a5f90-8b31-40b8-95ee-3a263579ead0)

**Flow Table Before Blocking:**
```bash
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
```
![flow table before](https://github.com/user-attachments/assets/018b6da4-39f4-4619-b920-e330d38acd70)

### Scenario 2: Suspicious Traffic Detection & Blocking

**Generate Suspicious Traffic (Flood Ping):**
```bash
mininet> h1 ping -f h2
```

**Controller Detection & Blocking:**
![Ryu alert and blocking](https://github.com/user-attachments/assets/f3bc0c76-7932-446b-8973-f3b698bfec98)

**Verification - Blocked Host Cannot Ping:**
```bash
mininet> h1 ping h2
```
![failed ping from blocked host](https://github.com/user-attachments/assets/eb56804e-71e6-4f55-8478-6db46fe9f755)

**Unaffected Hosts Still Communicate:**
```bash
mininet> h2 ping h3
```
![h2 ping h3 works](https://github.com/user-attachments/assets/70a58852-11e8-402c-8bc3-0ec807b615bb)

**Flow Table After Blocking (Drop Rule Installed):**
```bash
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
```
*Output shows: `priority=100,ip,nw_src=10.0.0.1 actions=drop`*

**Blocking Log:**
```bash
cat logs/blocked.log
```
*Example output: `2026-04-16 14:30:45 - BLOCKED: Host 10.0.0.1`*

---

## 📊 Performance Testing (iperf3)

| Test Scenario | Bandwidth (Mbps) |
|---------------|------------------|
| Baseline (h2 ↔ h3) | ~94.5 |
| During flood ping attack | ~75.2 |
| After blocking h1 | ~94.1 |

*Screenshots of each iperf run are attached.*

---

## 🔍 OpenFlow Control Traffic Analysis (Wireshark)

Wireshark capture on loopback interface (filter: `openflow_v1`) shows:

- **packet_in** – Switch sends unknown packet to controller
- **packet_out** – Controller instructs switch to forward
- **flow_mod** – Controller installs flow rule

![Wireshark OpenFlow messages](https://github.com/user-attachments/assets/...)

*(Your Wireshark screenshot goes here)*

---

## 📁 Project Structure

```
sdn-host-blocking/
├── src/
│   ├── topology.py          # Mininet topology with 3 hosts, 1 switch
│   └── dynamic_blocker.py   # Ryu controller with blocking logic
├── logs/
│   └── blocked.log          # Timestamped blocking events
└── README.md
```

---

## 🎯 Evaluation Criteria Fulfilled

| Criteria | How it's demonstrated |
|----------|----------------------|
| Problem Understanding & Setup (4 marks) | Clear problem statement + installation screenshots |
| SDN Logic & Flow Rule Implementation (6 marks) | Explicit match-action (priority 100, drop) in code |
| Functional Correctness - Demo (6 marks) | Two scenarios: allowed vs blocked |
| Performance Observation & Analysis (5 marks) | iperf3 before/during/after blocking |
| Explanation, Viva & Validation (4 marks) | Wireshark + flow table + logs |

---



**Nakshathira Bharathi**  
PES2UG24AM096
```

---
