# Real-Time Voting System — Backend

A distributed, event driven backend for real-time polling built with **Flask**, **Redis**, **Kafka**, and **SQLite**.

[![Docker](https://img.shields.io/badge/docker-1.41.0-blue?logo=docker&logoColor=white)
](https://www.docker.com/)
[![Python](https://img.shields.io/badge/python-3.11.6-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.2.5-blue?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Redis](https://img.shields.io/badge/redis-7.2.0-blue?logo=redis&logoColor=white)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/kafka-3.6.0-blue?logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![SQLite](https://img.shields.io/badge/sqlite-3.43.1-blue?logo=sqlite&logoColor=white)](https://www.sqlite.org/)

## Architecture

```mermaid
graph TD
    subgraph ClientLayer ["Client Layer"]
        REACT["React<br/>(Client)"]
    end

    subgraph Ingestion ["Ingestion & Streaming"]
        FLASK["Flask API<br/>(Producer)"]
        KAFKA["Kafka<br/>(Topic)"]
    end

    subgraph Realtime ["Real-time & State"]
        WS["WebSocket<br/>Server"]
        REDIS[("Redis<br/>(Cache+PS)")]
    end

    %% Flow Connections
    REACT -->|"HTTP"| FLASK
    FLASK -->|"Publish"| KAFKA
    KAFKA -->|"Consume"| WS
    WS -->|"Socket.IO Emit"| REACT
    WS <-->|"Pub/Sub"| REDIS

    %% Styling
    classDef client fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    classDef service fill:#1e293b,stroke:#818cf8,stroke-width:2px,color:#fff
    classDef streaming fill:#1e293b,stroke:#fbbf24,stroke-width:2px,color:#fff
    classDef storage fill:#1e293b,stroke:#f43f5e,stroke-width:2px,color:#fff

    class REACT client
    class FLASK,WS service
    class KAFKA streaming
    class REDIS storage
```

## Tech Stack

| Layer        | Technology |
|--------------|------------|
| API          | Flask      |
| Message Bus  | Kafka      |
| Cache / RT   | Redis      |
| Database     | SQLite     |
| Real-Time    | Socket.IO  |
| Infra        | Docker     |

## Quick Start

### 1. Start Infrastructure

```bash
docker-compose up -d
```

This starts Zookeeper, Kafka, and Redis.

### 2. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Seed the Database

```bash
python -m backend.infrastructure.database.seed
```

### 4. Run Services

Run each in a separate terminal:

```bash
# Flask API
python run.py

# Kafka Consumer
python -m backend.app.consumers.vote_consumer

# WebSocket Server
python -m backend.app.api.websocket_server
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/polls` | Create a new poll |
| GET | `/polls` | List all polls with status |
| GET | `/polls/<id>` | Get poll detail with timer status |
| POST | `/polls/<id>/vote` | Cast a vote (atomic, one per user) |
| GET | `/polls/<id>/results` | Get live vote counts |

## Vote Flow

1. **Client** sends vote to Flask API
2. **Redis SETNX** atomically checks if user already voted
3. **SQLite** persists the vote record
4. **Kafka** receives the vote event for async processing
5. **Consumer** increments Redis hash and emits via Socket.IO
6. **All clients** receive live update instantly

## Anti-Cheat Measures

- **Redis atomic lock** (`SETNX`) prevents race condition double voting
- **Consumer deduplication** ignores duplicate Kafka events
- **Time-gated voting** — polls auto close at `end_time`
- **DB rollback** on Redis lock if SQLite write fails

## Environment Variables

```bash
KAFKA_BROKER=localhost:9092
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Project Structure

```
backend/
├── app/
│   ├── api/              # Flask routes & WebSocket
│   ├── consumers/        # Kafka consumers
│   ├── domain/           # Entities (Poll, Vote, Option)
│   ├── producers/        # Kafka producers
│   ├── repositories/     # Abstract interfaces
│   └── services/         # Business logic
├── infrastructure/
│   ├── db/               # SQLite setup
│   ├── models/           # SQLAlchemy models
│   ├── redis/            # Redis client
│   └── repositories/     # Concrete implementations
├── run.py                # Flask entry point
└── requirements.txt
```

## Testing the Fix

1. Double click a vote button fast — second click rejected
2. Refresh and retry same poll — blocked
3. Stop consumer, vote, restart — no duplicates
4. Break SQLite path — Redis lock rolls back, user can retry
