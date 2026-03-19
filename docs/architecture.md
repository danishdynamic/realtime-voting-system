## Architecture Overview

Client (React Dashboard)
      │
      ▼
Flask API
      │
      ▼
Kafka Topic: votes
      │
      ▼
Vote Consumer
      │
      ▼
Redis (live counters)
      │
      ▼
WebSocket updates