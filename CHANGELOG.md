# Changelog

All notable changes to this project will be documented in this file.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-06-03

First stable release of the CoreBase boilerplate. Covers all foundational
patterns for a production-ready multi-tenant SaaS: authentication, tenancy,
API tokens, inter-service communication, task scheduling, and real-time
notifications.

### Core Platform (S01–S09)

- Multi-tenant architecture with logical isolation per tenant
- Email-based authentication with JWT (HttpOnly cookies), email verification, password reset
- Tenant CRUD with role-based access (Owner / Admin / Member) and SuperAdmin bypass
- API Tokens as signed JWTs — offline validation in apiauth (FastAPI)
- Django Unfold admin with CoreBase branding

### Rate Limiting & Plans (S10–S11)

- Plans module — Free / Basic / Pro / Enterprise tiers managed via Django admin only
- Plans scoped to the user (not the tenant); limits shared across all user's tenants
- Redis plan cache invalidated immediately on plan change (downgrade takes effect instantly)
- Per-minute sliding window + per-hour/day fixed counters in apiauth (FastAPI)
- Rate limit usage visible in dashboard widget

### Dashboard & Widgets (S11)

- Dynamic widget system with auto-discovery (modules declare `widgets.py`)
- Widgets persisted in DB, user preferences preserved across sessions
- Staff-only widgets hidden from regular users

### Inter-Service Communication (S11–S12)

- Watchdog service: Redis Streams consumer for heartbeat and remote commands
- Three boilerplate patterns: (1) heartbeat/health, (2) internal Celery task, (3) external remote command
- Watchdog module in frontend — panel for service health, on-demand execution, and command results

### Jobs & Task Scheduling (S11–S12)

- Jobs list: central read-only viewer of all Celery task executions (Redis result backend)
- UserTask model links each task to its owner; users see only their own jobs
- Celery Beat — user-created cron jobs via frontend (select task, set frequency)
- Scheduled tasks self-register as UserTask; each execution appears in Jobs

### Notifications (S12)

- Real-time WebSocket push via Django Channels (channel per user)
- Toast notifications (floating, auto-dismiss, manual close)
- Notification bell with unread badge; historical inbox
- Retention policy: all unread + read from last 7 days (max 20 read)
- Deep links — click navigates to the source of the notification

### Operations (S12)

- Docker multi-stage builds: `development` (uvicorn + hot reload) and `production` (gunicorn / nginx)
- Clean migrations — one `0001_initial.py` per app
- Default admin created on first migrate (idempotent, configurable via env)
- robots.txt in frontend (public/) and API endpoint
- CoreBase branding across browser tab, Django admin, and navigation
