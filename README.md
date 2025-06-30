# To-Do List Uygulaması

Bu proje, tam kapsamlı (fullstack) bir To-Do List web uygulamasıdır. Kullanıcılar hesap oluşturup giriş yaparak kendi yapılacaklar listelerini görüntüleyebilir, ekleme, güncelleme, silme ve tamamlama işlemlerini gerçekleştirebilirler.

---

## İçindekiler

1. [Özellikler](#özellikler)
2. [Teknolojiler](#teknolojiler)
3. [Ön Koşullar](#ön-koşullar)
4. [Kurulum](#kurulum)

   * [4.1 Veritabanı](#41-veritabanı)
   * [4.2 Backend](#42-backend)
   * [4.3 Frontend](#43-frontend)
5. [Çalıştırma](#çalıştırma)
6. [API Dokümantasyonu](#api-dokümantasyonu)
7. [Veritabanı Yapısı](#veritabanı-yapısı)

---

## Özellikler

* Kullanıcı kaydı ve girişi (JWT ile yetkilendirme)
* Görev ekleme
* Görev listeleme
* Görev güncelleme (başlık ve tamamlanma durumu)
* Görev silme
* CORS desteği
* Şifrelerin güvenli hash ile saklanması
* Basit React arayüz

---

## Teknolojiler

* **Backend:** Python, Flask, flask-jwt-extended
* **Veritabanı:** PostgreSQL (psycopg2)
* **Frontend:** React, HTML, CSS
* **Diğer:** werkzeug.security

---

## Ön Koşullar

* Python 3.8 veya üzeri
* PostgreSQL 17

---

## Kurulum

### 4.1 Veritabanı

1. PostgreSQL 17 sunucusunu başlatın.

2. Aşağıdaki komut ile `to-do-list` isimli veritabanını oluşturun:

   ```bash
   createdb to-do-list
   ```

3. `db.py` dosyasındaki bağlantı bilgilerini güncelleyin:

   ```python
   conn = psycopg2.connect(
       host="localhost",
       port=5432,
       dbname="to-do-list",
       user="postgres",
       password="admin"
   )
   ```

### 4.2 Backend

1. Proje dizinine gidin:

   ```bash
   cd backend
   ```

2. Sanal ortam oluşturun ve etkinleştirin:

   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/macOS
   venv\\Scripts\\activate   # Windows
   ```

3. Gerekli paketleri yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

4. Ortam değişkenlerini ayarlayın (isteğe bağlı `.env` dosyası):

   ```bash
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export JWT_SECRET_KEY="berfin_29_Haziran"
   ```

### 4.3 Frontend

* Proje, tek bir `index.html` dosyası ile çalışır; ek araç kurulumu gerekmez.
* React bileşenlerini ayrı bir yapı içinde kullanmak isterseniz, Babel veya benzeri araçlarla JSX derlemesi yapabilirsiniz.

---

## Çalıştırma

### Backend

```bash
source venv/bin/activate
flask run
```

Sunucu `http://127.0.0.1:5000` adresinde çalışır.

### Frontend

* `index.html` dosyasını tarayıcıda açarak veya
* Bir HTTP sunucusu (ör. Live Server, http-server) üzerinden çalıştırarak erişin.

---

## API Dokümantasyonu

**Temel URL:** `http://127.0.0.1:5000`

| Yöntem | Yol                                               | Açıklama                          | İstek Gövdesi                            | Header                          |                                 |
| ------ | ------------------------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------- | ------------------------------- |
| POST   | `/register`                                       | Yeni kullanıcı kaydı              | `{ "email", "password" }`                | -                               |                                 |
| POST   | `/login`                                          | Kullanıcı girişi, token döner     | `{ "email", "password" }`                | -                               |                                 |
| GET    | `/tasks/?email=<user_email>`                      | Kullanıcının görevlerini listeler | -                                        | `Authorization: Bearer <token>` |                                 |
| POST   | `/addTask/?email=<user_email>`                    | Yeni görev ekler                  | `{ "title" }`                            | `Authorization: Bearer <token>` |                                 |
| DELETE | `/deleteTask/?id=<task_id>`                       | Belirli görevi siler              | -                                        | `Authorization: Bearer <token>` |                                 |
| PATCH  | \`/updateTask/?id=\<task\_id>\&isCompleted=\<true | false>\&title=<newTitle>\`        | Görev güncelleme (başlık veya tamamlama) | -                               | `Authorization: Bearer <token>` |

---

## Veritabanı Yapısı

**users** tablosu:

```sql
CREATE TABLE users (
  email TEXT PRIMARY KEY,
  password TEXT NOT NULL
);
```

**tasks** tablosu:

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  owner_email TEXT REFERENCES users(email),
  title TEXT NOT NULL,
  is_completed BOOLEAN DEFAULT FALSE
);
```

---
