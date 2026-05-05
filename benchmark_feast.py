"""
Standalone Feast online lookup latency benchmark — run outside Jupyter.
Measures single lookup + 100-call P50/P95/P99 without notebook overhead.
"""
import time
from pathlib import Path

from feast import FeatureStore

REPO_ROOT = Path(__file__).resolve().parent
FEAST_DIR = REPO_ROOT / "app" / "feast_repo"

print(f"Feast repo: {FEAST_DIR}")
fs = FeatureStore(repo_path=str(FEAST_DIR))

REQUEST_FEATURES = [
    "user_profile_features:reading_speed_wpm",
    "user_profile_features:preferred_language",
    "user_profile_features:topic_affinity",
    "query_velocity_features:queries_last_hour",
    "query_velocity_features:distinct_topics_24h",
]

print("\n=== Warming up (10 calls) ===")
for i in range(10):
    fs.get_online_features(
        features=REQUEST_FEATURES,
        entity_rows=[{"user_id": f"u_{i:03d}"}],
    )
print("Warmup done.")

print("\n=== Single lookup ===")
t0 = time.perf_counter()
response = fs.get_online_features(
    features=REQUEST_FEATURES,
    entity_rows=[{"user_id": "u_001"}],
)
single_latency_ms = (time.perf_counter() - t0) * 1000
features = response.to_dict()
print(f"Single lookup: {single_latency_ms:.2f}ms")
sample = {k: v[0] for k, v in list(features.items())[:2]}
print(f"Sample features: {sample}")

print("\n=== Batch latency benchmark (100 lookups) ===")
latencies = []
for i in range(100):
    t0 = time.perf_counter()
    response = fs.get_online_features(
        features=REQUEST_FEATURES,
        entity_rows=[{"user_id": f"u_{i:03d}"}],
    )
    latencies.append((time.perf_counter() - t0) * 1000)
    _ = response.to_dict()

latencies.sort()
p50 = latencies[50]
p95 = latencies[95]
p99 = latencies[99]

print(f"Online lookup latency over 100 calls:")
print(f"  P50 = {p50:.2f}ms")
print(f"  P95 = {p95:.2f}ms")
print(f"  P99 = {p99:.2f}ms")

if p99 < 10:
    print(f"\n✓ PASS — online lookup P99 < 10ms ({p99:.2f}ms)")
else:
    print(f"\n✗ WARN — P99 = {p99:.2f}ms (exceeds 10ms target)")