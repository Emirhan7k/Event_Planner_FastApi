import os

folders = [
    "backend/app/api/v1", "backend/app/core",
    "backend/app/db", "backend/app/models",
    "backend/app/schemas", "backend/app/services",
    "backend/app/ml", "backend/tests",
    "frontend/public", "frontend/src/assets",
    "frontend/src/components", "frontend/src/pages",
    "frontend/src/hooks", "frontend/src/services",
    "frontend/src/context", "infrastructure"
]

files = [
    ".gitignore", ".env.example", "README.md",
    "infrastructure/docker-compose.yml", "infrastructure/Dockerfile.backend", "infrastructure/Dockerfile.frontend",
    "backend/alembic.ini", "backend/app/__init__.py", "backend/app/main.py",
    "backend/app/api/dependencies.py", "backend/app/api/v1/events.py", "backend/app/api/v1/users.py", "backend/app/api/v1/recommendations.py",
    "backend/app/core/config.py", "backend/app/core/security.py",
    "backend/app/db/base.py", "backend/app/db/session.py",
    "backend/app/models/event.py", "backend/app/models/user.py",
    "backend/app/schemas/event_schema.py", "backend/app/schemas/user_schema.py",
    "backend/app/services/event_service.py", "backend/app/services/user_service.py",
    "backend/app/ml/embeddings.py", "backend/app/ml/vector_db.py", "backend/app/ml/recommender.py",
    "backend/tests/conftest.py", "backend/tests/test_api_events.py", "backend/tests/test_ml_recommender.py",
    "frontend/package.json", "frontend/vite.config.js", "frontend/index.html",
    "frontend/src/main.jsx", "frontend/src/App.jsx", "frontend/src/index.css",
    "frontend/src/components/EventCard.jsx", "frontend/src/components/Sidebar.jsx", "frontend/src/components/Navbar.jsx",
    "frontend/src/pages/Dashboard.jsx", "frontend/src/pages/Calendar.jsx", "frontend/src/pages/Profile.jsx",
    "frontend/src/hooks/useRecommendations.js", "frontend/src/services/apiClient.js", "frontend/src/context/AuthContext.jsx", "frontend/src/context/ThemeContext.jsx"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        pass

print("✅ Tüm klasör ve dosyalar başarıyla oluşturuldu!")


"""
intelligent_event_planner/
├── backend/                        # ⚙️ FastAPI & Makine Öğrenmesi Servisleri
│   ├── pyproject.toml              # uv bağımlılık yöneticisi yapılandırması
│   ├── uv.lock                     # Kilitlenmiş kesin bağımlılık sürümleri
│   ├── alembic.ini (ÖMER)                # Veritabanı migrasyon aracı ayarları
│   ├── alembic/(ÖMER)                    # PostgreSQL tablo değişiklik kayıtları (Migrations)
│   ├── app/(EMİRHAN)
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI uygulamasının ana giriş noktası
│   │   ├── api/
│   │   │   ├── dependencies.py     # Ortak işlevler (örn: db_session, token doğrulama)
│   │   │   └── v1/                 # API versiyonlama
│   │   │       ├── events.py       # Etkinlik CRUD işlemleri
│   │   │       ├── users.py        # Kullanıcı işlemleri
│   │   │       └── recommendations.py # Öneri sistemi end-pointleri
│   │   ├── core/(EMİRHAN)
│   │   │   ├── config.py           # .env okuma ve temel yapılandırmalar
│   │   │   └── security.py         # JWT oluşturma, şifre hashleme (bcrypt)
│   │   ├── db/(ÖMER)
│   │   │   ├── base.py             # SQLAlchemy Base sınıfı
│   │   │   └── session.py          # Asenkron PostgreSQL bağlantı motoru
│   │   ├── models/(ÖMER)                 # Veritabanı Tablo Modelleri (SQLAlchemy)
│   │   │   ├── event.py
│   │   │   └── user.py
│   │   ├── schemas/(EMİRHAN)                # Veri Doğrulama Modelleri (Pydantic)
│   │   │   ├── event_schema.py
│   │   │   └── user_schema.py
│   │   ├── services/(EMİRHAN)              # Temel İş Mantığı Sınıfları
│   │   │   ├── event_service.py
│   │   │   └── user_service.py
│   │   └── ml/ (EMİRHAN)                    # 🧠 Yapay Zeka ve Öneri Motoru
│   │       ├── embeddings.py       # Metin/kategori vektörleştirme işlemleri
│   │       ├── vector_db.py        # pgvector veya FAISS ile vektör arama işlemleri
│   │       ├── recommender.py      # Temel RAG ve kosinüs benzerliği algoritmaları
│   │       └── model_weights.pt    # Eğitilmiş model ağırlıkları (PyTorch formatında)
│   └── tests/  (ÖMER EMİRHAN )                    # Birim ve Entegrasyon Testleri
│       ├── conftest.py
│       ├── test_api_events.py
│       └── test_ml_recommender.py
│
├── frontend/ (YASİN)                      # 🎨 React Kullanıcı Arayüzü (Vite tabanlı)
│   ├── package.json                # NPM/Yarn bağımlılıkları
│   ├── vite.config.js              # Hızlı derleme aracı ayarları
│   ├── index.html                  # Ana HTML şablonu
│   ├── public/                     # Statik dosyalar (favicon vb.)
│   └── src/
│       ├── main.jsx                # React ana bağlama noktası
│       ├── App.jsx                 # Ana routing (sayfa yönlendirme) bileşeni
│       ├── index.css               # Global stiller (Tailwind CSS entegrasyonu)
│       ├── assets/                 # Görseller ve özel ikonlar
│       ├── components/             # Yeniden Kullanılabilir Arayüz Parçaları
│       │   ├── EventCard.jsx       # Etkinlik kartı ve eşleşme skoru tasarımı
│       │   ├── Sidebar.jsx         # Sol gezinme menüsü
│       │   └── Navbar.jsx          # Üst arama ve profil çubuğu
│       ├── pages/                  # Tam Sayfa Görünümleri
│       │   ├── Dashboard.jsx       # Önerilerin aktığı ana pano
│       │   ├── Calendar.jsx        # Akıllı takvim görünümü
│       │   └── Profile.jsx         # İlgi alanı ağırlıklarını ayarlama sayfası
│       ├── hooks/                  # Özel React Hook'ları
│       │   └── useRecommendations.js # Backend'den anlık öneri çeken asenkron hook
│       ├── services/               # API İstek Yönetimi (Axios)
│       │   └── apiClient.js        # İstek başlıkları ve token ekleme işlemleri
│       └── context/                # Global State (Durum) Yönetimi
│           ├── AuthContext.jsx     # Kullanıcı oturum durumu
│           └── ThemeContext.jsx
│
├── .gitignore                      # Git'e dahil edilmeyecek dosyalar listesi
├── .env.example                    # Gerekli çevresel değişkenlerin şablonu
└── README.md                       # Proje kurulum ve çalıştırma talimatları
"""