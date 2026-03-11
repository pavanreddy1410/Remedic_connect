# Remedic Connect

Remedic Connect is a local-first healthcare microservices platform with FastAPI services, MongoDB, API Gateway, and React/Tailwind frontend.

## ✅ What is now implemented

- JWT + bcrypt authentication (`/api/auth/register`, `/api/auth/login`)
- Role-based authorization across services
- Patient order/report APIs
- Lab report upload with file storage (`UploadFile`) into `reports/`
- Pharmacy order processing APIs
- Admin approvals and audit-log APIs
- AI analytics with:
  - Drug interaction rules
  - **IsolationForest anomaly detection** for lab metrics
- API rate limiting using **slowapi** (example `5 requests/second` on critical endpoints)
- Structured service logging using **loguru**
- Docker support for all services + MongoDB + frontend via `docker compose`

## Local Run (Windows CMD)

### Option A: Docker (recommended)

```bat
docker compose up --build
```

Services:
- API Gateway: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- MongoDB: `mongodb://localhost:27017`

### Option B: Manual Uvicorn

```bat
cd backend\auth_service && uvicorn main:app --reload --port 8001
cd backend\patient_service && uvicorn main:app --reload --port 8002
cd backend\lab_service && uvicorn main:app --reload --port 8003
cd backend\pharmacy_service && uvicorn main:app --reload --port 8004
cd backend\ai_service && uvicorn main:app --reload --port 8005
cd backend\admin_service && uvicorn main:app --reload --port 8006
cd backend\api_gateway && uvicorn main:app --reload --port 8000
```

Frontend:

```bat
cd frontend
npm install
npm start
```

## Key APIs (via gateway)

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/lab/reports/upload` (multipart upload)
- `POST /api/patient/orders`
- `PATCH /api/pharmacy/orders/{order_id}`
- `POST /api/ai/drug-interactions`
- `POST /api/ai/lab-analysis`
- `POST /api/admin/approve/{target_role}`

For protected routes, pass:

`Authorization: Bearer <token>`
