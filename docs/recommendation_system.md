# Oneri Sistemi

Ilk prototip su sinyalleri kullanir:

- Kullanici ilgi agirliklari: teknoloji, sanat, girisimcilik gibi alanlar.
- Etkinlik kategorisi ve anahtar kelimeleri.
- Mod secimi: akademik ag kurma, odaklanmis calisma veya sosyal akis.
- Takvim cakismalari ve hatirlatma davranislari.

Uretim surumunde `embedding_service.py` metinleri embedding vektorlerine donusturur, `ranking.py` skorlar, `recommendation_log.py` geri bildirimleri kaydeder. Bu dongu her LCV, begenmeme ve etkinlik sonrasi puanlamayla guncellenir.
