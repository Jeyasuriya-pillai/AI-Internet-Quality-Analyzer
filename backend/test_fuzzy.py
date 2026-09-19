from fuzzy_logic import calculate_quality


result = calculate_quality(
    latency_value=40,
    jitter_value=5,
    packet_loss_value=0
)

print("Fuzzy Logic Result")
print("------------------")

print("Quality Score:", result["score"])
print("Quality:", result["category"])