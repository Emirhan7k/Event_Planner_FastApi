# Backend

FastAPI tabanlı API katmanı. İlk sürüm bellek içi örnek veriyle çalışır; `DATABASE_URL` verilirse SQLAlchemy bağlantısı hazırdır.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
