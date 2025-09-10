# Tugas 2: Implementasi Model-View-Template (MVT) pada Django
Link aplikasi PWS: [https://saffana-firsta-footballshop.pbp.cs.ui.ac.id/](https://saffana-firsta-footballshop.pbp.cs.ui.ac.id/)

Note: Proyek ini dibuat dengan sistem operasi macOS

## Jelaskan bagaimana cara kamu mengimplementasikan checklist berikut secara step-by-step
### Membuat sebuah proyek Django baru
1. Membuat direktori baru sebagai direktori utama. Pada tugas ini, direktori tersebut saya beri nama `football-shop`.
2. Di dalam direktori tersebut, saya membuat berkas `requirements.txt` dan menambahkan beberapa dependencies (komponen yang diperlukan suatu perangkat lunak untuk berfungsi) berikut:
    ```
    django
    gunicorn
    whitenoise
    psycopg2-binary
    requests
    urllib3
    python-dotenv
    ```
3. Untuk mengisolasi dependencies antar proyek yang berbeda, saya terlebih dahulu membuat virtual environment dengan menjalankan perintah `python3 -m venv env` dan mengaktifkannya dengan perintah `source env/bin/activate`.
4. Setelah virtual environment aktif, barulah saya menginstal dependencies yang ada menggunakan perintah `pip install -r requirements.txt`.
5. Setelah dependencies terinstal, saya membuat proyek Django bernama `football_shop` menggunakan perintah `django-admin startproject football_shop .`.
6. Kemudian, saya melakukan konfigurasi environment variables untuk menyimpan informasi konfigurasi di luar kode program. Saya membuat dua file pada direktori proyek, yakni:
    - `.env`: Berisi konfigurasi `PRODUCTION=False` untuk local development.
    - `.env.prod`: Berisi konfigurasi `PRODUCTION=True` dan kredensial database (`DB_NAME`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, dan `SCHEMA=tugas_individu`) pribadi dari ITF Fasilkom UI, untuk production deployment.
7. Untuk menggunakan environment variables di atas, saya kemudian memodifikasi `settings.py` dengan menambahkan kode berikut:
    ``` py
    import os
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
    ```
8. Selanjutnya, saya juga mengatur beberapa konfigurasi proyek pada `settings.py`, meliputi:
    - Menambahkan dua string (tertera) pada `ALLOWED_HOSTS = ["localhost", "127.0.0.1"]` untuk mengatur daftar host yang memiliki izin akses terhadap aplikasi web saya.
    - Menambahkan baris `PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'` untuk konfigurasi production.
    - Memodifikasi konfigurasi database dengan kode:
        ``` py
        # Database configuration
        if PRODUCTION:
            # Production: gunakan PostgreSQL dengan kredensial dari environment variables
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': os.getenv('DB_NAME'),
                    'USER': os.getenv('DB_USER'),
                    'PASSWORD': os.getenv('DB_PASSWORD'),
                    'HOST': os.getenv('DB_HOST'),
                    'PORT': os.getenv('DB_PORT'),
                    'OPTIONS': {
                        'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
                    }
                }
            }
        else:
            # Development: gunakan SQLite
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
        ```
9. Setelah konfigurasi berhasil, saya menjalankan migrasi database dengan perintah `python3 manage.py migrate`. Setelah migrasi selesai, saya menjalankan server Django dengan perintah `python3 manage.py runserver`. Terakhir, untuk mengetahui apakah aplikasi Django berhasil dibuat, saya membuka [http://localhost:8000/](http://localhost:8000/) dan memastikan animasi roket muncul.

### Membuat aplikasi dengan nama `main` pada proyek tersebut
1. Menjalankan perintah `python manage.py startapp main`. Setelah perintah tersebut dijalankan, direktori baru dengan nama `main` terbentuk.
2. Menambahkan `main` ke dalam daftar `INSTALLED_APPS` pada `settings.py` di direktori proyek `football_shop`.

### Melakukan routing pada proyek agar dapat menjalankan aplikasi `main`
1. Pada `urls.py` di direktori proyek `football_shop`, saya mengimpor fungsi `include` dan `path` dari `django.urls`. Fungsi `include` memungkinkan saya untuk mengimpor pola URL dari aplikasi lain (dalam hal ini dari aplikasi `main`) ke dalam file `urls.py` level proyek.
2. Selanjutnya, saya menambahkan baris `path('', include('main.urls'))` pada list `urlpatterns`. Path URL '' akan diarahkan ke rute yang didefinisikan pada `urls.py` di direktori aplikasi `main`.

### Membuat model pada aplikasi `main` dengan nama `Product` dan memiliki atribut wajib
1. Pada `models.py` di direktori aplikasi `main`, saya menambahkan kode berikut:
    ``` py
    from django.db import models

    class Product(models.Model):
        CATEGORY_CHOICES = [
            ('jersey', 'Jersey'),
            ('hoodie', 'Hoodie'),
            ('shoes', 'Shoes'),
            ('socks', 'Socks'),
            ('cap', 'Cap'),
            ('ball', 'Ball'),
        ]

        name = models.CharField(max_length=255)
        price = models.IntegerField(default=0)
        description = models.TextField()
        thumbnail = models.URLField(blank=True, null=True)
        category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='jersey')
        is_featured = models.BooleanField(default=False)
    ``` 
2. Kemudian, saya menjalankan migrasi model (cara Django melacak perubahan pada model basis data) dengan perintah `python manage.py makemigrations` dan `python manage.py migrate`.

### Membuat sebuah fungsi pada `views.py` untuk dikembalikan ke dalam sebuah template HTML yang menampilkan nama aplikasi serta nama dan kelas kamu
1. Pertama, saya membuat direktori `templates` di dalam direktori aplikasi `main`.
2. Di dalam direktori `templates`, saya membuat file `main.html` berisi:
    ``` py
    <h1>{{ app_name }}</h1>

    <h5>Name: </h5>
    <p>{{ name }}<p>
    <h5>Class: </h5>
    <p>{{ class }}</p>
    ```
3. Pada `views.py` di direktori aplikasi `main`, saya menambahkan kode:
    ``` py
    from django.shortcuts import render

    def show_main(request):
        context = {
            'app_name': 'Football Shop',
            'name': 'Saffana Firsta Aqila',
            'class': 'PBP B'
        }

        return render(request, "main.html", context)
    ```
    untuk me-render tampilan `main.html`.

### Membuat sebuah routing pada `urls.py` aplikasi `main` untuk memetakan fungsi yang telah dibuat pada `views.py`
Pada `urls.py` di direktori aplikasi `main`, saya menambahkan kode:
``` py
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```

### Melakukan deployment ke PWS terhadap aplikasi yang sudah dibuat
1. Masuk ke halaman [https://pbp.cs.ui.ac.id/](https://pbp.cs.ui.ac.id/).
2. Login dengan akun SSO.
3. Pada home page, klik `Create New Project` kemudian lengkapi seluruh informasi yang diminta.
4. Pada `settings.py` di proyek Django yang sudah dibuat sebelumnya, tambahkan URL deployment PWS pada `ALLOWED_HOSTS`.
4. Jalankan perintah yang terdapat pada informasi Project Command pada halaman PWS.

### Membuat sebuah `README.md` yang berisi tautan menuju aplikasi PWS yang sudah di-deploy, serta jawaban dari beberapa pertanyaan
Setelah selesai menjawab, lakukan `git add`, `commit`, dan `push` untuk menyimpan proyek ke repositori GitHub.

## Buatlah bagan yang berisi request client ke web aplikasi berbasis Django beserta responnya dan jelaskan pada bagan tersebut kaitan antara `urls.py`, `views.py`, `models.py`, dan berkas `html`
![](https://miro.medium.com/1*nn24X8szOc1KvXMZiOxK0Q.png) 
[https://miro.medium.com/1*nn24X8szOc1KvXMZiOxK0Q.png](https://miro.medium.com/1*nn24X8szOc1KvXMZiOxK0Q.png)

Ketika user mengirimkan request (mengakses URL) melalui browser ke server, server menerima request tersebut dan meneruskannya ke Django. Django kemudian menggunakan `urls.py` untuk memetakan URL ke fungsi yang sesuai di `views.py`. Selanjutnya, `views.py` memproses logika dan mengambil data dari `models.py` jika dibutuhkan. Output dari view kemudian dirender ke template `html`, dan server mengirimkan response berupa halaman web kepada user.

## Jelaskan peran `settings.py` dalam proyek Django
`settings.py` merupakan pusat konfigurasi dari sebuah proyek Django. File ini berisi variabel-variabel yang mengatur berbagai aspek dari aplikasi web, antara lain:
1. `BASE_DIR`: variabel yang mengacu pada direktori utama proyek. Semua path yang ditentukan di dalam proyek akan bersifat relatif terhadap `BASE_DIR`.
2. `DEBUG`: variabel yang digunakan untuk mengontrol mode debugging Django.
3. `ALLOWED_HOSTS`: variabel yang menyimpan daftar dari alamat host yang diizinkan untuk menjalankan proyek Django.
4. `INSTALLED_APPS`: variabel yang menyimpan daftar dari semua aplikasi Django yang akan digunakan dalam proyek.
5. `DATABASES`: variabel yang mendefinisikan konfigurasi basis data yang digunakan oleh proyek Django.

## Bagaimana cara kerja migrasi database di Django?
1. **Membuat Perubahan pada Model**: Modifikasi model Django pada `models.py`. Misalnya, menambahkan model baru atau mengubah atribut pada model.
2. **Mendeteksi Perubahan**: Setelah model dimodifikasi, jalankan perintah `python manage.py makemigrations` yang akan menganalisis `models.py` dan membandingkannya dengan kondisi terakhir pada database yang tercatat. Jika terdeteksi perbedaan, file migrasi baru akan dibuat di dalam folder `migrations` aplikasi. File ini berisi kode Python yang menggambarkan perubahan yang perlu diterapkan pada database.
3. **Menerapkan Perubahan**: Setelah file migrasi dibuat, jalankan perintah `python manage.py migrate`. Perintah ini akan:
    - Mencari file migrasi yang belum diterapkan pada database.
    - Menerjemahkan kode Python di dalam file migrasi menjadi perintah SQL sesuai database yang digunakan.
    - Menjalankan perintah SQL tersebut pada database.
    - Mencatat migrasi yang telah diterapkan pada tabel khusus bernama `django_migrations`. Tabel ini berfungsi sebagai riwayat untuk melacak migrasi mana yang sudah dan belum dijalankan.

## Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?
1. **Penggunaan Arsitektur MVT**: MVT memisahkan data (Model), logika (View), dan tampilan (Template). Pemisahan ini memungkinkan pengguna untuk memahami proses pengembangan dengan lebih terstruktur dan terorganisir.
2. **Abstraksi Tinggi**: Django menyembunyikan banyak detail teknis yang rumit dari pengguna. Misalnya, dengan menggunakan Object Relational Mapping (ORM), pengguna tidak perlu menulis kueri SQL secara manual. Pengguna cukup menggunakan Python untuk berinteraksi dengan database, yang jauh lebih mudah dipelajari.
3. **Struktur Proyek Otomatis**: Perintah bawaan Django, seperti `django-admin startproject` dan `python manage.py startapp`, akan secara otomatis membuat struktur direktori proyek yang sudah terorganisir sesuai dengan MVT. Ini memungkinkan pengguna untuk langsung mulai bekerja tanpa harus bingung mengatur folder dan file.
4. **Dokumentasi dan Komunitas**: Django memiliki dokumentasi yang lengkap dan komunitas yang besar. Setiap kali ada kebingungan tentang bagaimana menerapkan MVT, ada banyak sumber yang siap membantu.

## Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Tidak. Saya justru senang karena tutorial yang diberikan sangat terstruktur dan informatif. Sebagai seseorang pemula, tutorial yang diberikan juga mudah dipahami.
