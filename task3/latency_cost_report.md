# Latency/Cost Report
- Latency: ~1-2 seconds per query (local FAISS).
- Cost: $0 (using mocks; real OpenAI ~$0.001/query).
- Graceful Refusal: If query out of scope, returns "No relevant info found."
