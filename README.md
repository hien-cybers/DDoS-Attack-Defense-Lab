# 🛡️ DoS/DDoS Attack Simulation & Defense Lab

**Author:** [@hien-cybers](https://github.com/hien-cybers)  
**Role:** Red Team (Attacker) & Blue Team (Defender)

---

## ⚠️ DISCLAIMER

This project is created **EXCLUSIVELY for educational purposes, academic learning, and system security research**. 

Any unauthorized execution of the source code contained in this repository against real-world production systems without prior written consent is strictly illegal. 

**The author assumes no liability or responsibility for any misuse or damage caused by this tool.**

---

## 📖 Project Overview

This lab environment simulates various **Denial of Service (DoS/DDoS)** attack scenarios targeting a production Web Server, while concurrently deploying robust mitigation strategies via firewall engineering and Linux kernel tuning.

### 🔁 The Lab Workflow Consists of 2 Phases:

* **Red Team (Attacker):**
  * Developing custom Python-based exploit scripts targeting:
    * Layer 4 (Transport Layer)
    * Layer 7 (Application Layer)

* **Blue Team (Defender):**
  * Implementing advanced mitigation and defensive controls:
    * Linux Kernel Tuning (TCP SYN Cookies)
    * Rate Limiting & Connection Threshold Controls

---

## 🏗️ Lab Topology & Architecture

* **Attacker Infrastructure:**
  * Operating System: Kali Linux
  * Tooling: Python3, Scapy Engine, Multi-threaded Sockets

* **Victim Infrastructure:**
  * Operating System: Ubuntu Server 24.04 LTS
  * Service: Apache2 Web Server

* **Monitoring & Analysis Suite:**
  * Wireshark (Packet Inspection)
  * htop (Resource Monitoring)
  * netstat (Session Triage)
  * iptables (Firewall Management)

---

## ⚔️ Scenario 1: TCP SYN Flood Attack (Layer 4)

### 🧠 Core Principle

This scenario exploits the structural mechanics of the standard TCP 3-Way Handshake:

1. The Attacker floods the target with a high volume of `SYN` packets.
2. The Server responds to each request with a corresponding `SYN-ACK` packet.
3. The Attacker deliberately **withholds the final `ACK`** packet.

➡️ The Server is forced to maintain thousands of half-open connections in the `SYN_RECV` state ➡️ **Total RAM exhaustion/Backlog queue starvation**.

### 🛠️ Tools Used

```bash
syn_flood.py  # Custom Python exploit script leveraging the Scapy network stack
```

### 📊 Post-Attack Verification / Results

* The target server becomes heavily saturated with unresolved `SYN_RECV` states.
* The TCP connection backlog queue becomes fully saturated.
* Critical system resource degradation occurs, rejecting legitimate connections.

<img width="1601" height="818" alt="6" src="https://github.com/user-attachments/assets/c9395be6-6e31-40eb-a53e-e0b0fbaae17e" />

---

## ⚔️ Scenario 2: HTTP Flood Attack (Layer 7)

### 🧠 Core Principle

* Leverages high-concurrency **multi-threading** execution models.
* Generates thousands of application-layer valid HTTP `GET` requests simultaneously.
* Forces the Web Server into heavy processing loops (I/O and rendering overhead) ➡️ **100% CPU exhaustion**.

### 🛠️ Tools Used

```bash
http_flood.py  # Custom Python multi-threaded script using low-level sockets
```

### 📊 Post-Attack Verification / Results

* CPU utilization spikes instantly to 100%.
* System Load Average surpasses critical baseline thresholds.
* The Web Server experiences massive response latency or drops offline entirely.

<img width="1698" height="920" alt="Screenshot 2026-03-26 124754" src="https://github.com/user-attachments/assets/0b656c5d-6017-47f4-b965-ec1aa44cd561" />

---

## 🛡️ Scenario 3: Defensive Engineering (Blue Team)

---

### 🔐 3.1. Mitigating SYN Floods via Kernel Tuning (Layer 4)

### 💡 Mitigation Strategy

Activating the **TCP SYN Cookies** defense mechanism:

* The kernel stops allocating space in the RAM backlog immediately upon receiving a `SYN` packet.
* Instead, it generates a cryptographically signed cookie inside the TCP sequence number sent back.
* System resources are allocated only when a valid final `ACK` verifying that cookie is returned by the client.

➡️ **Effectively neutralizes IP spoofing and half-open resource depletion.**

### ⚙️ Sysctl Kernel Configuration

```bash
# Enable TCP SYN Cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1

# Maximize the SYN backlog queue capacity
sudo sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# Restrict SYN-ACK retry limits to drop dead connections faster
sudo sysctl -w net.ipv4.tcp_synack_retries=2
```

---

### 🌐 3.2. Mitigating HTTP Floods via Iptables Connlimit (Layer 7)

### 💡 Mitigation Strategy

Because Layer 7 HTTP Floods use fully established, valid TCP connections, Layer 4 SYN Cookies cannot detect them.

➡️ **Solution:**
Deploy the native Linux Netfilter firewall (`iptables`) paired with the `connlimit` module to enforce a strict threshold on concurrent HTTP TCP channels per unique IP address.

---

### ⚙️ Iptables Firewall Configuration

```bash
# Drop any inbound traffic from an individual IP exceeding 20 concurrent connections on Port 80
sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 20 -j DROP
```

---

### 📊 Defensive Verification / Results

* Aggressive request spammers are immediately dropped at the network firewall layer.
* Massive reduction in infrastructure overhead:
  * CPU usage drops from 100% saturation back to baseline stability.
* Web Server operational performance and availability are fully restored.
* Live monitoring via `htop` indicates:
  * Fluid system processing loops.
  * Total resolution of hardware resource starvation.

---

## ✅ Summary Matrix

| Scenario | Attack Vector | Mitigation Strategy |
| :--- | :--- | :--- |
| **SYN Flood** | Layer 4 (Transport) | TCP SYN Cookies & Backlog Queue Tuning |
| **HTTP Flood** | Layer 7 (Application) | Netfilter Iptables Connlimit Adjustments |

---

## 🚀 Future Roadmap & Hardening

* Implement `fail2ban` jail integration for automated, dynamic malicious IP banning.
* Deploy Layer 7 rate-limiting directly at the reverse proxy layer using `nginx`.
* Integrate a Web Application Firewall (WAF) to inspect malicious HTTP payload structures.
* Expand stress-testing coverage using advanced performance tools:
  * `hping3`
  * `ab` (Apache Benchmark)
  * `locust`
