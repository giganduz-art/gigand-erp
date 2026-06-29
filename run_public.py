"""GIGAND ERP — Internetga chiqarish (ngrok orqali)"""
import threading
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

def start_server():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

def start_tunnel():
    time.sleep(3)
    try:
        from pyngrok import ngrok
        tunnel = ngrok.connect(8000)
        print("=" * 60)
        print(f"  GIGAND ERP — INTERNET ORQALI OCHILDI!")
        print(f"  Public URL: {tunnel.public_url}")
        print(f"  Lokal: http://localhost:8000")
        print(f"  Bu linkni telefondan ham ochish mumkin!")
        print("=" * 60)
    except Exception as e:
        print(f"Ngrok xatolik: {e}")
        print("Lokal server ishlayapti: http://localhost:8000")

if __name__ == "__main__":
    print("GIGAND ERP v2.0 — Ishga tushirilmoqda...")
    t = threading.Thread(target=start_tunnel, daemon=True)
    t.start()
    start_server()
