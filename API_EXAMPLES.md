# API Foydalanish Misollari

## 1. Ro'yxatdan O'tish

```bash
POST /api/register/
Content-Type: application/json

{
  "username": "alisher_student",
  "email": "alisher@example.com",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "role": "student",
  "first_name": "Alisher",
  "last_name": "Navoiy"
}
```

## 2. Login (Token Olish)

```bash
POST /api/token/
Content-Type: application/json

{
  "username": "alisher_student",
  "password": "SecurePass123"
}

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 3. Ariza Yuborish

```bash
POST /api/applications/create/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: multipart/form-data

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
  "user_image": [file],
  "passport_image_first": [file],
  "passport_image_second": [file],
  "document": [file]
}
```

## 4. Admin - Arizalarni Ko'rish

```bash
GET /api/applications/?status=Pending
Authorization: Bearer [admin_token]

# Response:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Alisher",
      "last_name": "Navoiy",
      "dormitory_name": "Yotoqxona #1",
      "status": "Pending",
      "created_at": "2024-01-01T10:00:00Z",
      "passport": "AB1234567",
      "phone": "+998901234567"
    }
  ]
}
```

## 5. Admin - Arizani Tasdiqlash

```bash
PUT /api/applications/1/approve/
# yoki
PATCH /api/applications/1/approve/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "admin_comment": "Barcha hujjatlar to'liq va to'g'ri. Tasdiqlandi."
}

# Response:
{
  "message": "Ariza tasdiqlandi va talaba ro'yxatga olindi",
  "admin_comment": "Barcha hujjatlar to'liq va to'g'ri. Tasdiqlandi.",
  "application": {
    "id": 1,
    "status": "Approved",
    "name": "Alisher",
    "last_name": "Navoiy",
    "dormitory_name": "Yotoqxona #1",
    "admin_comment": "Barcha hujjatlar to'liq va to'g'ri. Tasdiqlandi.",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

## 6. Admin - Arizani Rad Etish

```bash
PUT /api/applications/1/reject/
# yoki
PATCH /api/applications/1/reject/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "admin_comment": "Passport rasmlari aniq emas. Iltimos, qayta yuklang."
}

# Response:
{
  "message": "Ariza rad etildi",
  "admin_comment": "Passport rasmlari aniq emas. Iltimos, qayta yuklang.",
  "application": {
    "id": 1,
    "status": "Rejected",
    "name": "Alisher",
    "last_name": "Navoiy",
    "dormitory_name": "Yotoqxona #1",
    "admin_comment": "Passport rasmlari aniq emas. Iltimos, qayta yuklang.",
    "created_at": "2024-01-01T10:00:00Z"
  }
}
```

## 7. Talaba - Dashboard

```bash
GET /api/student/dashboard/
Authorization: Bearer [student_token]

# Response:
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "middle_name": "Abdullayevich",
  "passport": "AB1234567",
  "phone": "+998901234567",
  "course": "1-kurs",
  "faculty": "Informatika",
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
    "id": 101,
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

## 8. Talaba - To'lovlar Tarixi

```bash
GET /api/student/payments/
Authorization: Bearer [student_token]

# Response:
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-01T10:00:00Z",
      "valid_until": "2024-02-01",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi uchun to'lov"
    }
  ]
}
```

## 9. Talaba - Xonadoshlar

```bash
GET /api/student/roommates/
Authorization: Bearer [student_token]

# Response:
[
  {
    "id": 2,
    "name": "Bobur",
    "last_name": "Mirzo",
    "middle_name": "Zahiriddinovich",
    "course": "2-kurs",
    "faculty": "Informatika",
    "phone": "+998901234568",
    "picture": "http://localhost:8000/media/student_pictures/bobur.jpg"
  },
  {
    "id": 3,
    "name": "Ulug'bek",
    "last_name": "Mirzo",
    "course": "1-kurs",
    "faculty": "Matematika",
    "phone": "+998901234569"
  }
]
```

## 10. Talaba - Bildirishnomalar

```bash
GET /api/notifications/?is_read=false
Authorization: Bearer [student_token]

# Response:
{
  "count": 3,
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
      "is_read": false,
      "created_at": "2024-01-02T10:00:00Z",
      "image": "http://localhost:8000/media/notifications/payment.jpg"
    }
  ]
}
```

## 11. Talaba - Bildirishnomani O'qilgan Deb Belgilash

```bash
POST /api/notifications/mark-read/
Authorization: Bearer [student_token]
Content-Type: application/json

{
  "type": "application",
  "id": 1
}

# Response:
{
  "message": "Bildirishnoma o'qilgan deb belgilandi"
}
```

## 12. Talaba - O'qilmagan Bildirishnomalar Soni

```bash
GET /api/notifications/unread-count/
Authorization: Bearer [student_token]

# Response:
{
  "unread_count": 5,
  "user_notifications": 3,
  "application_notifications": 2
}
```

## 13. Admin - To'lov Qo'shish

```bash
POST /api/payments/create/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "student": 1,
  "dormitory": 1,
  "amount": 500000,
  "valid_until": "2024-02-01",
  "method": "Card",
  "status": "APPROVED",
  "comment": "Yanvar oyi uchun to'lov"
}
```

## 14. Qavat Sardori - Davomat Yaratish

```bash
POST /api/attendance-sessions/create/
Authorization: Bearer [floor_leader_token]
Content-Type: application/json

{
  "floor": 1,
  "leader": 1
}

# Response:
{
  "id": 1,
  "date": "2024-01-01",
  "floor": 1,
  "leader": 1,
  "created_at": "2024-01-01T20:00:00Z"
}
```

## 15. Qavat Sardori - Davomat Belgilash

```bash
POST /api/attendance-records/
Authorization: Bearer [floor_leader_token]
Content-Type: application/json

{
  "session": 1,
  "student": 1,
  "status": "in"
}
```

## Muhim Eslatmalar

1. **Authorization Header** - Barcha himoyalangan endpointlar uchun `Bearer token` kerak
2. **Content-Type** - JSON uchun `application/json`, file upload uchun `multipart/form-data`
3. **Pagination** - Ko'pchilik list endpointlar pagination qo'llab-quvvatlaydi (`?page=2`)
4. **Filtering** - Query parametrlar orqali filter qilish mumkin (`?status=Pending`)
5. **Search** - Ba'zi endpointlarda search mavjud (`?search=Alisher`)


## 16. Admin - Xonaga Joylashtirilmagan Talabalar

```bash
GET /api/students/unassigned/?gender=Erkak
Authorization: Bearer [admin_token]

# Response:
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
      "dormitory_name": "Yotoqxona #1",
      "is_active": false,
      "placement_status": "Qabul qilindi",
      "room": null,
      "floor": null
    }
  ]
}
```

## 17. Admin - Talabaga Xona Biriktirish

```bash
PUT /api/students/1/assign-room/
# yoki
PATCH /api/students/1/assign-room/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "floor": 1,
  "room": 101
}

# Response:
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

## 18. Admin - Talabani Xonadan Chiqarish

```bash
PUT /api/students/1/remove-room/
# yoki
PATCH /api/students/1/remove-room/
Authorization: Bearer [admin_token]
Content-Type: application/json

{}
# yoki bo'sh body

# Response:
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

## 19. Talaba - Dashboard (Xonaga Joylashtirilgandan Keyin)

```bash
GET /api/student/dashboard/
Authorization: Bearer [student_token]

# Response:
{
  "id": 1,
  "name": "Alisher",
  "is_active": true,
  "placement_status": "Joylashdi",
  "floor_info": {
    "id": 1,
    "name": "1-qavat",
    "gender": "male"
  },
  "room_info": {
    "id": 101,
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
      "course": "2-kurs"
    }
  ]
}
```

## Xatolar

### Xonada Joy Yo'q

```bash
POST /api/students/1/assign-room/
{
  "floor": 1,
  "room": 101
}

# Response (400):
{
  "room": ["Bu xonada bo'sh joy yo'q"]
}
```

### Jinsi Mos Kelmaydi

```bash
# Response (400):
{
  "error": "Talaba jinsi (Erkak) va xona jinsi (female) mos kelmaydi"
}
```

### Allaqachon Joylashtirilgan

```bash
# Response (400):
{
  "error": "Bu talaba allaqachon xonaga joylashtirilgan",
  "current_room": "101",
  "current_floor": "1-qavat"
}
```


## 20. Admin - Dashboard Statistikasi

```bash
GET /api/admin/dashboard/
Authorization: Bearer [admin_token]

# Response:
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

### Statistika Tushuntirishlari

**Talabalar:**
- `total` - Jami talabalar soni
- `male` - Yigitlar soni
- `female` - Qizlar soni
- `active` - Xonaga joylashtirilgan talabalar
- `inactive` - Xonaga joylashtirilmagan talabalar
- `by_course` - Kurs bo'yicha talabalar

**Xonalar:**
- `total.capacity` - Jami sig'im
- `total.occupied` - Band joylar
- `total.free` - Bo'sh joylar
- `male` - Yigitlar uchun xonalar
- `female` - Qizlar uchun xonalar

**To'lovlar:**
- `total` - Jami to'lovlar soni
- `approved` - Tasdiqlangan to'lovlar
- `total_amount` - Jami to'lov summasi (so'm)
- `paid_students` - Oxirgi 30 kunda to'lov qilgan talabalar
- `debtors` - Qarzdorlar (30 kundan ko'p to'lov qilmagan)

**Arizalar:**
- `pending` - Kutilayotgan arizalar
- `approved` - Tasdiqlangan arizalar
- `rejected` - Rad etilgan arizalar


## 21. Foydalanuvchi - Profilni Ko'rish (To'lovlar Bilan)

```bash
GET /api/me/
Authorization: Bearer [student_token]

# Response (Talaba uchun):
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
  "telegram": "@alisher_student",
  "student_info": {
    "id": 1,
    "name": "Alisher Navoiy",
    "course": "1-kurs",
    "faculty": "Informatika",
    "group": "IT-101",
    "dormitory_name": "Yotoqxona #1",
    "room_name": "101",
    "is_active": true,
    "placement_status": "Joylashdi"
  },
  "recent_payments": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-01T10:00:00Z",
      "valid_until": "2024-02-01",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi uchun to'lov"
    },
    {
      "id": 2,
      "amount": 500000,
      "paid_date": "2023-12-01T10:00:00Z",
      "valid_until": "2024-01-01",
      "method": "Cash",
      "status": "APPROVED",
      "comment": "Dekabr oyi uchun to'lov"
    }
  ],
  "payment_summary": {
    "total_payments": 5,
    "approved_payments": 4,
    "total_amount": 2000000,
    "last_payment_date": "2024-01-01T10:00:00Z",
    "is_debtor": false
  }
}

# Response (Admin uchun):
{
  "id": 2,
  "username": "admin_user",
  "email": "admin@example.com",
  "role": "admin",
  "student_info": null,
  "recent_payments": [],
  "payment_summary": null,
  ...
}
```

## 22. Foydalanuvchi - Profilni Tahrirlash

```bash
PUT /api/me/
# yoki
PATCH /api/me/
Authorization: Bearer [token]
Content-Type: application/json

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

# Response:
{
  "id": 1,
  "username": "alisher_student",
  "email": "alisher.new@example.com",
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "role": "student",
  "image": null,
  "bio": "Dasturiy injiniring talabasi",
  "phone": "+998901234567",
  "birth_date": "2000-01-01",
  "address": "Toshkent, Yunusobod",
  "telegram": "@alisher_new"
}
```

## 23. Foydalanuvchi - Profil Rasmini Yangilash

```bash
PATCH /api/me/
Authorization: Bearer [token]
Content-Type: multipart/form-data

{
  "image": [file]
}

# Response:
{
  "id": 1,
  "username": "alisher_student",
  "email": "alisher@example.com",
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "role": "student",
  "image": "http://localhost:8000/media/user_profiles/alisher_new.jpg",
  ...
}
```

### Tahrirlash Qoidalari

1. **Username** - O'zgartirib bo'lmaydi (read_only)
2. **Role** - O'zgartirib bo'lmaydi (read_only)
3. **Email** - Yangilash mumkin
4. **First_name, Last_name** - Yangilash mumkin
5. **Image** - Multipart/form-data orqali yuklash
6. **Barcha fieldlar** - Ixtiyoriy (PATCH bilan qisman yangilash)


## 24. Admin - O'z Yotoqxonalari Ro'yxati

```bash
GET /api/admin/my-dormitories/
Authorization: Bearer [admin_token]

# Response:
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Yotoqxona #1",
      "address": "Toshkent, Chilonzor tumani",
      "university_name": "TATU",
      "month_price": 500000,
      "year_price": 5000000,
      "is_active": true,
      ...
    }
  ]
}
```

## 25. Admin - O'z Yotoqxonasini Ko'rish

```bash
GET /api/admin/my-dormitory/
Authorization: Bearer [admin_token]

# Response:
{
  "id": 1,
  "name": "Yotoqxona #1",
  "address": "Toshkent, Chilonzor tumani, Bunyodkor ko'chasi 1",
  "university": 1,
  "university_name": "Toshkent Axborot Texnologiyalari Universiteti",
  "description": "Zamonaviy yotoqxona, barcha qulayliklar mavjud",
  "admin": 2,
  "admin_name": "admin_user",
  "month_price": 500000,
  "year_price": 5000000,
  "latitude": 41.311081,
  "longitude": 69.240562,
  "rating": 5,
  "is_active": true,
  "images": [
    {
      "id": 1,
      "image": "http://localhost:8000/media/dormitories/image1.jpg"
    }
  ],
  "amenities_list": [
    {
      "id": 1,
      "name": "Wi-Fi",
      "is_active": true
    },
    {
      "id": 2,
      "name": "Konditsioner",
      "is_active": true
    }
  ]
}
```

## 26. Admin - Yotoqxonani Tahrirlash

```bash
PUT /api/admin/my-dormitory/
# yoki
PATCH /api/admin/my-dormitory/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "name": "Yotoqxona #1 (Yangilangan)",
  "address": "Toshkent, Chilonzor tumani, Bunyodkor ko'chasi 1-uy",
  "description": "Zamonaviy yotoqxona, barcha qulayliklar mavjud. WiFi, konditsioner, issiq suv 24/7",
  "month_price": 550000,
  "year_price": 5500000,
  "latitude": 41.311081,
  "longitude": 69.240562,
  "rating": 5
}

# Response:
{
  "id": 1,
  "name": "Yotoqxona #1 (Yangilangan)",
  "address": "Toshkent, Chilonzor tumani, Bunyodkor ko'chasi 1-uy",
  "university": 1,
  "university_name": "Toshkent Axborot Texnologiyalari Universiteti",
  "description": "Zamonaviy yotoqxona, barcha qulayliklar mavjud. WiFi, konditsioner, issiq suv 24/7",
  "admin": 2,
  "admin_name": "admin_user",
  "month_price": 550000,
  "year_price": 5500000,
  "latitude": 41.311081,
  "longitude": 69.240562,
  "rating": 5,
  "is_active": true,
  ...
}
```

## 27. Admin - Qisman Yangilash (PATCH)

```bash
PATCH /api/admin/my-dormitory/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "month_price": 600000,
  "description": "Yangi tavsif"
}

# Response:
{
  "id": 1,
  "name": "Yotoqxona #1",
  "month_price": 600000,
  "description": "Yangi tavsif",
  ...
}
```

### Tahrirlash Imkoniyatlari

**Tahrirlash mumkin:**
- ✅ name - Yotoqxona nomi
- ✅ address - Manzil
- ✅ description - Tavsif
- ✅ month_price - Oylik narx
- ✅ year_price - Yillik narx
- ✅ latitude, longitude - Koordinatalar
- ✅ rating - Reyting
- ✅ amenities - Qulayliklar (ManyToMany)

**Tahrirlash mumkin emas:**
- ❌ id
- ❌ admin - Faqat superuser o'zgartiradi
- ❌ university - Faqat superuser o'zgartiradi
- ❌ is_active - Faqat superuser o'zgartiradi

## 28. Talaba - O'z Arizasini Ko'rish

```bash
GET /api/student/application/
Authorization: Bearer [student_token]

# Response:
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "middle_name": "Abdullayevich",
  "passport": "AB1234567",
  "phone": "+998901234567",
  "course": "1-kurs",
  "group": "IT-101",
  "faculty": "Informatika",
  "direction": "Dasturiy injiniring",
  "dormitory": 1,
  "dormitory_name": "Yotoqxona #1",
  "province": 1,
  "province_name": "Toshkent",
  "district": 1,
  "district_name": "Chilonzor",
  "status": "Approved",
  "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi.",
  "created_at": "2024-01-01T10:00:00Z",
  "user_image": "http://localhost:8000/media/application_image/alisher.jpg",
  "passport_image_first": "http://localhost:8000/media/passport_image/passport1.jpg",
  "passport_image_second": "http://localhost:8000/media/passport_image/passport2.jpg",
  "document": "http://localhost:8000/media/application_documents/document.pdf"
}
```

## 29. Talaba - Dashboard (Ariza Ma'lumoti Bilan)

```bash
GET /api/student/dashboard/
Authorization: Bearer [student_token]

# Response:
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "is_active": true,
  "placement_status": "Joylashdi",
  "application_info": {
    "id": 1,
    "status": "Approved",
    "created_at": "2024-01-01T10:00:00Z",
    "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi.",
    "dormitory_name": "Yotoqxona #1"
  },
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
    "id": 101,
    "name": "101",
    "capacity": 4,
    "current_occupancy": 3,
    "status": "PARTIALLY_OCCUPIED"
  },
  "roommates": [...],
  "recent_payments": [...]
}
```

### Ariza Statuslari

- **Pending** - Kutilmoqda (admin hali ko'rmagan)
- **Approved** - Tasdiqlangan (Student yaratilgan)
- **Rejected** - Rad etilgan (admin_comment da sabab)
- **Cancelled** - Bekor qilingan

### 404 Xatolari

**Ariza topilmasa:**
```json
{
  "detail": "Sizning arizangiz topilmadi"
}
```

**Student bo'lmasa:**
```json
{
  "error": "Siz hali talaba sifatida ro'yxatdan o'tmagansiz"
}
```