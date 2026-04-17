

---

```markdown
# Dynamic Host Blocking System – SDN Project

**Author:** Nakshathira Bharathi (PES2UG24AM096)  
**Controller:** POX (OpenFlow 1.0)  
**Emulator:** Mininet  

---

## Problem Statement

Design and implement an SDN‑based system that:

- Monitors network traffic in real time  
- Detects suspicious hosts based on packet rate (10 packets in 5 seconds)  
- Dynamically installs OpenFlow drop rules to block those hosts  
- Logs blocking events for auditing  
- Allows normal traffic to continue for unaffected hosts  

The solution must demonstrate controller–switch interaction, explicit match‑action rules, and validation with tools like `ping`, `ovs-ofctl`, and Wireshark.

---

## Setup & Execution

### 1. Install dependencies (Ubuntu 20.04/22.04)

```bash
sudo apt update
sudo apt install mininet openvswitch-switch wireshark iperf3 -y
```

### 2. Clone and prepare POX controller

```bash
cd ~
git clone https://github.com/noxrepo/pox.git
cd pox
mkdir -p pox/ext
# Copy the dynamic_blocker.py into pox/ext/
# (The file is included in this repository under pox_component/)
```

### 3. Prepare the Mininet topology

```bash
cd ~/sdn-host-blocking   # or wherever you placed this repository
# Ensure src/topology.py is present (provided in this repo)
```

### 4. Run the controller (Terminal 1)

```bash
cd ~/pox
./pox.py ext.dynamic_blocker
```

```

<img width="625" height="208" alt="Screenshot 2026-04-17 at 11 13 32 AM" src="https://github.com/user-attachments/assets/eb13545d-0a90-47c9-b2c9-ebe7feadfc3b" />
### 5. Run Mininet topology (Terminal 2)

```bash
cd ~/sdn-host-blocking
sudo python3 src/topology.py
```

<img width="627" height="445" alt="Screenshot 2026-04-17 at 11 13 52 AM" src="https://github.com/user-attachments/assets/e6bcb1cb-36bd-4dbb-a49f-0e60fd686dff" />
---

## Testing & Validation

### Scenario 1 – Normal traffic (allowed)

In the Mininet CLI:

```bash
mininet> pingall
```
<img width="627" height="238" alt="Screenshot 2026-04-17 at 11 15 21 AM" src="https://github.com/user-attachments/assets/6b14f609-6e94-4b45-9e5e-f01647b848a8" />



```bash
mininet> h1 ping -c 4 h2
```

**Expected result:** 4 successful replies.

```
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=1.94 ms
...
4 packets transmitted, 4 received, 0% packet loss
```

<img width="627" height="210" alt="Screenshot 2026-04-17 at 11 15 43 AM" src="https://github.com/user-attachments/assets/3ce4e0a9-4f19-4a8b-b369-e53ab1861c03" />
### Scenario 2 – Suspicious traffic detection & blocking

In Mininet CLI, generate a flood ping from `h1`:

```bash
mininet> h1 ping -f h2
```

After 5‑10 seconds, the POX controller terminal (Terminal 1) shows:

<img width="647" height="229" alt="Screenshot 2026-04-17 at 11 16 03 AM" src="https://github.com/user-attachments/assets/b020df90-c6c0-4aea-bda3-9752b3aeb2b8" />


**[Screenshot 5 – POX blocking alert]**

Stop the flood ping with `Ctrl+C`, then test connectivity from blocked host:

```bash
mininet> h1 ping -c 4 h2
```

**Expected result:** 100% packet loss.



<img width="627" height="129" alt="Screenshot 2026-04-17 at 11 16 42 AM" src="https://github.com/user-attachments/assets/b55c9f80-f886-421a-8042-12f2fde4b162" />
Verify that unaffected hosts can still communicate:

```bash
mininet> h2 ping -c 4 h3
```

<img width="630" height="215" alt="Screenshot 2026-04-17 at 11 17 18 AM" src="https://github.com/user-attachments/assets/f3939bd5-2e86-4cdd-b764-4ebeb5d34175" />


**[Screenshot 7 – successful ping between h2 and h3]**

### Verify OpenFlow drop rule (Terminal 3)

```bash
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
```

**Expected output – shows the blocking flow:**


<img width="626" height="179" alt="Screenshot 2026-04-17 at 11 17 52 AM" src="https://github.com/user-attachments/assets/25565932-f7c1-421c-99a9-4225944589c2" />
### Check blocking log

```bash
cat ~/sdn-host-blocking/logs/blocked.log
```

**Expected output:**

```
Fri Apr 17 04:30:54 2026 - BLOCKED: 10.0.0.1
```

<img width="630" height="103" alt="Screenshot 2026-04-17 at 11 18 41 AM" src="https://github.com/user-attachments/assets/5ab7fcc4-ce0d-4d5e-aa96-3a8683746f51" />

### Wireshark capture (controller‑switch communication)

- Start Wireshark on loopback interface (`lo`), filter `openflow_v1`.
- Run `h1 ping h2` in Mininet.

Observe `OFPT_ECHO_REQUEST` / `OFPT_ECHO_REPLY` messages (or `packet_in`/`flow_mod`).



<img width="625" height="534" alt="Screenshot 2026-04-17 at 11 19 06 AM" src="https://github.com/user-attachments/assets/61431206-c187-43c4-a454-0e782a0d373c" />
---

## Repository Structure

```
.
├── README.md
├── src/
│   └── topology.py                 # Mininet topology (3 hosts, 1 switch)
├── pox_component/
│   └── dynamic_blocker.py          # POX controller with blocking logic
├── logs/
│   └── blocked.log                 # Example log file (auto‑generated)
└── (other folders – ignore)
```

---

## Summary of Results

| Feature | Status |
|---------|--------|
| Normal traffic allowed | ✅ |
| Suspicious host detected (10 packets / 5 sec) | ✅ |
| Drop flow installed (`priority=100,ip,nw_src=10.0.0.1 actions=drop`) | ✅ |
| Blocked host cannot communicate | ✅ |
| Unaffected hosts continue normal communication | ✅ |
| Event logged with timestamp | ✅ |
| OpenFlow control traffic visible in Wireshark | ✅ |

---

## How to Run the Live Demo

1. **Terminal 1** – start POX: `./pox.py ext.dynamic_blocker`  
2. **Terminal 2** – start Mininet: `sudo python3 src/topology.py`  
3. In Mininet: `pingall` → show normal operation  
4. `h1 ping -f h2` → trigger blocking (watch POX terminal)  
5. `h1 ping h2` → show failure  
6. `h2 ping h3` → show unaffected hosts  
7. `sudo ovs-ofctl dump-flows s1` → show drop rule  
8. (Optional) show Wireshark capture.

---

## References

- POX Controller: https://github.com/noxrepo/pox  
- Mininet: http://mininet.org  
- OpenFlow 1.0 Specification

---
```

---

