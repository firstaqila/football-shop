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

# Tugas 3: Implementasi Form dan Data Delivery pada Django
## Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
1. **Memfasilitasi Proses HTTP Request–Response**: Data delivery memastikan setiap request dari pengguna dapat diteruskan ke server, diproses sesuai kebutuhan, lalu response dari server dikembalikan ke pengguna dengan benar. Tanpa mekanisme ini, request bisa saja tidak sampai ke server atau response gagal kembali ke pengguna, sehingga data tidak dapat ditampilkan dan platform tidak berfungsi sebagaimana mestinya.
2. **Menghubungkan Komponen yang Terdistribusi**: Sebuah platform umumnya dibangun dari berbagai komponen kecil yang saling terhubung. Data delivery berperan sebagai jembatan yang menghubungkan komponen-komponen tersebut. Tanpa data delivery, setiap komponen akan berjalan terisolasi dan tidak mampu membentuk sistem yang utuh.
3. **Menjaga Konsistensi Data**: Data delivery memastikan bahwa setiap perubahan informasi pada satu komponen dapat tersampaikan ke seluruh komponen lain yang membutuhkannya. Dengan demikian, kesalahan informasi dapat dicegah dan semua komponen yang berkaitan dapat bekerja dengan data yang sama secara konsisten.

## Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
Menurut saya, JSON lebih baik. Berikut alasannya, yang sekaligus menjelaskan mengapa JSON lebih populer dibandingkan XML:
1. **Integrasi Bawaan dengan JavaScript**: Cara data diorganisir dalam JSON hampir identik dengan cara objek didefinisikan secara langsung di dalam kode JavaScript. Karena kesamaan ini, JavaScript memiliki mekanisme bawaan untuk mem-prase data JSON menjadi objek JavaScript dan mengubah objek JavaScript menjadi string JSON. Proses ini cepat dan efisien tanpa memerlukan library tambahan. Sebaliknya, untuk memproses data XML di dalam aplikasi JavaScript, developer harus menggunakan parser XML yang lebih kompleks. Proses ini melibatkan penguraian DOM (Document Object Model) XML, yang umumnya lebih lambat dan memerlukan lebih banyak kode untuk mengakses data yang diinginkan.
2. **Kesederhanaan dan Keterbacaan Sintaks**: JSON menggunakan struktur berbasis key-value pair yang intuitif, sederhana, dan mudah dibaca. Struktur ini mirip dengan bagaimana objek didefinisikan dalam banyak bahasa pemrograman. Sebaliknya, XML menggunakan struktur berbasis tag yang memerlukan elemen pembuka dan penutup, sehingga lebih panjang dan kurang efisien untuk dibaca maupun ditulis.
3. **Ukuran File Lebih Kecil**: JSON mampu merepresentasikan data yang sama dengan ukuran file yang lebih kecil dibandingkan XML. Penyebab utamanya adalah sintaks yang lebih efisien dan minim overhead. Dengan ukuran file yang lebih kecil, proses transfer data menjadi lebih cepat dan efisien, terutama pada aplikasi yang membutuhkan pertukaran data secara real-time.

## Jelaskan fungsi dari method `is_valid()` pada form Django dan mengapa kita membutuhkan method tersebut?
Method `is_valid()` digunakan pada instance form (baik itu Form atau ModelForm) untuk memeriksa apakah data yang diinput oleh pengguna pada setiap field pada form sudah sesuai dengan aturan yang didefinisikannya. Contoh pemeriksaan yang dilakukan adalah:
1. Apakah field yang wajib diisi (`required=True`) sudah diisi?
2. Apakah tipe datanya sudah benar? (misalnya, `IntegerField` harus berisi angka).
3. Apakah panjangnya sesuai? (`max_length` dan `min_length`), dsb.
Jika data valid, `is_valid()` akan mengisi atribut `cleaned_data` dengan data yang telah dibersihkan dan dikonversi ke tipe Python yang sesuai. Kemudian return `True`. Namun, jika data tidak valid, kesalahan validasi akan disimpan dalam atribut `errors` yang dapat digunakan untuk menampilkan pesan error kepada pengguna. Kemudian, return False.

Kita membutuhkan method ini untuk:
1. Mencegah invalid data masuk ke sistem atau database.
2. Memberikan feedback kepada pengguna jika terdapat kesalahan input.
3. Agar developer bisa bekerja dengan data yang sudah terjamin valid dan aman, tanpa perlu memvalidasi ulang secara manual.

## Mengapa kita membutuhkan `csrf_token` saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan `csrf_token` pada form Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
`csrf_token` merupakan sebuah token rahasia unik yang dibuat oleh Django setiap kali pengguna membuka halaman dengan form. Token ini disisipkan secara otomatis ke dalam form HTML melalui template tag:
``` py
<form method="post">
    {% csrf_token %}
    ...
</form>
```
Tujuannya adalah untuk memastikan bahwa request POST benar-benar berasal dari form yang sah pada aplikasi pengguna, bukan dari pihak luar. Tanpa `csrf_token`, aplikasi pengguna akan rentan terhadap serangan Cross-Site Request Forgery (CSRF).

Dengan menambahkan `csrf_token`, saat pengguna mengirimkan form, Django akan memeriksa: "Apakah token rahasia dari form ini cocok dengan token rahasia yang diharapkan dari pengguna ini?". Di sisi lain, situs peretas tidak dapat mengetahui token rahasia ini. Maka form palsu yang mereka kirim tidak akan memiliki `csrf_token` yang benar. Akibatnya, server Django akan menolak permintaan tersebut.

Namun, jika pengguna tidak menambahkan `csrf_token`, Django tidak dapat membedakan apakah request berasal dari form yang sah pada aplikasi pengguna atau dari pihak luar. Akibatnya, penyerang dapat memanfaatkan kesempatan ini dengan:
1. **Membuat Halaman HTML Berbahaya**: Penyerang membuat halaman HTML yang berisi form tersembunyi. Form ini dirancang untuk mengirimkan request ke aplikasi target tanpa sepengetahuan pengguna.
2. **Mengirimkan Link Berbahaya**: Penyerang menyebarkan link menuju halaman HTML tersebut kepada pengguna, misalnya melalui email, pesan instan, atau media sosial.
3. **Memanfaatkan Cookie Login**: Jika pengguna mengklik link tersebut saat sedang login ke aplikasi target (yang menggunakan HTTP request), browser pengguna akan secara otomatis melampirkan cookie sesi login yang masih valid ke dalam permintaan yang dibuat oleh form tersembunyi. Karena server tidak memvalidasi permintaan dengan `csrf_token`, server menganggap permintaan tersebut sah. Akibatnya server memproses aksi yang diminta oleh form, seperti mengubah data pengguna, melakukan transaksi, atau aksi berbahaya lainnya, tanpa sepengetahuan pengguna.

## Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
### Tambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.
Pada `views.py` di direktori `main`, tambahkan import `HttpResponse` 
untuk menyusun respon yang ingin dikembalikan oleh server ke user, dan import `Serializer` untuk men-translate objek model menjadi format lain seperti XML dan JSON. Kemudian, tambahkan fungsi-fungsi berikut:
``` py
def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    json_data = serializers.serialize("json", product_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
   try:
       product_item = Product.objects.filter(pk=product_id)
       xml_data = serializers.serialize("xml", product_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json_by_id(request, product_id):
   try:
       product_item = Product.objects.get(pk=product_id)
       json_data = serializers.serialize("json", [product_item])
       return HttpResponse(json_data, content_type="application/json")
   except Product.DoesNotExist:
       return HttpResponse(status=404)
```

### Membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 1.
Pada `urls.py` di direktori `main`, import fungsi-fungsi yang telah dibuat sebelumnya:
``` py
from main.views import show_main, show_xml, show_json, show_xml_by_id, show_json_by_id
```

Kemudian tambahkan path url ke dalam `urlpatterns` untuk mengakses fungsi-fungsi tersebut:
``` py
urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
]
```

### Membuat halaman yang menampilkan data objek model yang memiliki tombol "Add" yang akan redirect ke halaman form, serta tombol "Detail" pada setiap data objek model yang akan menampilkan halaman detail objek; Membuat halaman form untuk menambahkan objek model pada app sebelumnya; Membuat halaman yang menampilkan detail dari setiap data objek model.
1. Buat direktori `templates` di direktori utama dan buat file `base.html` didalamnya. File ini menjadi template dasar (kerangka umum) untuk halaman-halaman pada proyek.

2. Pada `settings.py` di direktori proyek, sesuaikan variabel `TEMPLATES` dengan `'DIRS': [BASE_DIR / 'templates']` agar file `base.html` terdeteksi sebagai sebuah template.

3. Buat file `forms.py` di direktori `main`. File ini berfungsi untuk membuat struktur form yang dapat menerima data Product baru.
``` py
from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "brand", "price", "description", "is_featured", "thumbnail"]
```

- `model = Product` menetapkan bahwa `Product` adalah model yang akan digunakan untuk form. Ketika data dari form disimpan, isi dari form akan disimpan sebagai sebuah objek `Product`.
- `fields` mendaftarkan field apa saja dari `Product` yang akan digunakan untuk form. 

4. Pada `views.py` di direktori `main`, tambahkan dan sesuaikan fungsi-fungsi berikut:
``` py
from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product

def show_main(request):
    product_list = Product.objects.all()

    context = {
        'app_name': 'Slide & Score',
        'name': 'Saffana Firsta Aqila',
        'class': 'PBP B',
        'product_list': product_list # Mengambil seluruh objek Product yang tersimpan pada database.
    }

    return render(request, "main.html", context)

# Menghasilkan form yang dapat menambahkan objek Product baru
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

# Mengambil dan mengembalikan objek Product berdasarkan id
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)
```

5. Pada `urls.py` di direktori `main`, import fungsi yang telah dibuat pada poin 4.
``` py
from django.urls import path
from main.views import show_main, show_xml, show_json, show_xml_by_id, show_json_by_id, create_product, show_product

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('create-product/', create_product, name='create_product'),
    path('product/<str:id>/', show_product, name='show_product'),
]
```

6. Pada `main.html` di direktori `main/templates`, terapkan template `base.html`. Kemudian, di dalam blok `content` tambahkan kode untuk menampilkan data product serta tombol "Add Product" yang akan redirect ke halaman form.

7. Buat dua file baru di direktori `main/templates` dengan nama `create_product.html` sebagai halaman form untuk menambahkan objek model dan `product_detail.html` sebagai halaman yang menampilkan detail dari setiap data objek model.

8. Terakhir, pada `settings.py` di direktori proyek, tambahkan:
``` py
CSRF_TRUSTED_ORIGINS = [
    "https://saffana-firsta-footballshop.pbp.cs.ui.ac.id"
]
```

9. Setelah proses development berhasil, buka Postman dan buat sebuah request baru dengan method `GET` dari url-url yang terdaftar. Salin tiap url dan klik tombol `Send` untuk mengirim request tersebut. Pastikan untuk menjalankan server terlebih dahulu. Berikut hasil akses url pada Postman untuk tugas 3:
- [http://localhost:8000/xml/](https://drive.google.com/file/d/16dCYYyUvDzpv48RNahZe6HVVJhh2nSAg/view?usp=share_link)
- [http://localhost:8000/json/](https://drive.google.com/file/d/1vMUbkJjjLtVP7LxygDGsQEAAhDVzmZqP/view?usp=share_link)
- [http://localhost:8000/xml/[product_id]/](https://drive.google.com/file/d/19cU6jMTH6L7knBVZK4sStCzOjoS7zspu/view?usp=share_link)
- [http://localhost:8000/json/[product_id]/](https://drive.google.com/file/d/1In3YPSC3qNhhwBIfWWuIUdrvI_dmPVMW/view?usp=share_link)

10. Menerapkan perubahan pada GitHub dan PWS.

### Apakah ada feedback untuk asdos di tutorial 2 yang sudah kalian kerjakan?
Tidak ada