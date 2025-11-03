## 🛠️ animatic_vision_server

**animatic_vision_server** is the FastAPI backend for the Animatic Vision platform. It powers authentication, project management, and story segmentation workflows, integrating with MySQL, Redis, Alembic, and Celery. The API is designed to work seamlessly with the Next.js client using secure HttpOnly cookies.

## 🚀 Features
- 🔐 **Authentication** — Register, login, logout, refresh tokens, change/forgot/reset password
- 📁 **Projects** — Create, list, fetch by ID, update status, delete
- 🎬 **Scenes / Segmentation** — Endpoint to trigger AI-based story segmentation (processor scaffold)
- 🗃️ **Persistence** — SQLAlchemy models with Alembic migrations (MySQL via PyMySQL)
- ⚡ **Redis Integration** — Token blacklist and Celery broker/backend
- 🌐 **CORS-ready** — Preconfigured for local Next.js development

## 🏗️ Tech Stack
| Layer | Technology |
|-------|------------|
| Framework | FastAPI / Starlette |
| ORM & Migrations | SQLAlchemy / Alembic |
| Cache/Queue | Redis / Celery |
| Auth | JWT (HS256), HttpOnly cookies, Argon2 hashing |
| Email | SMTP (via Celery task) |

## 📂 Project Structure
```
app/
  main.py                 # App factory, CORS, lifespan, routers
  core/                   # security, middleware, logger, responses, exceptions
  database/               # session, models (user, project, scene, asset), redis
  modules/
    auth/                 # controller, service, repository, schemas
    project/              # controller, service, repository, schemas
    scene/                # controller, service, repository, schemas
    story/processor.py    # segmentation processor scaffold
  tasks/                  # celery tasks (emails)
alembic/                  # migrations
```

## ⚙️ Setup & Installation

1. Clone the server
   ```bash
   git clone https://github.com/your-org/animatic_vision_server.git
   cd animatic_vision_server
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\\Scripts\\activate  # Windows PowerShell
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables
   Create a `.env` file in the project root:
   ```env
   # General
   ENVIROMENT=development
   SECRET_KEY=replace-with-strong-random-secret

   # Database (MySQL)
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=animatic_vision

   # Redis
   REDIS_HOST=127.0.0.1
   REDIS_PORT=6379
   REDIS_USERNAME=
   REDIS_PASSWORD=

   # SMTP (for password reset emails via Celery task)
   SMTP_EMAIL=you@example.com
   SMTP_PASSWORD=your_app_password

   # Client URL (for reset link generation)
   FRONTEND_URL=http://localhost:3000
   ```

5. Run database migrations
   ```bash
   alembic upgrade head
   ```

6. Start the development server
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Server runs at `http://127.0.0.1:8000`.

## 🔌 Real-Time / Workers (Optional)
- Start Celery worker (uses Redis as broker and backend):
  ```bash
  python -m app.celery_worker worker -Q emails --loglevel=info
  ```

## 🔑 Authentication
- Login sets `access_token` (1h) and `refresh_token` (7d) as HttpOnly cookies.
- When `access_token` expires, call `GET /auth/refresh-token` to rotate tokens.
- Logout blacklists the access token in Redis.

## 🌍 CORS
Allowed origins (see `app/main.py`):
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Add your client URL to `origins` if different.

## 📡 API Summary

Auth (`/auth`)
- `POST /register` — Create user
- `POST /login` — Sets cookies with JWTs
- `GET /refresh-token` — Rotate tokens via refresh cookie
- `POST /logout` — Blacklist current access token
- `GET /me` — Get authenticated user
- `PUT /change-password` — Change password
- `POST /forgot-password` — Send reset email
- `POST /reset-password` — Reset via token

Projects (`/projects`)
- `POST /` — Create project
- `GET /` — List projects for user
- `GET /{project_id}` — Get project (with scenes)
- `PATCH /{project_id}/status` — Update status
- `DELETE /{project_id}` — Delete

Scenes (`/projects/segment`)
- `POST /segment` — Trigger story segmentation for a project

Health
- `GET /test` — Simple health check

> Protected routes require the `access_token` cookie. Clients must send requests with credentials included.

## 🧾 License
This project is licensed under the MIT License. See `LICENSE` for details.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to improve.

