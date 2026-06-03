# CoreBase

Production-ready multi-tenant SaaS boilerplate. Clone, configure, ship.

## What's included

| Capability | Detail |
|---|---|
| Multi-tenancy | Logical isolation — shared DB, per-tenant scope enforcement |
| Authentication | JWT (HttpOnly cookies), email verification, password reset |
| Roles | Owner / Admin / Member per tenant + SuperAdmin bypass |
| API Tokens | Signed JWT, offline validation in apiauth |
| Plans | Free / Basic / Pro / Enterprise — scoped to user, managed via admin |
| Rate limiting | Per-minute sliding window + per-hour/day quotas in apiauth |
| Jobs | Central Celery task viewer — users see only their own |
| Scheduling | User-created cron jobs via UI; each run appears in Jobs |
| Notifications | Real-time WebSocket toasts + historical bell inbox |
| Dashboard | Dynamic widgets — modules declare their own, auto-discovered |
| Watchdog | Inter-service monitor — heartbeat, internal tasks, remote commands |

## Services

```
corebase/
├── backend/      Django 5 + DRF + Celery + Django Channels
├── frontend/     Vue 3 + Vite + TailwindCSS
├── apiauth/      FastAPI — token validation + rate limiting (read-only)
└── watchdog/     Python service — Redis Streams consumer + command executor
```

## Quick start

```bash
cp .env.example .env          # fill in secrets
docker compose up --build
```

Open http://localhost:3000 — default admin: `admin@corebase.local` / `P4ssw0rd!`

> Change credentials immediately. The default admin is created by the initial migration only if no superuser exists.

## Environment

| File | Purpose |
|---|---|
| `docker-compose.yml` | Development (uvicorn + hot reload + Vite dev server) |
| `docker-compose.prod.yml` | Production overrides (gunicorn + nginx static) |

```bash
# Production
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

## Key environment variables

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret — required |
| `FASTAPI_SECRET_KEY` | Shared key for JWT API tokens — required |
| `POSTGRES_*` | Database connection |
| `REDIS_URL` | Redis (broker + channel layer + result backend) |
| `DEFAULT_ADMIN_EMAIL` | First superuser email (default: `admin@corebase.local`) |
| `DEFAULT_ADMIN_PASSWORD` | First superuser password (default: `P4ssw0rd!`) |

## Architecture patterns

Three inter-service communication patterns are implemented as boilerplate references:

1. **Heartbeat** — Django → Redis Stream → Watchdog → `service:watchdog:last_seen`
2. **Internal task** — Django view → Celery task → Redis result → Jobs list
3. **Remote command** — Django → Redis Stream → Watchdog executes → Redis result → UI

Each pattern is demonstrated in the Watchdog module and visible in the Jobs list.

## Default credentials

| Role | Email | Password |
|---|---|---|
| Superadmin | `admin@corebase.local` | `P4ssw0rd!` |

## License

MIT
