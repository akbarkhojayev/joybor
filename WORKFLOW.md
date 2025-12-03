# Yotoqxona Tizimi - Ish Jarayoni

## 1. Talaba Ariza Yuboradi

**Endpoint:** `POST /api/applications/create/`

**Request body:**
```json
{
  "dormitory": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "middle_name": "Abdullayevich",
  "province": 1,
  "district": 1,
  "faculty": "Informatika",
  "direction": "Dasturiy injiniring",
  "course": "1-kurs",
  "group": "IT-101",
  "phone": "+998901234567",
  "passport": "AB1234567",
  "user_image": "file",
  "passport_image_first": "file",
  "passport_image_second": "file",
  "document": "file"
}
```

**Response:**
```json
{
  "id": 1,
  "status": "Pending",
  "created_at": "2024-01-01T10:00:00Z",
  ...
}
```

## 2. Admin Arizani Ko'radi

**Endpoint:** `GET /api/applications/`

Admin o'z yotoqxonasiga kelgan barcha arizalarni ko'radi.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Alisher",
    "last_name": "Navoiy",
    "dormitory_name": "Yotoqxona #1",
    "status": "Pending",
    "created_at": "2024-01-01T10:00:00Z"
  }
]
```

## 3. Admin Arizani Tasdiqlaydi

**Endpoint:** `PUT /api/applications/{id}/approve/` yoki `PATCH /api/applications/{id}/approve/`

**Request body:**
```json
{
  "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi."
}
```

Admin arizani tasdiqlaydi. Bu paytda:
1. Ariza statusi "Approved" ga o'zgaradi
2. Admin izohi saqlanadi
3. **Avtomatik ravishda Student yaratiladi** (signal orqali)
4. Talabaga bildirishnoma yuboriladi

**Response:**
```json
{
  "message": "Ariza tasdiqlandi va talaba ro'yxatga olindi",
  "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi.",
  "application": {
    "id": 1,
    "status": "Approved",
    "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi.",
    ...
  }
}
```

### Signal Ishlashi (Avtomatik)

`main/signals.py` faylida `handle_application_approval` signal ishlaydi:
- Application.status == "Approved" bo'lganda
- Yangi Student obyekti yaratiladi
- Barcha ma'lumotlar Application dan Student ga ko'chiriladi
- ApplicationNotification yaratiladi

## 4. Talaba Dashboard ga Kiradi

**Endpoint:** `GET /api/student/dashboard/`

Talaba o'z ma'lumotlarini ko'radi:

**Response:**
```json
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "dormitory_info": {
    "id": 1,
    "name": "Yotoqxona #1",
    "address": "Toshkent, Chilonzor",
    "month_price": 500000,
    "year_price": 5000000
  },
  "floor_info": {
    "id": 1,
    "name": "1-qavat",
    "gender": "male"
  },
  "room_info": {
    "id": 1,
    "name": "101",
    "capacity": 4,
    "current_occupancy": 3,
    "status": "PARTIALLY_OCCUPIED"
  },
  "roommates": [
    {
      "id": 2,
      "name": "Bobur",
      "last_name": "Mirzo",
      "course": "2-kurs",
      "faculty": "Informatika",
      "phone": "+998901234568"
    }
  ],
  "recent_payments": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-01T10:00:00Z",
      "method": "Card",
      "status": "APPROVED"
    }
  ]
}
```

## 5. Talaba Boshqa Ma'lumotlarni Ko'radi

### To'lovlar Tarixi
**Endpoint:** `GET /api/student/payments/`

### Xonadoshlar
**Endpoint:** `GET /api/student/roommates/`

### Davomat
**Endpoint:** `GET /api/student/attendance/`

### Yig'imlar
**Endpoint:** `GET /api/student/collections/`

### Bildirishnomalar
**Endpoint:** `GET /api/student/notifications/`

## 6. Admin Arizani Rad Etishi (Agar kerak bo'lsa)

**Endpoint:** `PUT /api/applications/{id}/reject/` yoki `PATCH /api/applications/{id}/reject/`

**Request body:**
```json
{
  "admin_comment": "Hujjatlar to'liq emas. Passport rasmlari aniq emas."
}
```

Bu paytda:
1. Ariza statusi "Rejected" ga o'zgaradi
2. Admin izohi saqlanadi
3. Talabaga bildirishnoma yuboriladi (rad etilish sababi bilan)
4. Student yaratilmaydi

**Response:**
```json
{
  "message": "Ariza rad etildi",
  "admin_comment": "Hujjatlar to'liq emas. Passport rasmlari aniq emas.",
  "application": {
    "id": 1,
    "status": "Rejected",
    "admin_comment": "Hujjatlar to'liq emas. Passport rasmlari aniq emas.",
    ...
  }
}
```

## Muhim Eslatmalar

1. **Avtomatik Student yaratish** - Signal orqali amalga oshadi, qo'lda yaratish shart emas
2. **Passport unique** - Bir xil passport raqami bilan ikki marta Student yaratilmaydi
3. **Bildirishnomalar** - Har bir ariza tasdiqlanishi yoki rad etilishi haqida talabaga xabar boradi
4. **Role-based access** - Har bir foydalanuvchi faqat o'z ma'lumotlarini ko'radi

## Test Qilish

1. Talaba sifatida ro'yxatdan o'ting
2. Ariza yuboring
3. Admin sifatida arizani tasdiqlang
4. Talaba sifatida dashboard ga kiring
5. Barcha ma'lumotlaringiz ko'rinadi!


## 7. Bildirishnomalar Tizimi

### Barcha Bildirishnomalarni Olish

**Endpoint:** `GET /api/notifications/`

**Query Parameters:**
- `is_read` - true/false (ixtiyoriy)
- `page` - sahifa raqami

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/student/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "type": "application",
      "message": "Tabriklaymiz! Arizangiz tasdiqlandi. Siz Yotoqxona #1 yotoqxonasiga qabul qilindingiz.",
      "is_read": false,
      "created_at": "2024-01-01T10:00:00Z",
      "image": null
    },
    {
      "id": 2,
      "type": "user",
      "message": "Yangi to'lov qo'shildi",
      "is_read": true,
      "created_at": "2024-01-02T10:00:00Z",
      "image": "http://localhost:8000/media/notifications/image.jpg"
    }
  ]
}
```

### O'qilmagan Bildirishnomalar Soni

**Endpoint:** `GET /api/notifications/unread-count/`

**Response:**
```json
{
  "unread_count": 5,
  "user_notifications": 3,
  "application_notifications": 2
}
```

### Bildirishnomani O'qilgan Deb Belgilash

**Endpoint:** `POST /api/notifications/mark-read/`

**Request body:**
```json
{
  "type": "application",
  "id": 1
}
```

**Response:**
```json
{
  "message": "Bildirishnoma o'qilgan deb belgilandi"
}
```

### Barcha Bildirishnomalarni O'qilgan Deb Belgilash

**Endpoint:** `POST /api/notifications/mark-all-read/`

**Response:**
```json
{
  "message": "5 ta bildirishnoma o'qilgan deb belgilandi"
}
```

## Notification Turlari

### 1. ApplicationNotification
- Ariza tasdiqlanganda
- Ariza rad etilganda
- Avtomatik signal orqali yaratiladi

### 2. UserNotification
- Admin tomonidan yuborilgan umumiy xabarlar
- Maxsus bildirishnomalar
- Rasm qo'shish mumkin

## Frontend Uchun Maslahatlar

1. **Real-time yangilanish** - Har 30 sekundda unread_count ni tekshiring
2. **Badge ko'rsatish** - Unread count ni badge sifatida ko'rsating
3. **Filterlash** - is_read parametri bilan o'qilgan/o'qilmaganlarni ajrating
4. **Pagination** - Sahifalash orqali barcha bildirishnomalarni ko'rsating
5. **Type bo'yicha icon** - application va user turlari uchun turli iconlar


## 8. Admin Talabaga Xona Biriktirish

Ariza tasdiqlangandan keyin, talaba yaratiladi lekin hali xonaga joylashtirilmagan (`is_active=False`).

### Xonaga Joylashtirilmagan Talabalar

**Endpoint:** `GET /api/students/unassigned/`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Alisher",
      "last_name": "Navoiy",
      "passport": "AB1234567",
      "course": "1-kurs",
      "gender": "Erkak",
      "is_active": false,
      "placement_status": "Qabul qilindi"
    }
  ]
}
```

### Talabaga Xona Biriktirish

**Endpoint:** `PUT /api/students/{id}/assign-room/` yoki `PATCH /api/students/{id}/assign-room/`

**Request body:**
```json
{
  "floor": 1,
  "room": 101
}
```

Bu paytda:
1. Talabaning jinsi va xona jinsi tekshiriladi
2. Xonada bo'sh joy borligini tekshiriladi
3. Talaba xonaga joylashtiriladi
4. `is_active = True` bo'ladi
5. `placement_status = "Joylashdi"` bo'ladi
6. Xonaning `current_occupancy` oshadi
7. Talabaga bildirishnoma yuboriladi

**Response:**
```json
{
  "message": "Talaba muvaffaqiyatli xonaga joylashtirildi",
  "student": {
    "id": 1,
    "name": "Alisher Navoiy",
    "floor": "1-qavat",
    "room": "101",
    "is_active": true,
    "placement_status": "Joylashdi"
  }
}
```

### Talabani Xonadan Chiqarish

**Endpoint:** `PUT /api/students/{id}/remove-room/` yoki `PATCH /api/students/{id}/remove-room/`

**Request body:** (bo'sh yoki {})

Bu paytda:
1. Talaba xonadan chiqariladi
2. `is_active = False` bo'ladi
3. `placement_status = "Qabul qilindi"` bo'ladi
4. Xonaning `current_occupancy` kamayadi
5. Talabaga bildirishnoma yuboriladi

**Response:**
```json
{
  "message": "Talaba xonadan chiqarildi",
  "student": {
    "id": 1,
    "name": "Alisher Navoiy",
    "is_active": false,
    "placement_status": "Qabul qilindi"
  }
}
```

## Talaba Holatlari

### 1. Ariza Yuborildi
- Status: Application.status = "Pending"
- Student: Mavjud emas

### 2. Ariza Tasdiqlandi
- Status: Application.status = "Approved"
- Student: Yaratildi
- is_active: False
- placement_status: "Qabul qilindi"
- room: null
- floor: null

### 3. Xonaga Joylashtirildi
- is_active: True
- placement_status: "Joylashdi"
- room: Biriktirilgan
- floor: Biriktirilgan

### 4. Xonadan Chiqarildi
- is_active: False
- placement_status: "Qabul qilindi"
- room: null
- floor: null

## Validatsiyalar

1. **Jinsi tekshiruvi** - Talaba jinsi va xona jinsi mos bo'lishi kerak
2. **Bo'sh joy** - Xonada bo'sh joy bo'lishi kerak
3. **Qavat-xona** - Xona tanlangan qavatda bo'lishi kerak
4. **Dublikat** - Talaba allaqachon xonaga joylashtirilgan bo'lsa, xato qaytaradi


## 9. Admin Dashboard Statistikasi

Admin o'z yotoqxonasi bo'yicha to'liq statistikani bitta endpoint orqali oladi.

**Endpoint:** `GET /api/admin/dashboard/`

**Response:**
```json
{
  "students": {
    "total": 150,
    "male": 90,
    "female": 60,
    "active": 140,
    "inactive": 10,
    "by_course": {
      "1-kurs": 40,
      "2-kurs": 35,
      "3-kurs": 30,
      "4-kurs": 25,
      "5-kurs": 20
    }
  },
  "rooms": {
    "total": {
      "rooms": 50,
      "capacity": 200,
      "occupied": 140,
      "free": 60
    },
    "male": {
      "rooms": 30,
      "capacity": 120,
      "occupied": 90,
      "free": 30
    },
    "female": {
      "rooms": 20,
      "capacity": 80,
      "occupied": 50,
      "free": 30
    }
  },
  "payments": {
    "total": 500,
    "approved": 450,
    "cancelled": 50,
    "total_amount": 225000000,
    "paid_students": 130,
    "debtors": 10
  },
  "applications": {
    "total": 200,
    "pending": 15,
    "approved": 150,
    "rejected": 30,
    "cancelled": 5
  }
}
```

### Statistika Ma'lumotlari

**1. Talabalar (students)**
- Jami talabalar
- Yigitlar va qizlar soni
- Faol (xonaga joylashtirilgan) va nofaol talabalar
- Kurs bo'yicha taqsimot

**2. Xonalar (rooms)**
- Jami xonalar va sig'im
- Band va bo'sh joylar
- Yigitlar va qizlar uchun alohida statistika

**3. To'lovlar (payments)**
- Jami to'lovlar soni
- Tasdiqlangan va bekor qilingan to'lovlar
- Jami to'lov summasi
- To'lov qilgan talabalar va qarzdorlar

**4. Arizalar (applications)**
- Barcha arizalar statistikasi
- Status bo'yicha taqsimot

### Frontend uchun Maslahatlar

1. **Dashboard Cards** - Har bir bo'lim uchun alohida card
2. **Charts** - Pie chart (yigitlar/qizlar), Bar chart (kurslar)
3. **Progress Bars** - Bo'sh joylar foizi
4. **Alerts** - Qarzdorlar soni ko'p bo'lsa ogohlantirish
5. **Real-time** - Har 5 daqiqada yangilanish


## 10. Foydalanuvchi Profilini Tahrirlash

Har qanday foydalanuvchi o'z profilini tahrirlashi mumkin.

### Profilni Ko'rish

**Endpoint:** `GET /api/me/`

**Response:**
```json
{
  "id": 1,
  "username": "alisher_student",
  "email": "alisher@example.com",
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "role": "student",
  "image": "http://localhost:8000/media/user_profiles/alisher.jpg",
  "bio": "Informatika fakulteti talabasi",
  "phone": "+998901234567",
  "birth_date": "2000-01-01",
  "address": "Toshkent, Chilonzor",
  "telegram": "@alisher_student"
}
```

### Profilni Tahrirlash

**Endpoint:** `PUT /api/me/` yoki `PATCH /api/me/`

**Request body (to'liq yangilash - PUT):**
```json
{
  "email": "alisher.new@example.com",
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "bio": "Dasturiy injiniring talabasi",
  "phone": "+998901234567",
  "birth_date": "2000-01-01",
  "address": "Toshkent, Yunusobod",
  "telegram": "@alisher_new"
}
```

**Request body (qisman yangilash - PATCH):**
```json
{
  "phone": "+998901234568",
  "telegram": "@alisher_updated"
}
```

### Profil Rasmini Yangilash

**Endpoint:** `PATCH /api/me/`

**Content-Type:** `multipart/form-data`

**Request body:**
```
image: [file]
```

### Tahrirlash Imkoniyatlari

**Tahrirlash mumkin:**
- ✅ email
- ✅ first_name
- ✅ last_name
- ✅ image
- ✅ bio
- ✅ phone
- ✅ birth_date
- ✅ address
- ✅ telegram

**Tahrirlash mumkin emas:**
- ❌ username (o'zgarmas)
- ❌ role (faqat admin o'zgartiradi)
- ❌ id (o'zgarmas)

### Avtomatik Profil Yaratish

Agar foydalanuvchida profil bo'lmasa, birinchi marta `/api/me/` ga so'rov yuborilganda avtomatik yaratiladi.
