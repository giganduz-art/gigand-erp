# GIGAND ERP v2.0

Professional ERP dastur — GIGAND XOLDING uchun.

## Deploy (Render.com — bepul)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/giganduz-art/gigand-erp)

## Lokal ishga tushirish

```bash
pip install -r backend/requirements.txt
python run.py
```

http://localhost:8000 da ochiladi.

## Login

| Login | Parol | Rol |
|-------|-------|-----|
| admin | gigand2026 | Admin |
| rustam | rustam123 | Manager |
| chori | chori123 | Kassir |

## API

- Swagger docs: `/docs`
- Stats: `/api/stats`
- Dashboard: `/api/dashboard`

## Texnologiyalar

- Backend: Python FastAPI
- Database: SQLite (lokal) / PostgreSQL (cloud)
- Frontend: Vanilla HTML/JS
- Auth: JWT
