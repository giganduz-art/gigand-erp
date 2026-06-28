"""GIGAND ERP — Serverni ishga tushirish"""
import uvicorn
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

if __name__ == "__main__":
    print("=" * 50)
    print("  GIGAND ERP v2.0 — Ishga tushirilmoqda...")
    print("  http://localhost:8000")
    print("  API: http://localhost:8000/api/stats")
    print("  Docs: http://localhost:8000/docs")
    print("=" * 50)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
