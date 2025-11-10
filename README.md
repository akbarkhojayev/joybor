# Yotoqxona Boshqaruv Tizimi API

Django REST Framework asosida qurilgan yotoqxona (dormitory) boshqaruv tizimi.

## Xususiyatlar

- **Foydalanuvchi boshqaruvi**: Student, Admin, Ijarachi, Sardor rollari
- **Yotoqxona boshqaruvi**: Yotoqxonalar, qavatlar, xonalar
- **Talabalar boshqaruvi**: Talabalar ro'yxati, joylashish
- **Arizalar tizimi**: Talabalar arizalari va ularni tasdiqlash
- **To'lovlar**: To'lovlarni kuzatish va boshqarish
- **Kvartiralar**: Ijaraga beriladigan kvartiralar
- **Davomat tizimi**: Qavat sardorlari uchun davomat yuritish
- **Yig'imlar**: Qavat bo'yicha yig'imlarni boshqarish
- **Navbatchilik jadvali**: Xonalar bo'yicha navbatchilik
- **Bildirishnomalar**: Foydalanuvchilarga xabarlar yuborish

## O'rnatish

1. Virtual muhitni yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Kerakli paketlarni o'rnating:
```bash
pip install -r requirements.txt
```

3. Ma'lumotlar bazasini yarating:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Superuser yarating:
```bash
python manage.py createsuperuser
```

5. Serverni ishga tushiring:
```bash
python manage.py runserver
```

## API Endpoints

### Autentifikatsiya
- `POST /api/register/` - Ro'yxatdan o'tish
- `POST /api/token/` - Token olish
- `POST /api/token/refresh/` - Tokenni yangilash
- `GET /api/me/` - Joriy foydalanuvchi ma'lumotlari

### Foydalanuvchilar
- `GET /api/users/` - Foydalanuvchilar ro'yxati
- `POST /api/users/create/` - Yangi foydalanuvchi
- `GET /api/users/{id}/` - Foydalanuvchi ma'lumotlari
- `PUT /api/users/{id}/` - Foydalanuvchini yangilash
- `DELETE /api/users/{id}/` - Foydalanuvchini o'chirish

### Yotoqxonalar
- `GET /api/dormitories/` - Yotoqxonalar ro'yxati
- `POST /api/dormitories/create/` - Yangi yotoqxona
- `GET /api/dormitories/{id}/` - Yotoqxona ma'lumotlari
- `PUT /api/dormitories/{id}/` - Yotoqxonani yangilash
- `DELETE /api/dormitories/{id}/` - Yotoqxonani o'chirish

### Talabalar
- `GET /api/students/` - Talabalar ro'yxati
- `POST /api/students/create/` - Yangi talaba
- `GET /api/students/{id}/` - Talaba ma'lumotlari
- `PUT /api/students/{id}/` - Talabani yangilash
- `DELETE /api/students/{id}/` - Talabani o'chirish

### Arizalar
- `GET /api/applications/` - Arizalar ro'yxati
- `POST /api/applications/create/` - Yangi ariza
- `GET /api/applications/{id}/` - Ariza ma'lumotlari
- `POST /api/applications/{id}/approve/` - Arizani tasdiqlash
- `POST /api/applications/{id}/reject/` - Arizani rad etish

### To'lovlar
- `GET /api/payments/` - To'lovlar ro'yxati
- `POST /api/payments/create/` - Yangi to'lov
- `GET /api/payments/{id}/` - To'lov ma'lumotlari

### Davomat
- `GET /api/attendance-sessions/` - Davomat sessiyalari
- `POST /api/attendance-sessions/create/` - Yangi sessiya
- `GET /api/attendance-records/` - Davomat yozuvlari

### Yig'imlar
- `GET /api/collections/` - Yig'imlar ro'yxati
- `POST /api/collections/create/` - Yangi yig'im
- `GET /api/collection-records/` - Yig'im yozuvlari

## Ruxsatlar (Permissions)

- **IsStudnet** - Faqat talabalar
- **IsDormitoryAdmin** - Yotoqxona adminlari
- **IsOwnerOrIsAdmin** - Egasi yoki admin
- **IsAdminOrDormitoryAdmin** - Admin yoki yotoqxona admini
- **IsFloorLeader** - Qavat sardorlari

## API Hujjatlari

Serverni ishga tushirgandan so'ng quyidagi manzillarda API hujjatlarini ko'rishingiz mumkin:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Texnologiyalar

- Django 5.2.8
- Django REST Framework 3.15.2
- Django REST Framework SimpleJWT 5.4.0
- Django Filter 24.3
- Django CORS Headers 4.6.0
- drf-yasg 1.21.8
- Pillow 11.0.0
