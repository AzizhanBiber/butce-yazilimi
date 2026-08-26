# Bütçe Yazılımı

TÜMOSAN için geliştirilen sanayi işletmeleri bütçe yönetim sistemi. Django ile Python dilinde yazılmıştır.

## Özellikler
- Departman bazlı bütçe yönetimi (Üretim, Satış, Satın Alma, Muhasebe, Ar-Ge, İnsan Kaynakları, Finans)
- Bütçe vs gerçekleşen karşılaştırma ve sapma analizi
- Onay iş akışı ve versiyon yönetimi
- PDF rapor çıktısı
- E-posta bildirimleri
- SAP/muhasebe veri senkronizasyonu (simülasyon)

## Kurulum

1. Python'ı bilgisayarınıza kurun: https://www.python.org/downloads/
2. Bu projeyi indirin (sağ üstteki "Code" > "Download ZIP" veya git clone ile)
3. Terminal/komut satırını açıp proje klasörüne girin
4. Gerekli kütüphaneleri kurun: pip install -r requirements.txt
5. Veritabanını hazırlayın: python manage.py migrate
6. Sunucuyu başlatın: python manage.py runserver
7. Tarayıcıdan şu adrese girin: http://127.0.0.1:8000

## Kullanılan Teknolojiler
- Python
- Django
- SQLite