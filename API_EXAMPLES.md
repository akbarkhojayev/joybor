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
```

## 6. Talaba Ma'lumotlarini Ko'rish (To'lovlar bilan)

```bash
GET /api/students/1/
Authorization: Bearer [token]

# Response:
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "middle_name": "Abdullayevich",
  "course": "1-kurs",
  "faculty": "Informatika",
  "group": "IT-101",
  "dormitory_name": "Yotoqxona #1",
  "room_name": "101",
  "floor_name": "1-qavat",
  "province_name": "Toshkent",
  "district_name": "Yunusobod",
  "is_active": true,
  "placement_status": "Joylashdi",
  "payments": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-15T10:00:00Z",
      "valid_until": "2024-02-15",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi to'lovi"
    },
    {
      "id": 2,
      "amount": 500000,
      "paid_date": "2023-12-15T10:00:00Z",
      "valid_until": "2024-01-15",
      "method": "Cash",
      "status": "APPROVED",
      "comment": "Dekabr oyi to'lovi"
    }
  ],
  "payment_summary": {
    "total_payments": 5,
    "approved_payments": 5,
    "total_amount": 2500000,
    "last_payment_date": "2024-01-15T10:00:00Z",
    "last_payment_amount": 500000,
    "is_debtor": false
  }
}
```

## 7. Profil Ma'lumotlarini Ko'rish (To'lovlar bilan)

```bash
GET /api/profiles/1/
Authorization: Bearer [token]

# Response:
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "alisher_student",
    "email": "alisher@example.com",
    "role": "student"
  },
  "image": "http://example.com/media/user_profiles/photo.jpg",
  "bio": "Informatika fakulteti talabasi",
  "phone": "+998901234567",
  "birth_date": "2005-05-15",
  "address": "Toshkent, Yunusobod",
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
  "payments": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-15T10:00:00Z",
      "valid_until": "2024-02-15",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi to'lovi"
    }
  ],
  "payment_summary": {
    "total_payments": 5,
    "approved_payments": 5,
    "total_amount": 2500000,
    "last_payment_date": "2024-01-15T10:00:00Z",
    "last_payment_amount": 500000,
    "is_debtor": false
  }
}
```

## 8. Joriy Foydalanuvchi Ma'lumotlari (To'lovlar bilan)

```bash
GET /api/me/
Authorization: Bearer [token]

# Response (agar student bo'lsa):
{
  "id": 1,
  "username": "alisher_student",
  "email": "alisher@example.com",
  "first_name": "Alisher",
  "last_name": "Navoiy",
  "role": "student",
  "image": "http://example.com/media/user_profiles/photo.jpg",
  "bio": "Informatika fakulteti talabasi",
  "phone": "+998901234567",
  "birth_date": "2005-05-15",
  "address": "Toshkent, Yunusobod",
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
      "paid_date": "2024-01-15T10:00:00Z",
      "valid_until": "2024-02-15",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi to'lovi"
    }
  ],
  "payment_summary": {
    "total_payments": 5,
    "approved_payments": 5,
    "total_amount": 2500000,
    "last_payment_date": "2024-01-15T10:00:00Z",
    "is_debtor": false
  }
}
```

## 9. To'lovlar Xulosasi Tushuntirish

```json
"payment_summary": {
  "total_payments": 5,           // Jami to'lovlar soni
  "approved_payments": 5,         // Tasdiqlangan to'lovlar soni
  "total_amount": 2500000,        // Jami to'langan summa (faqat APPROVED)
  "last_payment_date": "2024-01-15T10:00:00Z",  // Oxirgi to'lov sanasi
  "last_payment_amount": 500000,  // Oxirgi to'lov summasi
  "is_debtor": false              // Qarzdormi? (30 kundan ko'p to'lov qilmagan)
}
```

### is_debtor Qanday Hisoblanadi?

- Agar oxirgi 30 kun ichida hech qanday APPROVED to'lov bo'lmasa → `is_debtor: true`
- Agar oxirgi 30 kun ichida kamida bitta APPROVED to'lov bo'lsa → `is_debtor: false`

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
      "free": 60,
      "occupancy_rate": 70.0
    },
    "male": {
      "rooms": 30,
      "capacity": 120,
      "occupied": 90,
      "free": 30,
      "occupancy_rate": 75.0
    },
    "female": {
      "rooms": 20,
      "capacity": 80,
      "occupied": 50,
      "free": 30,
      "occupancy_rate": 62.5
    },
    "by_status": {
      "available": 10,
      "partially_occupied": 25,
      "fully_occupied": 15
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

**Talabalar (students):**
- `total` - Jami talabalar soni
- `male` - Yigitlar soni
- `female` - Qizlar soni
- `active` - Xonaga joylashtirilgan talabalar
- `inactive` - Xonaga joylashtirilmagan talabalar
- `by_course` - Kurs bo'yicha talabalar

**Xonalar (rooms):**
- `total.rooms` - Jami xonalar soni
- `total.capacity` - Jami sig'im (barcha o'rinlar)
- `total.occupied` - Band o'rinlar soni
- `total.free` - Bo'sh o'rinlar soni
- `total.occupancy_rate` - Band bo'lish foizi (%)
- `male` - Erkaklar uchun xonalar statistikasi
- `female` - Ayollar uchun xonalar statistikasi
- `by_status.available` - To'liq bo'sh xonalar (hech kim yo'q)
- `by_status.partially_occupied` - Qisman band xonalar (joy bor)
- `by_status.fully_occupied` - To'liq band xonalar (joy yo'q)

**To'lovlar (payments):**
- `total` - Jami to'lovlar soni
- `approved` - Tasdiqlangan to'lovlar
- `cancelled` - Bekor qilingan to'lovlar
- `total_amount` - Jami to'lov summasi (so'm)
- `paid_students` - Oxirgi 30 kunda to'lov qilgan talabalar
- `debtors` - Qarzdorlar (30 kundan ko'p to'lov qilmagan)

**Arizalar (applications):**
- `total` - Jami arizalar soni
- `pending` - Kutilayotgan arizalar
- `approved` - Tasdiqlangan arizalar
- `rejected` - Rad etilgan arizalar
- `cancelled` - Bekor qilingan arizalar

### Xonalar Statistikasi Qo'shimcha Tushuntirish

**occupancy_rate (Band bo'lish foizi):**
- 0% = Hamma xonalar bo'sh
- 50% = Xonalarning yarmi band
- 75% = Xonalarning 3/4 qismi band
- 100% = Hamma xonalar to'liq band

**by_status (Xonalar holati):**
- `available` = To'liq bo'sh xonalar - yangi talabalar uchun
- `partially_occupied` = Qisman band - xonadosh bilan
- `fully_occupied` = To'liq band - joy yo'q

**Misol:**
Agar `male.free = 30` bo'lsa, bu 30 ta erkak talaba uchun bo'sh o'rin mavjud degani.
Agar `female.occupancy_rate = 62.5` bo'lsa, bu ayollar xonalarining 62.5% band degani.


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
## 30
. Umumiy Statistika

```bash
GET /api/stats/
# Token kerak emas - hamma ko'ra oladi

# Response:
{
  "dormitories": {
    "total": 25,
    "active": 23
  },
  "students": {
    "total": 1500,
    "active": 1350,
    "male": 900,
    "female": 600
  },
  "universities": {
    "total": 15
  },
  "applications": {
    "total": 2000,
    "pending": 50,
    "approved": 1500
  },
  "rooms": {
    "total": 500,
    "capacity": 2000,
    "occupied": 1350,
    "free": 650,
    "occupancy_rate": 67.5
  },
  "provinces": {
    "total": 14
  }
}
```

### Statistika Tushuntirishlari

**Yotoqxonalar (dormitories):**
- `total` - Jami yotoqxonalar soni
- `active` - Faol yotoqxonalar soni

**Talabalar (students):**
- `total` - Jami talabalar soni
- `active` - Xonaga joylashtirilgan talabalar
- `male` - Yigitlar soni
- `female` - Qizlar soni

**Universitetlar (universities):**
- `total` - Jami universitetlar soni

**Arizalar (applications):**
- `total` - Jami arizalar soni
- `pending` - Kutilayotgan arizalar
- `approved` - Tasdiqlangan arizalar

**Xonalar (rooms):**
- `total` - Jami xonalar soni
- `capacity` - Jami sig'im
- `occupied` - Band joylar
- `free` - Bo'sh joylar
- `occupancy_rate` - Band joylar foizi

**Viloyatlar (provinces):**
- `total` - Jami viloyatlar soni

### Foydalanish

Bu endpoint:
- ✅ Token talab qilmaydi (AllowAny)
- ✅ Tez ishlaydi
- ✅ Landing page uchun mos
- ✅ Dashboard kartlari uchun ideal
- ✅ Real-time ma'lumotlar


## Bildirishnomalar (Notifications)

### 1. Barcha Bildirishnomalarni Ko'rish

```bash
GET /api/notifications/
Authorization: Bearer [token]

# Response:
{
  "count": 10,
  "next": null,
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
      "message": "Yangi e'lon: Ertaga yig'ilish bo'ladi",
      "is_read": true,
      "created_at": "2024-01-01T09:00:00Z",
      "image": "http://example.com/media/notifications/image.jpg"
    }
  ]
}
```

### 2. O'qilmagan Bildirishnomalarni Ko'rish

```bash
GET /api/notifications/?is_read=false
Authorization: Bearer [token]
```

### 3. O'qilmagan Bildirishnomalar Sonini Ko'rish

```bash
GET /api/notifications/unread-count/
Authorization: Bearer [token]

# Response:
{
  "unread_count": 5,
  "user_notifications": 3,
  "application_notifications": 2
}
```

### 4. Bildirishnomani O'qilgan Deb Belgilash

```bash
POST /api/notifications/mark-read/
Authorization: Bearer [token]
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

### 5. Barcha Bildirishnomalarni O'qilgan Deb Belgilash

```bash
POST /api/notifications/mark-all-read/
Authorization: Bearer [token]

# Response:
{
  "message": "5 ta bildirishnoma o'qilgan deb belgilandi"
}
```

### 6. Admin - Bildirishnoma Yaratish (Barcha Studentlarga)

```bash
POST /api/admin/notifications/create/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "message": "Ertaga soat 10:00 da umumiy yig'ilish bo'ladi. Barcha talabalar ishtirok etishi shart!",
  "target_type": "all_students",
  "is_active": true
}

# Rasm bilan:
POST /api/admin/notifications/create/
Authorization: Bearer [admin_token]
Content-Type: multipart/form-data

{
  "message": "Yangi qoidalar e'lon qilindi",
  "target_type": "all_students",
  "image": [file],
  "is_active": true
}
```

### 7. Admin - Bildirishnoma Yaratish (Ma'lum Foydalanuvchiga)

```bash
POST /api/admin/notifications/create/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "message": "Sizning to'lovingiz qabul qilindi",
  "target_type": "specific_user",
  "target_user": 5,
  "is_active": true
}
```

### 8. Admin - Bildirishnoma Yaratish (Barcha Adminlarga)

```bash
POST /api/admin/notifications/create/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "message": "Yangi admin paneli funksiyalari qo'shildi",
  "target_type": "all_admins",
  "is_active": true
}
```

### 9. Admin - Bildirishnomalar Ro'yxati

```bash
GET /api/admin/notifications/
Authorization: Bearer [admin_token]

# Filter by target_type:
GET /api/admin/notifications/?target_type=all_students
GET /api/admin/notifications/?is_active=true

# Response:
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "message": "Ertaga soat 10:00 da umumiy yig'ilish bo'ladi",
      "image": null,
      "target_type": "all_students",
      "target_user": null,
      "target_user_name": null,
      "created_at": "2024-01-01T10:00:00Z",
      "is_active": true
    }
  ]
}
```

### 10. Admin - Bildirishnomani Tahrirlash

```bash
PUT /api/admin/notifications/1/
# yoki
PATCH /api/admin/notifications/1/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "message": "Yig'ilish vaqti o'zgartirildi - soat 11:00 ga",
  "is_active": true
}
```

### 11. Admin - Bildirishnomani O'chirish

```bash
DELETE /api/admin/notifications/1/
Authorization: Bearer [admin_token]
```

## Bildirishnoma Turlari (target_type)

- `all_students` - Barcha studentlarga yuborish
- `all_admins` - Barcha adminlarga yuborish
- `specific_user` - Ma'lum bir foydalanuvchiga yuborish (target_user field ni to'ldirish kerak)

## Bildirishnoma Tiplari (type)

- `user` - Admin tomonidan yaratilgan bildirishnoma (UserNotification)
- `application` - Tizim tomonidan avtomatik yaratilgan bildirishnoma (ApplicationNotification)
  - Ariza tasdiqlanganda
  - Ariza rad etilganda
  - Xonaga joylashtirilganda
  - Xonadan chiqarilganda


## Yotoqxona Bo'sh Joylar Statistikasi

### Yotoqxona Ma'lumotlarini Ko'rish (Bo'sh Joylar bilan)

```bash
GET /api/dormitories/1/
Authorization: Bearer [token]

# Response:
{
  "id": 1,
  "name": "Yotoqxona #1",
  "address": "Toshkent, Chilonzor tumani",
  "university": 1,
  "university_name": "TATU",
  "admin": 2,
  "admin_name": "admin_user",
  "description": "Zamonaviy yotoqxona",
  "month_price": 500000,
  "year_price": 5000000,
  "latitude": 41.311151,
  "longitude": 69.279737,
  "rating": 5,
  "is_active": true,
  "distance": 2.5,
  "images": [
    {
      "id": 1,
      "image": "http://example.com/media/dormitories/image1.jpg",
      "dormitory": 1
    }
  ],
  "amenities_list": [
    {
      "id": 1,
      "name": "WiFi",
      "is_active": true
    },
    {
      "id": 2,
      "name": "Konditsioner",
      "is_active": true
    }
  ],
  "rules": [
    {
      "id": 1,
      "dormitory": 1,
      "rule": "Soat 23:00 dan keyin shovqin qilish taqiqlanadi"
    },
    {
      "id": 2,
      "dormitory": 1,
      "rule": "Mehmonlar faqat soat 20:00 gacha"
    }
  ],
  "room_statistics": {
    "total": {
      "rooms": 50,
      "capacity": 200,
      "occupied": 150,
      "free": 50,
      "occupancy_rate": 75.0
    },
    "male": {
      "rooms": 30,
      "capacity": 120,
      "occupied": 90,
      "free": 30,
      "occupancy_rate": 75.0
    },
    "female": {
      "rooms": 20,
      "capacity": 80,
      "occupied": 60,
      "free": 20,
      "occupancy_rate": 75.0
    },
    "by_status": {
      "available": 10,
      "partially_occupied": 25,
      "fully_occupied": 15
    }
  }
}
```

### Room Statistics Tushuntirish

```json
"room_statistics": {
  "total": {
    "rooms": 50,              // Jami xonalar soni
    "capacity": 200,          // Jami sig'im (barcha o'rinlar)
    "occupied": 150,          // Band o'rinlar soni
    "free": 50,               // Bo'sh o'rinlar soni
    "occupancy_rate": 75.0    // Band bo'lish foizi (%)
  },
  "male": {
    "rooms": 30,              // Erkaklar xonalari soni
    "capacity": 120,          // Erkaklar uchun jami o'rinlar
    "occupied": 90,           // Band erkaklar o'rinlari
    "free": 30,               // Bo'sh erkaklar o'rinlari
    "occupancy_rate": 75.0    // Erkaklar xonalari band bo'lish foizi
  },
  "female": {
    "rooms": 20,              // Ayollar xonalari soni
    "capacity": 80,           // Ayollar uchun jami o'rinlar
    "occupied": 60,           // Band ayollar o'rinlari
    "free": 20,               // Bo'sh ayollar o'rinlari
    "occupancy_rate": 75.0    // Ayollar xonalari band bo'lish foizi
  },
  "by_status": {
    "available": 10,          // To'liq bo'sh xonalar (hech kim yo'q)
    "partially_occupied": 25, // Qisman band xonalar (joy bor)
    "fully_occupied": 15      // To'liq band xonalar (joy yo'q)
  }
}
```

### Yotoqxonalar Ro'yxati (Bo'sh Joylar bilan)

```bash
GET /api/dormitories/
Authorization: Bearer [token]

# Response:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Yotoqxona #1",
      "address": "Toshkent, Chilonzor",
      "university_name": "TATU",
      "month_price": 500000,
      "room_statistics": {
        "total": {
          "rooms": 50,
          "capacity": 200,
          "occupied": 150,
          "free": 50,
          "occupancy_rate": 75.0
        },
        "male": {
          "rooms": 30,
          "capacity": 120,
          "occupied": 90,
          "free": 30,
          "occupancy_rate": 75.0
        },
        "female": {
          "rooms": 20,
          "capacity": 80,
          "occupied": 60,
          "free": 20,
          "occupancy_rate": 75.0
        },
        "by_status": {
          "available": 10,
          "partially_occupied": 25,
          "fully_occupied": 15
        }
      }
    }
  ]
}
```

### Bo'sh Joylar Bo'yicha Filtrlash

```bash
# Faqat bo'sh joyi bor yotoqxonalarni ko'rish
GET /api/dormitories/?is_active=true

# Ma'lum universitetning yotoqxonalari
GET /api/dormitories/?university=1

# Qidiruv
GET /api/dormitories/?search=TATU
```

### Foydali Ma'lumotlar

1. **occupancy_rate** - Xonalar qanchalik to'lganligini ko'rsatadi (0-100%)
   - 0% = Hamma xonalar bo'sh
   - 100% = Hamma xonalar to'liq band
   - 75% = Xonalarning 75% band, 25% bo'sh

2. **free** - Hozir mavjud bo'sh o'rinlar soni
   - Talabalar shu raqamga qarab yotoqxona tanlashi mumkin

3. **by_status** - Xonalar holati
   - `available` = To'liq bo'sh xonalar (yangi talabalar uchun)
   - `partially_occupied` = Qisman band (xonadosh bilan)
   - `fully_occupied` = To'liq band (joy yo'q)

4. **male/female** - Jinsi bo'yicha ajratilgan statistika
   - Erkak talabalar faqat erkaklar statistikasiga qarashi kerak
   - Ayol talabalar faqat ayollar statistikasiga qarashi kerak
