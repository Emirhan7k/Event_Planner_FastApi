# AI Event Planner

AI Event Planner, kullanıcının ilgi alanları, geçmiş katılımları ve takvim uygunluğuna göre etkinlik öneren tam yığın bir web uygulaması iskeletidir.

## Yapı

- `backend/`: FastAPI, SQLAlchemy, öneri servisleri, WebSocket bildirimleri ve testler.
- `frontend/`: Next.js App Router, TypeScript, Tailwind CSS ve AI odaklı etkinlik arayüzü.
- `docs/`: API, mimari ve öneri sistemi notları.

## Hızlı Başlangıç

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Varsayılan frontend adresi `http://localhost:3000`, backend adresi `http://localhost:8000`.
