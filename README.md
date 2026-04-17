

---

## 🔍 Analysis of Screenshots

From the text you pasted:

| Screenshot filename | What it actually shows | Correct section title |
|---------------------|------------------------|----------------------|
| `10.54.08 AM.png` | POx controller starting, switch connected, Mininet topology creation | **Controller & Switch Connection** (or Running the Project) |
| `10.54.17 AM.png` | `pingall` success + `h1 ping -c 4 h2` success (0% loss) | **Scenario 1 – Connectivity Test** and **Individual Ping** |
| `10.54.30 AM.png` | `pingall` (unclear), then `h1 ping -c 4 h2` → 100% loss (blocked), then `h2 ping h3` success | **Blocked Host Cannot Ping** + **Unaffected Hosts Still Communicate** |
| `10.54.40 AM.png` | `ovs-ofctl dump-flows` shows drop rule (`priority=100,ip,nw_src=10.0.0.1 actions=drop`) + log file content | **Flow Table After Blocking** + **Blocking Log** |
| `10.55.01 AM.png` | Again shows blocked ping and drop rule (duplicate) | Same as above – can be omitted or merged |
| `10.55.15 AM.png` | Performance table (text) + Wireshark placeholder + project structure | **Performance Testing** and **Wireshark** |

> ⚠️ **Note:** Your controller screenshot shows **POx**, not Ryu. The project requirement allows Ryu or POX, so that’s fine. But make sure your code matches the controller you actually used.

---

## ✅ Corrected README (with proper image titles)

Copy the entire block below into your `README.md`.  
**Replace the placeholder `image-url-...` with your actual GitHub image URLs** (the ones that look like `https://github.com/user-attachments/assets/...`).

```markdown
# Dynamic Host Blocking System - SDN Project

**Author:** Nakshathira Bharathi (PES2UG24AM096)

---

## 📌 Problem Statement

Implement an SDN-based system that dynamically detects suspicious hosts based on packet rate and blocks them by installing OpenFlow drop rules. The system uses Mininet for network emulation and POX as the OpenFlow controller.

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

### Prerequisites Installation

*(Screenshots of version checks go here – you already have them from earlier)*

### Running the Project

**Terminal 1 – Start Controller (POx):**
```bash
cd ~/pox
./pox.py ext.dynamic_blocker
```

**Terminal 2 – Start Mininet Topology:**
```bash
cd ~/sdn-host-blocking
sudo python3 src/topology.py
```

### Controller & Switch Connection

![Controller and switch connection](image-url-10.54.08)

---

## 🧪 Testing & Validation

### Scenario 1: Normal Traffic (Allowed)

**Connectivity Test (`pingall`)**

![pingall success](image-url-10.54.17-part1)

**Individual Ping (`h1 ping -c 4 h2`)**

![h1 ping success](image-url-10.54.17-part2)

---

### Scenario 2: Suspicious Traffic Detection & Blocking

**Generate Suspicious Traffic (Flood Ping):**
```bash
mininet> h1 ping -f h2
```

**Blocked Host Cannot Ping:**

![h1 ping fails](image-url-10.54.30-part1)

**Unaffected Hosts Still Communicate:**

![h2 ping h3 works](image-url-10.54.30-part2)

**Flow Table After Blocking (Drop Rule Installed):**

```bash
sudo ovs-ofctl dump-flows s1 -O OpenFlow13
```

![Flow table with drop rule](image-url-10.54.40-part1)

**Blocking Log:**

```bash
cat logs/blocked.log
```

![Blocking log entries](image-url-10.54.40-part2)

---

## 📊 Performance Testing (iperf3)

| Test Scenario | Bandwidth (Mbps) |
|---------------|------------------|
| Baseline (h2 ↔ h3) | ~94.5 |
| During flood ping attack | ~75.2 |
| After blocking h1 | ~94.1 |

*(Insert your iperf3 screenshots here – you can place them under this table)*

---

## 🔍 OpenFlow Control Traffic Analysis (Wireshark)

Wireshark capture on loopback interface (filter: `openflow_v1`) shows:

- **packet_in** – Switch sends unknown packet to controller
- **packet_out** – Controller instructs switch to forward
- **flow_mod** – Controller installs flow rule

**Wireshark capture while running `mininet> h1 ping h2`:**

![Wireshark OpenFlow messages](image-url-wireshark)

> 👉 You said *"mininet> h1 ping h2 - wireshark under this rn"* – please upload your Wireshark screenshot and replace `image-url-wireshark` with its actual URL.

---

## 📁 Project Structure

```
sdn-host-blocking/
├── src/
│   ├── topology.py          # Mininet topology
│   └── dynamic_blocker.py   # POX controller logic
├── logs/
│   └── blocked.log
└── README.md
```

---

## 📦 GitHub Repository

[https://github.com/nakshathira200-svg/sdn-host-blocking](https://github.com/nakshathira200-svg/sdn-host-blocking)

---

## 👩‍💻 Author

**Nakshathira Bharathi**  
PES2UG24AM096
```

