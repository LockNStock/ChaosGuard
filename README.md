# ChaosGuard: Adaptive Stochastic Scheduler for Autonomous Agents

**ChaosGuard** is an advanced, environment-aware scheduling engine designed to mimic human cognitive irregularity. By merging **Stochastic Processes** with **Bayesian Inference**, it provides a robust solution for autonomous agents (LLM scrapers, RPA suites) to evade sophisticated statistical bot detection systems.

---

## 🚀 The Core Philosophy

Standard automation fails because it is "too regular." Even with simple random delays, bots often fall into statistical patterns easily flagged by frequency analysis. **ChaosGuard** introduces **"Tactical Breathing"** — a non-linear, high-entropy rhythm that is mathematically indistinguishable from a focused human user.

### Key Technical Pillars:
*   **Dynamic Sliding Prime Windows**: Utilizes a full domain of **1,229 primes (up to 10,000)** to generate rotating sub-pools, eliminating fixed statistical edges and discrete frequency peaks.
*   **Dual-Profile Tactical Switching**: Supports **Smooth (Long-term)** and **Contrast (Short-term)** interaction profiles to mimic specific human cognitive states during Web/LLM sessions.
*   **Inhomogeneous Poisson Process**: Transforms discrete prime delays into continuous exponential distributions (Poisson sampling) to eliminate mechanical "fingerprints."
*   **Bayesian Risk Feedback Loop**: A real-time governor that "senses" environment pressure (server latency/HTTP 429s) and updates a posterior risk probability to auto-adjust mission density.

---

## 📊 Visualizing "Tactical Breathing"

ChaosGuard dynamically adjusts task density based on environmental risk. Below is a conceptual representation of the Bayesian response:

```text
Density 3 |     █          █   █                     
Density 2 |  █  █  █    █  █   █             █       
Density 1 | ███ █ ███  ██ ████ █            ███  █   
Risk Lv   |    [Safe]      [🔥 HIGH RISK]   [🌊 Recovery]
Mode      |    [Hyper]     [Chaos Mode]     [Cruise]
```

---

## 🛠️ Quick Start

Integrate the **ChaosGovernor** into your agent loop in minutes:

```python
from chaos_governor import ChaosGovernor

# Initialize with a 1.5s latency baseline
gov = ChaosGovernor(baseline_latency=1.5)

while tasks_remaining:
    # 1. Get high-entropy delay
    delay = gov.get_next_delay()
    time.sleep(delay)
    
    # 2. Execute Task & Measure Latency
    start_ts = time.time()
    result = agent.execute_task()
    latency = time.time() - start_ts
    
    # 3. Update Bayesian Governor
    gov.observe_and_update(latency)
    print(f"Current Risk Level: {gov.risk_level:.1%}")
```

---

## ⚖️ License
This project is licensed under the MIT License.
