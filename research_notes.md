# Research Notes: The Mathematics of Chaos Scheduling

This document outlines the theoretical foundations behind the ChaosGuard scheduling engine.

## 1. Prime Number De-synchronization
The choice of prime numbers (up to 1000) as the base for delays is a strategic decision to avoid **Harmonic Coupling**. 
Most server-side monitoring systems use fixed sampling windows (e.g., 1-minute or 5-minute buckets). By using prime numbers, we ensure that our task triggering frequency rarely aligns with these fixed windows, preventing the accumulation of "frequency spikes" that WAFs (Web Application Firewalls) look for.

## 2. Inhomogeneous Poisson Process (IPP)
While the prime pools provide the "skeleton" of the delay, the **Exponential Distribution** provides the "flesh." 
Mathematically, the time between events in a Poisson process follows an exponential distribution. By sampling `delay = -ln(U) * base_delay`, we ensure that the inter-task intervals are truly continuous. This "smears" the prime numbers across the time axis, creating a statistical profile that mimics the jitter found in human browsing patterns.

## 3. Dynamic Sliding Windows (The "Mood" Model)
Instead of fixed pools (e.g., Small, Medium, Large), ChaosGuard uses **Dynamic Sliding Windows**. 
Every cycle, the system picks a starting index and a window length (typically 5-20 primes). This represents the "Local Behavioral Context." This prevents the bot from ever falling into a "steady state" of delays, as the available palette of time intervals is constantly shifting.

## 4. Bayesian Risk Adaptation
The Governor treats "System Detection" as a hidden state with a dynamic probability.
- **Prior**: Initial belief about safety (e.g., 5%).
- **Likelihood**: Probability of observing high latency or error codes given that the system is being throttled.
- **Posterior**: Updated risk score.
The system uses this posterior to shift its sliding window toward higher primes (slowing down) or suppressing the "Burst" probability. This is a form of **Closed-Loop Control** rarely seen in open-source automation tools.

## 5. Miller's Law and Cognitive Load
The window length of 5-20 is inspired by cognitive psychology (Miller's Law), simulating the limited set of options a human usually considers at any given moment. This ensures "Local Consistency" but "Global Chaos."
