TO-DO LİST UYGULAMASI

Bu proje, tam kapsamlı (fullstack) bir To-Do List web uygulamasıdır. Kullanıcılar hesap oluşturup giriş yaparak kendi yapılacaklar listelerini görüntüleyebilir, ekleme, güncelleme, silme ve tamamlama işlemlerini gerçekleştirebilirler.

İÇİNDEKİLER

ÖZELLİKLER

TEKNOLOJİLER

ÖN KOŞULLAR

KURULUM
4.1 Veritabanı
4.2 Backend
4.3 Frontend

ÇALIŞTIRMA

API DOKÜMANTASYONU

VERİTABANI YAPISI

ÖZELLİKLER

Kullanıcı kaydı ve girişi (JWT ile yetkilendirme)

Görev ekleme

Görev listeleme

Görev güncelleme (başlık ve tamamlama durumu)

Görev silme

CORS desteği

Şifrelerin güvenli hash ile saklanması

Basit React arayüz

TEKNOLOJİLER

Backend: Python, Flask, flask-jwt-extended

Veritabanı: PostgreSQL (psycopg2)

Frontend: React (JSX via Babel), HTML, CSS

Diğer: werkzeug.security, flask-cors

ÖN KOŞULLAR

Python 3.8 veya üzeri

PostgreSQL

KURULUM

4.1 Veritabanı

PostgreSQL sunucusunu başlatın.

Terminalde aşağıdaki komutu çalıştırarak veritabanını oluşturun:
createdb to-do-list

db.py dosyasındaki bağlantı bilgilerini gerektiği gibi güncelleyin:
conn = psycopg2.connect(host="localhost", port=5432, dbname="to-do-list", user="postgres", password="admin")

4.2 Backend

Proje dizinine gidin: cd backend

Sanal ortam oluşturun: python -m venv venv

Sanal ortamı etkinleştirin:

Linux/macOS: source venv/bin/activate

Windows: venv\Scripts\activate

Gerekli Python paketlerini yükleyin: pip install -r requirements.txt

Ortam değişkenlerini ayarlayın:
FLASK_APP=app.py
FLASK_ENV=development
JWT_SECRET_KEY="berfin_29_Haziran"

4.3 Frontend

Proje, tek bir index.html dosyası ile çalışır. Frontend için ek araç kurulumu gerekmemektedir.

Eğer React bileşenlerini ayrı bir yapıda kullanmak isterseniz, Babel veya benzeri araçlarla JSX derlemesi yapabilirsiniz.

ÇALIŞTIRMA

Backend:

Sanal ortamı etkinleştirin.

flask run
Sunucu http://127.0.0.1:5000 adresinde çalışır.

Frontend:

Tarayıcıda index.html dosyasını açarak veya HTTP sunucusu (Live Server, http-server vb.) üzerinden çalıştırarak erişin.

API DOKÜMANTASYONU

Temel URL: http://127.0.0.1:5000

Endpoints:

POST /register

Açıklama: Yeni kullanıcı kaydı

İstek gövdesi: { "email", "password" }

Header: none

POST /login

Açıklama: Kullanıcı girişi, token döner

İstek gövdesi: { "email", "password" }

Header: none

GET /tasks/?email=<user_email>

Açıklama: Kullanıcının tüm görevlerini getirir

Header: Authorization: Bearer 

POST /addTask/?email=<user_email>

Açıklama: Yeni görev ekler

İstek gövdesi: { "title" }

Header: Authorization: Bearer 

DELETE /deleteTask/?id=<task_id>

Açıklama: Belirli görevi siler

Header: Authorization: Bearer 

PATCH /updateTask/?id=<task_id>&isCompleted=<true|false>&title=

Açıklama: Görev güncelleme (başlık veya tamamlama durumu)

Header: Authorization: Bearer 

VERİTABANI YAPISI

Users tablosu:

email: TEXT, birincil anahtar

password: TEXT, hash’lenmiş şifre

Tasks tablosu:

id: SERIAL, birincil anahtar

owner_email: TEXT, users.email referansı

title: TEXT, görev başlığı

is_completed: BOOLEAN, varsayılan false



