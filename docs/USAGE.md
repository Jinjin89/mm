# Music Platform Monorepo – Usage Guide

This document explains how to bootstrap the development environment, run the available services, and execute automated tests for the self-hosted music platform stack.

## Repository Layout

```
backend/   # Django + Celery application and project configuration
mobile/    # Expo (React Native) client for iOS, Android, and web preview
web/       # Next.js web client
```

Supporting files include:

- `docker-compose.yml` – service orchestration for databases, storage, backend, and frontends.
- `Makefile` – convenience wrappers around common `docker compose` commands.
- `.env.example` – template of required environment variables.

## Prerequisites

- Docker Engine 24+ and Docker Compose v2 (recommended for the full stack).
- Node.js 18+ and Yarn/NPM if you prefer to run web/mobile clients without Docker.
- Python 3.11+ if you need to execute the Django backend directly.

## Environment Setup

1. Duplicate the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Adjust any secrets, passwords, or hostnames to fit your local environment. The defaults are suitable for a single-machine developer setup.

## Starting the Full Stack with Docker

Use the provided Make target to build images and launch every service:

```bash
make up
```

The following endpoints will become available once the containers finish booting:

- Django API (health check): <http://localhost:8000/api/health/>
- Next.js web client: <http://localhost:3000>
- Expo web preview: <http://localhost:19006>
- MinIO console: <http://localhost:9001> (credentials `music` / `musicsecret`)

You can open a shell inside running containers:

```bash
make backend-shell   # Attach to the Django container
make celery-shell    # Attach to the Celery worker
```

To stop and remove all containers, networks, and volumes created by Compose:

```bash
make down
```

## Running Without Docker (SQLite Fallback)

If Docker is unavailable, you can still run the Django test suite locally using SQLite:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
USE_SQLITE_FOR_TESTS=1 python backend/manage.py migrate
USE_SQLITE_FOR_TESTS=1 python backend/manage.py test
```

The `USE_SQLITE_FOR_TESTS` environment variable triggers a lightweight in-memory database configuration defined in `backend/music_platform/settings.py`.

## Testing Shortcut

A convenient Make target wraps the Django test command (runs within Docker when available):

```bash
make tests
```

## Frontend Development Notes

### Next.js Web

Install dependencies and run the development server without Docker:

```bash
cd web
npm install
npm run dev
```

The web client reads the API base URL from `NEXT_PUBLIC_API_BASE_URL` (defined in `.env` and injected via Docker Compose for containerised runs).

### Expo Mobile

This repository intentionally **omits binary image assets** (icons and splash screens) to avoid issues with environments that disallow binary files. Expo falls back to default visuals when these assets are absent.

To customise them:

1. Place your PNG files inside `mobile/assets/`.
2. Update `mobile/app.json` with the filenames (see `mobile/assets/README.md`).
3. Restart the Expo development server or rebuild the project.

Launch Expo locally with:

```bash
cd mobile
npm install
npm run start
```

## Troubleshooting

- **Binary file errors when creating PRs** – ensure no binary artefacts are tracked by Git. The repository keeps only text-based placeholders for assets; add your own binaries locally without committing them.
- **Docker unavailable** – use the SQLite fallback commands above.
- **Port conflicts** – stop any existing services listening on the ports listed in the Docker section or edit `docker-compose.yml` to remap ports.

## Next Steps

The README (`README.MD`) outlines the broader project milestones. Extend the backend and frontend applications iteratively to satisfy those milestones once the environment is confirmed working.
