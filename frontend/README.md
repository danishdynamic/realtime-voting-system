# VoteLive Frontend

A modern, real time voting interface built with **React 18**, **TypeScript**, **Vite**, **Tailwind CSS**, **Zustand**, and **Framer Motion**.

[![React](https://img.shields.io/badge/react-18.2.0-blue?logo=react&logoColor=white)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/typescript-5.2.2-blue?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/vite-5.3.1-blue?logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/tailwindcss-3.6.2-blue?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![Zustand](https://img.shields.io/badge/zustand-4.4.1-blue?logo=zustand&logoColor=white)](https://github.com/pmndrs/zustand)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | React 18 + TypeScript |
| Build Tool | Vite |
| Styling | Tailwind CSS |
| State Management | Zustand |
| Animations | Framer Motion |
| Real-Time | Socket.IO Client |
| HTTP Client | Axios |
| Notifications | Sonner |
| Icons | Lucide React |
| Effects | Canvas Confetti |

---

## Quick Start

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The dev server starts at `http://localhost:3000`.

---

## Environment Variables

Create a `.env` file from `.env.example`:

```bash
VITE_API_URL=http://localhost:5000/api
VITE_WS_URL=http://localhost:8000
```

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Flask backend API base URL |
| `VITE_WS_URL` | Socket.IO WebSocket server URL |

---

## Project Structure

```mermaid
graph TD
    %% Global Entry & Layout
    subgraph Core ["🚀 App Core & Routing"]
        MAIN["main.tsx"] --> APP["App.tsx (Router)"]
        APP --> HOME_P["HomePage.tsx"]
        APP --> POLL_P["PollPage.tsx"]
        APP --> CREATE_P["CreatePollPage.tsx"]
    end

    %% Pages to Feature Components
    subgraph UI ["🎨 Component Hierarchy"]
        POLL_P --> LIVE_CNT["LiveCounter"]
        POLL_P --> VOTE_OPT["VoteOption"]
        POLL_P --> TIMER["CountdownTimer"]
        POLL_P --> WINNER["WinnerBanner"]
        CREATE_P --> FORM["CreatePollForm"]
        
        %% Primitives
        LIVE_CNT & VOTE_OPT & WINNER --> PRIMS["ui/ Primitives<br/>(Button, Card, Badge, ProgressBar)"]
    end

    %% State & Custom Hooks Layer
    subgraph Logic ["⚡ Hooks & State Layer"]
        POLL_P --> USE_POLL["usePoll.ts"]
        VOTE_OPT --> USE_VOTE["useVote.ts"]
        TIMER --> USE_COUNT["useCountdown.ts"]
        
        USE_POLL & USE_VOTE --> ZUSTAND["store/pollStore.ts<br/>(Zustand State)"]
    end

    %% API & Network Layer
    subgraph Services ["🔌 Infrastructure & Utilities"]
        USE_POLL --> SOCKET["lib/socket.ts<br/>(Socket.IO Client)"]
        USE_VOTE & FORM --> API["lib/api.ts<br/>(Axios API)"]
        
        API --> REST_BE[("Flask API")]
        SOCKET --> WS_BE[("WebSocket Server")]
        
        USE_VOTE --> UTILS["lib/utils.ts<br/>(cn, formatDuration, getWinner)"]
    end

    %% Styling and Types Across App
    TYPES["types/poll.ts"] -.-> Logic & UI
    CSS["index.css / Tailwind"] -.-> UI

    %% Styling Classes
    classDef entry fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    classDef ui fill:#1e293b,stroke:#818cf8,stroke-width:2px,color:#fff
    classDef logic fill:#1e293b,stroke:#fbbf24,stroke-width:2px,color:#fff
    classDef infra fill:#1e293b,stroke:#f43f5e,stroke-width:2px,color:#fff

    class MAIN,APP,HOME_P,POLL_P,CREATE_P entry
    class LIVE_CNT,VOTE_OPT,TIMER,WINNER,FORM,PRIMS ui
    class USE_POLL,USE_VOTE,USE_COUNT,ZUSTAND logic
    class SOCKET,API,UTILS,REST_BE,WS_BE infra
```

---

## Pages

### `/` — Home
- Hero section with CTA
- Tabbed poll grid: **All** / **Live** / **Ended**
- Auto-refreshes every 30 seconds
- Skeleton loading states

### `/poll/:id` — Vote
- Live countdown timer (turns red under 5 min)
- Vote buttons with animated progress bars
- Real time vote counts via WebSocket
- Confetti burst on vote
- Auto disables when poll ends
- Winner banner with trophy animation when closed

### `/create` — New Poll
- Question input
- Dynamic options (2 to 6, add/remove)
- Duration picker (5 min to 24 hours)
- Creator name (optional)
- Redirects to new poll on success

---

## Key Features

| Feature | How It Works |
|---------|--------------|
 | **Real Time Updates** | Socket.IO listens for `vote_update` events; Zustand updates global state |
| **Optimistic Voting** | UI updates immediately, rolls back on error |
| **Atomic Timer** | `useCountdown` hook syncs every second; expires trigger UI lock |
| **Winner Detection** | `getWinner()` handles ties and single winners |
| **Responsive** | Mobile first Tailwind; grid adapts 1→2→3 columns |
| **Accessible** | Keyboard navigable buttons, focus rings, ARIA labels |

---

## State Flow

```mermaid
graph TD
    A["👤 User Clicks 'Vote'"] --> B["⚡ useVote.vote() Triggered"]
    B --> C["📡 POST /api/polls/:id/vote"]
    
    C -->|HTTP 200/202 Success| D["🎉 Local UI Feedback"]
    
    subgraph Local ["Local Client Updates"]
        D --> D1["Zustand: setUserVote(pollId, option)"]
        D --> D2["🎉 Fire Confetti Burst"]
        D --> D3["🍞 Toast: 'Vote cast!'"]
    end
    
    C -.->|Async Event Ingestion| WS["🔌 Socket.IO Server Broadcasts 'vote_update'"]
    
    WS --> E["📥 Client Receives Socket Event"]
    
    subgraph Global ["Global Sync Across All Connected Users"]
        E --> F["Zustand: updatePollResults(pollId, results)"]
        F --> G["📊 UI Live Count Increment Real-Time"]
    end

    %% Styling
    classDef step fill:#1e293b,stroke:#38bdf8,stroke-width:2px,color:#fff
    classDef success fill:#1e293b,stroke:#22c55e,stroke-width:2px,color:#fff
    classDef broadcast fill:#1e293b,stroke:#fbbf24,stroke-width:2px,color:#fff

    class A,B,C step
    class D1,D2,D3 success
    class WS,E,F,G broadcast
```

---

## Build for Production

```bash
npm run build
```

Output goes to `dist/`. Serve with any static host (Vercel, Netlify, Nginx).

---

## Proxy Setup

Vite dev server proxies `/api` to the Flask backend:

```ts
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

No CORS issues in development.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `Cannot find module '@/'` | Restart Vite dev server; path aliases are pre-configured |
| Socket not connecting | Check `VITE_WS_URL` matches your WebSocket server port |
| CORS errors in production | Ensure Flask `CORS(app)` allows your frontend domain |
| Polls not appearing | Verify `GET /api/polls` returns array with `status` field |

---

## License

MIT — same as the backend.
