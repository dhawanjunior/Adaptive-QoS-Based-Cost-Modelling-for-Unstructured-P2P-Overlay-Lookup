import random
import heapq
import numpy as np


# 1. DATA MODELS


class Peer:
    def __init__(self, node_id):
        self.id = node_id
        self.past_response = random.uniform(0.3, 0.9)


class Link:
    def __init__(self, bandwidth, latency, congestion):
        self.bandwidth = bandwidth      # Mbps
        self.latency = latency          # ms
        self.congestion = congestion    # 0–1

# 2. OVERLAY NETWORK


def build_overlay(num_nodes=60, avg_degree=4):
    graph = {i: {} for i in range(num_nodes)}
    peers = {i: Peer(i) for i in range(num_nodes)}

    for i in range(num_nodes):
        neighbors = random.sample(
            [n for n in range(num_nodes) if n != i],
            k=random.randint(2, avg_degree)
        )
        for n in neighbors:
            graph[i][n] = Link(
                bandwidth=random.uniform(1, 25),
                latency=random.uniform(10, 200),
                congestion=random.uniform(0, 1)
            )
    return graph, peers

# 3. NORMALIZATION


def norm_bandwidth(bw, max_bw=25):
    return 10 - int((bw / max_bw) * 9)

def norm_latency(lat, max_lat=200):
    return int((lat / max_lat) * 9) + 1

# 4. FIXED COMPOSITE COST (BASELINE)

def fixed_cost(link, peer):
    bw = norm_bandwidth(link.bandwidth)
    lat = norm_latency(link.latency)
    pr = int(peer.past_response * 10)

    return 0.65 * bw + 0.20 * lat + 0.15 * pr

# 5. ADAPTIVE COST (YOUR EXTENSION)

def adaptive_weights(file_size_mb, congestion):
    # File-size awareness
    if file_size_mb >= 500:      # bulk transfer
        wb, wl, wp = 0.70, 0.20, 0.10
    else:                        # delay-sensitive
        wb, wl, wp = 0.55, 0.30, 0.15

    # Congestion shifts importance
    shift = congestion * 0.10
    wb -= shift
    wl += shift

    return wb, wl, wp


def adaptive_cost(link, peer, file_size_mb):
    bw = norm_bandwidth(link.bandwidth)
    lat = norm_latency(link.latency)
    pr = int(peer.past_response * 10)

    wb, wl, wp = adaptive_weights(file_size_mb, link.congestion)

    return wb * bw + wl * lat + wp * pr


# 6. QoS THRESHOLD (CONTROLLED FORWARDING)


def qos_threshold(mode, file_size_mb):
    
    if mode == "fixed":
        return 6.5
    else:
        return 6.0 if file_size_mb >= 500 else 5.5



# 7. QUERY ROUTING


def route_query(graph, peers, src, ttl, mode, file_size_mb=None):
    visited = set()
    pq = [(0, src, ttl)]
    messages = 0
    total_cost = 0
    threshold = qos_threshold(mode, file_size_mb)

    while pq:
        cost, node, ttl = heapq.heappop(pq)
        if ttl <= 0 or node in visited:
            continue

        visited.add(node)
        messages += 1
        total_cost += cost

        for nbr, link in graph[node].items():
            if nbr in visited:
                continue

            if mode == "fixed":
                c = fixed_cost(link, peers[nbr])
            else:
                c = adaptive_cost(link, peers[nbr], file_size_mb)

            if c <= threshold:
                heapq.heappush(pq, (cost + c, nbr, ttl - 1))

    return total_cost, messages




def run_experiment():
    graph, peers = build_overlay()
    trials = 60
    ttl = 4
    file_size = 100024 

    fixed_msgs, fixed_costs = [], []
    adapt_msgs, adapt_costs = [], []

    for _ in range(trials):
        src = random.randint(0, len(peers) - 1)

        fc, fm = route_query(graph, peers, src, ttl, "fixed")
        ac, am = route_query(graph, peers, src, ttl, "adaptive", file_size)

        fixed_msgs.append(fm)
        fixed_costs.append(fc)

        adapt_msgs.append(am)
        adapt_costs.append(ac)

    print("\n<-----SIMULATION RESULTS------>\n")

    print("Baseline: Fixed Composite Cost")
    print(f"Avg Message Overhead : {np.mean(fixed_msgs):.2f}")
    print(f"Avg Route Cost       : {np.mean(fixed_costs):.2f}\n")

    print("Proposed: Adaptive Composite Cost")
    print(f"Avg Message Overhead : {np.mean(adapt_msgs):.2f}")
    print(f"Avg Route Cost       : {np.mean(adapt_costs):.2f}\n")

    print("<------ COMPARISON ------>")
    print(f"Message Reduction : {((np.mean(fixed_msgs)-np.mean(adapt_msgs))/np.mean(fixed_msgs))*100:.2f}%")
    print(f"Cost Improvement  : {((np.mean(fixed_costs)-np.mean(adapt_costs))/np.mean(fixed_costs))*100:.2f}%")



if __name__ == "__main__":
    run_experiment()
