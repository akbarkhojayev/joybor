# Qavat Sardori (Floor Leader) API Misollari

## Sardor Huquqlari

Qavat sardori (role='sardor') faqat o'z qavatidagi talabalarni ko'rishi va boshqarishi mumkin.

## 1. Sardor - O'z Qavatidagi Talabalar Ro'yxati

```bash
GET /api/students/
Authorization: Bearer [sardor_token]

# Response: Faqat o'z qavatidagi faol talabalar
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "name": "Alisher",
      "last_name": "Navoiy",
      "course": "1-kurs",
      "faculty": "Informatika",
      "group": "IT-101",
      "dormitory_name": "Yotoqxona #1",
      "floor_name": "2-qavat",
      "room_name": "201",
      "phone": "+998901234567",
      "is_active": true,
      "placement_status": "Joylashdi"
    }
  ]
}
```

## 2. Sardor - Talaba Ma'lumotlarini Ko'rish

```bash
GET /api/students/1/
Authorization: Bearer [sardor_token]

# Response: Faqat o'z qavatidagi talaba
{
  "id": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "middle_name": "Abdullayevich",
  "course": "1-kurs",
  "faculty": "Informatika",
  "group": "IT-101",
  "dormitory_name": "Yotoqxona #1",
  "floor_name": "2-qavat",
  "room_name": "201",
  "phone": "+998901234567",
  "is_active": true,
  "payments": [...],
  "payment_summary": {...}
}

# Agar boshqa qavatdagi talabani ko'rmoqchi bo'lsa:
# Response: 404 Not Found
```

## 3. Sardor - Talabalarni Qidirish

```bash
# Ism bo'yicha qidirish
GET /api/students/?search=Alisher
Authorization: Bearer [sardor_token]

# Xona bo'yicha filtrlash
GET /api/students/?room=5
Authorization: Bearer [sardor_token]

# Kurs bo'yicha filtrlash
GET /api/students/?course=1-kurs
Authorization: Bearer [sardor_token]

# Jinsi bo'yicha filtrlash
GET /api/students/?gender=Erkak
Authorization: Bearer [sardor_token]
```

## 4. Sardor - Davomat Sessiyasi Yaratish

```bash
POST /api/attendance-sessions/create/
Authorization: Bearer [sardor_token]
Content-Type: application/json

{
  "floor": 2,
  "leader": 1
}

# Response:
{
  "id": 1,
  "date": "2024-01-15",
  "floor": 2,
  "floor_name": "2-qavat",
  "leader": 1,
  "leader_name": "sardor_user",
  "created_at": "2024-01-15T10:00:00Z",
  "records": []
}
```

## 5. Sardor - Davomat Belgilash

```bash
POST /api/attendance-records/
Authorization: Bearer [sardor_token]
Content-Type: application/json

{
  "session": 1,
  "student": 5,
  "status": "in"
}

# Response:
{
  "id": 1,
  "session": 1,
  "student": 5,
  "student_name": "Alisher",
  "status": "in",
  "created_at": "2024-01-15T10:00:00Z"
}
```

## 6. Sardor - Yig'im Yaratish

```bash
POST /api/collections/create/
Authorization: Bearer [sardor_token]
Content-Type: application/json

{
  "title": "Qavat tozalash uchun yig'im",
  "amount": 50000,
  "description": "Har oylik qavat tozalash xarajatlari uchun",
  "deadline": "2024-01-31T23:59:59Z",
  "floor": 2,
  "leader": 1
}

# Response:
{
  "id": 1,
  "title": "Qavat tozalash uchun yig'im",
  "amount": 50000,
  "description": "Har oylik qavat tozalash xarajatlari uchun",
  "deadline": "2024-01-31T23:59:59Z",
  "floor": 2,
  "floor_name": "2-qavat",
  "leader": 1,
  "leader_name": "sardor_user",
  "created_at": "2024-01-15T10:00:00Z",
  "records": []
}
```

## 7. Sardor - Yig'im Yozuvlarini Boshqarish

```bash
POST /api/collection-records/
Authorization: Bearer [sardor_token]
Content-Type: application/json

{
  "collection": 1,
  "student": 5,
  "status": "To'lagan"
}

# Response:
{
  "id": 1,
  "collection": 1,
  "student": 5,
  "student_name": "Alisher",
  "status": "To'lagan"
}
```

## 8. Sardor - O'z Vazifalarini Ko'rish

```bash
GET /api/tasks-for-leaders/
Authorization: Bearer [sardor_token]

# Response: Faqat o'ziga berilgan vazifalar
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "user": 5,
      "user_name": "sardor_user",
      "description": "2-qavat xonalarini tekshirish",
      "status": "PENDING",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

## 9. Sardor - Vazifani Bajarish

```bash
PATCH /api/tasks-for-leaders/1/
Authorization: Bearer [sardor_token]
Content-Type: application/json

{
  "status": "IN_PROGRESS"
}

# Vazifa bajarilgandan keyin:
PATCH /api/tasks-for-leaders/1/
{
  "status": "COMPLETED"
}
```

## Sardor Cheklovlari

### ✅ Sardor Qila Oladi:
- O'z qavatidagi talabalarni ko'rish
- O'z qavatidagi talabalar ma'lumotlarini ko'rish
- Davomat sessiyasi yaratish
- Davomat belgilash
- Yig'im yaratish va boshqarish
- O'z vazifalarini ko'rish va bajarish

### ❌ Sardor Qila Olmaydi:
- Boshqa qavatdagi talabalarni ko'rish
- Talaba ma'lumotlarini tahrirlash (faqat admin)
- Talabani o'chirish (faqat admin)
- Talabaga xona biriktirish (faqat admin)
- To'lov qo'shish (faqat admin)
- Arizalarni tasdiqlash/rad etish (faqat admin)

## Xatoliklar

### 403 Forbidden - Ruxsat yo'q
```json
{
  "error": "Faqat admin talaba ma'lumotlarini tahrirlashi mumkin"
}
```

### 404 Not Found - Talaba topilmadi
```json
{
  "detail": "Not found."
}
```
Bu xatolik sardor boshqa qavatdagi talabani ko'rmoqchi bo'lganda yoki talaba mavjud bo'lmaganda chiqadi.

## Foydali Maslahatlar

1. **Filtrlash**: Sardor o'z qavatidagi talabalarni filtrlash uchun barcha filtrlash parametrlaridan foydalanishi mumkin
2. **Qidiruv**: `search` parametri ism, familiya, passport va telefon bo'yicha qidiradi
3. **Davomat**: Har kuni yangi davomat sessiyasi yaratish kerak
4. **Yig'im**: Yig'im yaratgandan keyin har bir talaba uchun yozuv yaratish kerak
