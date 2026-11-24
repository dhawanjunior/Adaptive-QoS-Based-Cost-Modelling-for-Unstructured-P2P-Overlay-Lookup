****Adaptive QoS-Aware Routing in Unstructured P2P Overlay Networks****

This project presents a simulation-based study of query routing in unstructured peer-to-peer (P2P) overlay networks, focusing on the limitations of static composite cost routing under real-world network conditions. The work proposes and evaluates an adaptive QoS-aware routing model that dynamically adjusts routing decisions based on file size characteristics and instantaneous network congestion.

**Background and Motivation**

Classical shortest-path routing approaches, while theoretically optimal, often degrade in effectiveness under congestion, heterogeneous link conditions, and dynamic workloads. Inspired by prior work on adaptive lookup mechanisms in unstructured overlays, this project investigates how static cost weighting fails to scale when network conditions fluctuate.

The central question addressed is:

How can routing decisions be adapted to better reflect real network behavior while reducing message overhead and routing cost?

**System Model**
Overlay Network

Randomly generated unstructured P2P overlay

Each peer maintains a historical response score to represent reliability

Each link models:

Bandwidth (Mbps)

Latency (ms)

Congestion level (0–1)

Routing Constraints

TTL-limited query propagation

Priority-queue-based routing

Visited-node tracking to avoid loops

QoS threshold-based controlled forwarding

**Routing Cost Models**

Baseline: Fixed Composite Cost

A static weighted combination of:

Normalized bandwidth

Normalized latency

Peer past-response score

This model reflects conventional composite routing metrics that do not adapt to traffic patterns or congestion.

**Proposed: Adaptive QoS-Aware Cost Model**

The adaptive model dynamically adjusts routing weights based on:

File size

Bulk transfers prioritize bandwidth

Delay-sensitive transfers prioritize latency

Network congestion

Weight is shifted from bandwidth toward latency under congestion

This enables routing decisions that better reflect current network conditions and application requirements.

**Experimental Setup**

Multiple randomized trials with different source peers

Comparison between fixed and adaptive routing modes

Metrics evaluated:

Average message overhead

Average routing cost

**Results**

The adaptive routing strategy consistently outperforms fixed composite cost routing:

~25% reduction in message overhead

~30–34% reduction in routing cost for large file transfers

Improved scalability under congested network conditions

These results demonstrate that context-aware routing significantly improves efficiency in unstructured P2P overlays.

**Key Insights**

Static routing metrics fail to capture dynamic network behavior

File-size awareness is critical for realistic traffic modeling

Congestion-aware weight adaptation reduces unnecessary message propagation

QoS thresholds enable controlled forwarding without sacrificing reachability

**Purpose**

This project bridges the gap between theoretical routing optimality and real-world network behavior, highlighting the importance of adaptive, system-level routing design. It serves as a foundation for further exploration into delay decomposition, real-time traffic modeling, and scalable distributed systems.
