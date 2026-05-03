# 🗳️ Real-Time Voting System 

A distributed, event-driven real-time voting platform designed for high throughput, low latency, and horizontal scalability.

<img width="986" height="152" alt="Screenshot 2026-03-27 201439" src="https://github.com/user-attachments/assets/61a02ec1-4202-48bd-a2c3-9b7708a6499d" />

## 🎯 Problem Statement

- Design a system that:

- Handles high-frequency concurrent votes

- Provides real-time updates to users

- Scales to millions of users

- Ensures fault tolerance and reliability

### 🚀 Tech Stack

| Layer	| Technology
|-------|------------
| Frontend	| React
| API Layer	| Flask
| Messaging	| Kafka
| Processing	| Kafka Consumers
| Cache/Store	| Redis
| Realtime	| WebSockets
| Infra	| Docker

### 🏗️ High-Level Architecture

        ┌──────────────┐
        │   Frontend   │
        │   (React)    │
        └──────┬───────┘
               │ HTTP (Vote)
               ▼
        ┌──────────────┐
        │  Flask API   │
        │ (Producer)   │
        └──────┬───────┘
               │ Publish Event
               ▼
        ┌──────────────┐
        │    Kafka     │
        │  (Broker)    │
        └──────┬───────┘
               │ Consume
               ▼
        ┌──────────────┐
        │  Consumers   │
        └──────┬───────┘
               │ Update
               ▼
        ┌──────────────┐
        │    Redis     │
        │ (Cache + PS) │
        └──────┬───────┘
               │ Publish
               ▼
        ┌──────────────┐
        │ WebSocket    │
        │   Server     │
        └──────┬───────┘
               │ Push
               ▼
        ┌──────────────┐
        │   Frontend   │
        └──────────────┘


### 🔍 Low-Level Design (LLD)

🔹 1. Vote API (Flask)

>Endpoint:

- POST /vote

>Responsibilities:

- Validate request

- Produce event to Kafka

- Return immediate response (non-blocking)

>Payload:

```
{
  "user_id": "u123",
  "poll_id": "p456",
  "option": "A",
  "timestamp": "2026-03-19T10:00:00Z"
}
```

>🔹 2. Kafka Design

- Topic: votes

- Partition Key: poll_id

- Ensures ordering per poll

>Why Kafka?

- Decouples services

- Handles traffic spikes

- Supports replay

>🔹 3. Consumer Workers

Responsibilities:

- Consume vote events

- Aggregate counts

- Update Redis

Scaling:

- Consumer groups

- Partition-based parallelism

🔹 4. Redis Design

Data Model:
```
Key: poll:{poll_id}
Type: HASH

{
  "A": 120,
  "B": 95
}

```

Pub/Sub Channel:

poll_updates

>🔹 5. WebSocket Server

Responsibilities:

- Subscribe to Redis Pub/Sub

- Broadcast updates to clients

### 🔄 Sequence Diagrams

### 🧩 1. Vote Submission Flow

``` mermaid
sequenceDiagram
    participant F as Frontend (React)
    participant A as Flask API
    participant K as Kafka Broker
    participant C as Consumer Worker
    participant R as Redis (Cache)

    Note over F, R: Event-Driven Architecture
    F->>A: POST /vote (poll_id, option)
    activate A
    A->>K: Produce "vote_event"
    K-->>A: Ack
    A-->>F: 202 Accepted
    deactivate A

    K->>C: Consume Event
    activate C
    C->>R: INCRBY poll:{id}:{option}
    R-->>C: Update Success
    deactivate C
```

### ⚡ 2. Real-Time Update Flow
``` mermaid
sequenceDiagram
    participant R as Redis (Pub/Sub)
    participant W as WebSocket Server
    participant F as Frontend (React)

    R->>W: Publish: poll_updated_event
    activate W
    W->>F: Broadcast via Socket.IO
    deactivate W
    Note right of F: UI Updates Automatically
```

### 🔁 3. End-to-End Flow

>User → React → Flask → Kafka → Consumer → Redis → WebSocket → Reactjs

### ⚙️ Setup Instructions

- 🐳 Prerequisites

> Docker, Docker Compose, Python 3.9+ , Reactjs

- 🐳 1. Start Infrastructure (Kafka + Redis)

``` bash
docker-compose up -d
➤ docker-compose.yml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
```

``` bash
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```
  
### 🧠 2. Backend Setup

>> Run ``` bash py -m backend.infrastructure.database.seed ``` to initialize the local database i.e seed_db.py.
  
```
cd backend

python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### ▶️ Run Backend Services

### Flask API
```
py app.py
```

### Kafka Consumer
```
py consumer.py
```

### WebSocket Server
``` 
py websocket_server.py
```

### 🌐 3. Frontend Setup
``` bash
cd frontend 

npm install
npm start

```

### 🔌 4. Environment Variables
``` bash
- Backend .env

KAFKA_BROKER=localhost:9092
REDIS_HOST=localhost
REDIS_PORT=6379

- Frontend .env

REACT_APP_API_URL=http://localhost:5000

REACT_APP_WS_URL=ws://localhost:8000

```

### ✅ 5. Verify Setup

- Kafka → localhost:9092 

- Redis → localhost:6379

- Flask → http://localhost:5000

- WebSocket → ws://localhost:8000

- React → http://localhost:3000 

### 📈 Scalability

| Component | Strategy |
|-----------|----------|
| Flask API | Stateless scaling |
| Kafka | Partitioning |
| Consumers | Consumer groups |
| Redis | Clustering |
| WebSocket | Horizontal scaling |

### ⚠️ Bottlenecks & Solutions

| Problem | Solution |
|--------|----------|
| Kafka lag | Increase partitions |
| Redis overload | Sharding |
| WebSocket scaling | Load balancer |
| Duplicate votes | Idempotency keys |

### 🔐 Reliability

- At-least-once delivery (Kafka)

- Retry mechanisms

- Graceful failure handling

### 🚀 Future Enhancements

- Authentication & authorization

- Rate limiting

- Persistent DB (PostgreSQL)

- Kubernetes deployment

- Monitoring (Prometheus + Grafana)

### 👿 ScreenShots

<img width="1350" height="1042" alt="Screenshot 2026-03-27 201351" src="https://github.com/user-attachments/assets/431e4e8e-5888-45d8-bf3d-61661f9a507a" />


### 🤝 Contributing Guidelines

We welcome contributions to improve the Real-Time Voting System!

### 🚀 How to Contribute

- Fork the repository

- Create a new branch:
```
git checkout -b feature/your-feature-name
```
- Make your changes

- Commit your changes:
```
git commit -m "Add: your feature description"
```
- Push to your fork:
```
git push origin feature/your-feature-name
```
- Open a Pull Request to merge your branch into ```main```

