# 🛡️ 06. Security Architecture & Infrastructure Performance Tuning
> **Edge AI Telegram Multimodal Translation and Web Integrated Management System Guide**

> 🌐 **Language / 언어 전환**: [English](./06_security_and_tuning_EN.md) | [한국어](./06_security_and_tuning.md)

---

## 🔗 Navigation
- [01. System Overview](./01_system_overview_EN.md)
- [02. System Architecture Blueprint](./02_system_architecture_EN.md)
- [03. Installation History](./03_installation_history_EN.md)
- [04. Upgrades & Evolution](./04_upgrades_and_evolution_EN.md)
- [05. Detailed Workflows](./05_detailed_workflows_EN.md)
- **[06. Security & Infrastructure Tuning](./06_security_and_tuning_EN.md)**
- [07. Operations & Deployment Guide](./07_operations_and_deployment_EN.md)
- [14. eBPF Cilium & AI Firewall + Telegram SOC](./14_ebpf_cilium_ai_firewall_and_telegram_soc_EN.md)

---

## 1. Multi-layered Security Defense

Security enforcement spans from the underlying Linux kernel and host OS up through the REST API ingress layers.

### 1.1 Host-Level SSH Brute-Force Defense (`setup_fail2ban.sh`)
Continuous Fail2ban daemon monitoring mitigates automated credential attacks across external networks:

- **Target Ports**: Non-standard management ports and standard SSH port probes.
- **Telemetry Parsing**: Streams `/var/log/auth.log` in real time; flags IP addresses incurring 5 consecutive failed authentications.
- **Mitigation Action**: Commits temporary rules directly into host firewall chains (`iptables`), completely isolating the client IP for 24 hours.
- **Daemon Status Verification**:
  ```bash
  sudo fail2ban-client status sshd
  ```

---

### 1.2 Web Dashboard Direct IP Scanning Mitigation
Eliminates opportunistic automated bot scans targeting naked server IP addresses:

- **Enforcement Rule**: Evaluates the HTTP `Host` header. Incoming traffic lacking verified domains (`edgeai.local`) is immediately dropped with `HTTP 403 Forbidden`.
- **Environment Configuration**: Configured seamlessly in `web-dashboard/deployment.yaml`:
  ```yaml
  env:
  - name: BLOCK_DIRECT_IP
    value: "true"
  - name: ALLOWED_DOMAIN
    value: "edgeai.local"
  ```

---

### 1.3 Web Login Brute-Force Barrier
Protects dashboard administrative credentials against automated credential stuffing:

- **Enforcement Rule**: An in-memory tracking dictionary locks out any client IP after 3 consecutive invalid authentication attempts.
- **Administrative Override**: Blocked IPs can be inspected and unlocked with a single click inside the Web Console Security tab.

---

## 2. 16 vCPU & 60GB RAM OS Kernel Optimization (`tune_memory.sh`)

High-throughput neural network inference demands aggressive memory bandwidth and minimized disk swap latency:

```bash
# /etc/sysctl.d/99-ram-optimization.conf

# 1. 60GB RAM Priority Allocation (Prevent Disk Swap)
vm.swappiness = 10                  # Delays disk swap until RAM reaches capacity
vm.vfs_cache_pressure = 50          # Retains filesystem inode/dentry caches in memory
vm.dirty_ratio = 20                 # Maximum active memory write buffer
vm.dirty_background_ratio = 5       # Background write thread trigger threshold

# 2. Concurrency & Network Socket Expansion
net.core.somaxconn = 4096           # Deepens TCP backlog queue
net.ipv4.tcp_max_syn_backlog = 4096 # Accommodates high-volume SYN handshake bursts
fs.file-max = 2097152               # Raises global system open file descriptor ceiling
```

### Apply Kernel Tuning
```bash
sudo chmod +x ~/tune_memory.sh
sudo ~/tune_memory.sh
```
Executes kernel state updates immediately without requiring server reboots.
