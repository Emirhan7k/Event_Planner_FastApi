# API

Base URL: `http://localhost:8000`

| Method | Path | Aciklama |
| --- | --- | --- |
| `GET` | `/health` | Servis durumu |
| `POST` | `/api/auth/login` | Token uretir |
| `POST` | `/api/auth/register` | Kullanici kaydi |
| `GET` | `/api/users/me` | Aktif kullanici profili |
| `GET` | `/api/events` | Etkinlik listesi |
| `GET` | `/api/events/{event_id}` | Etkinlik detayi |
| `POST` | `/api/events` | Yeni etkinlik |
| `GET` | `/api/recommendations` | AI onerileri |
| `GET` | `/api/calendar` | Haftalik takvim |
| `GET` | `/api/preferences` | Kullanici tercihleri |
| `PUT` | `/api/preferences` | Tercih guncelleme |
| `GET` | `/api/admin/metrics` | Admin metrikleri |
