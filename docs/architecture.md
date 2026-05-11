# Mimari

Uygulama iki ana parcadan olusur:

- `backend/app/api`: HTTP endpointleri ve dependency katmani.
- `backend/app/services`: Is kurallari, oneriler, takvim ve analitik.
- `backend/app/repositories`: Veritabani erisim soyutlamasi.
- `frontend/src/app`: Next.js App Router sayfalari.
- `frontend/src/components`: Tekrar kullanilabilir UI, layout, event, calendar ve AI bilesenleri.
- `frontend/src/services`: Backend API istemcileri.
- `frontend/src/store`: Zustand tabanli istemci durumu.

Ilk iskelet bellek ici ornek veriyle calisir. PostgreSQL'e geciste repository siniflari SQLAlchemy session kullanacak sekilde genisletilir.
