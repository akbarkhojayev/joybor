# To'lovlar (Payments) API

## To'lovlar Tizimi Qanday Ishlaydi?

Admin talabalar uchun to'lovlarni qo'shadi va boshqaradi. Talabalar o'z to'lovlarini ko'rishi mumkin.

## 1. To'lov Qo'shish (Admin)

```bash
POST /api/payments/create/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "student": 5,
  "amount": 500000,
  "valid_until": "2024-02-15",
  "method": "Card",
  "status": "APPROVED",
  "comment": "Yanvar oyi uchun to'lov"
}

# Response:
{
  "id": 1,
  "student_info": {
    "id": 5,
    "name": "Alisher Navoiy",
    "course": "1-kurs",
    "group": "IT-101",
    "room_name": "201",
    "floor_name": "2-qavat"
  },
  "student": 5,
  "dormitory": 1,
  "dormitory_name": "Yotoqxona #1",
  "amount": 500000,
  "paid_date": "2024-01-15T10:00:00Z",
  "valid_until": "2024-02-15",
  "method": "Card",
  "status": "APPROVED",
  "comment": "Yanvar oyi uchun to'lov"
}
```

## 2. To'lovlar Ro'yxati (Admin)

```bash
GET /api/payments/
Authorization: Bearer [admin_token]

# Response:
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "student_info": {
        "id": 5,
        "name": "Alisher Navoiy",
        "course": "1-kurs",
        "group": "IT-101"
      },
      "amount": 500000,
      "paid_date": "2024-01-15T10:00:00Z",
      "status": "APPROVED"
    }
  ]
}
```

## 3. Filtrlash va Saralash

```bash
# Ma'lum talaba to'lovlari
GET /api/payments/?student=5

# Faqat tasdiqlangan to'lovlar
GET /api/payments/?status=APPROVED

# Faqat bekor qilingan to'lovlar
GET /api/payments/?status=CANCELLED

# Karta orqali to'lovlar
GET /api/payments/?method=Card

# Naqd to'lovlar
GET /api/payments/?method=Cash

# Saralash (eng yangi birinchi)
GET /api/payments/?ordering=-paid_date

# Saralash (eng katta summa birinchi)
GET /api/payments/?ordering=-amount
```



## 4. To'lovni Ko'rish (Admin)

```bash
GET /api/payments/1/
Authorization: Bearer [admin_token]

# Response:
{
  "id": 1,
  "student_info": {
    "id": 5,
    "name": "Alisher Navoiy",
    "course": "1-kurs",
    "group": "IT-101",
    "room_name": "201",
    "floor_name": "2-qavat"
  },
  "student": 5,
  "dormitory": 1,
  "dormitory_name": "Yotoqxona #1",
  "amount": 500000,
  "paid_date": "2024-01-15T10:00:00Z",
  "valid_until": "2024-02-15",
  "method": "Card",
  "status": "APPROVED",
  "comment": "Yanvar oyi uchun to'lov"
}
```

## 5. To'lovni Tahrirlash (Admin)

```bash
PUT /api/payments/1/
# yoki
PATCH /api/payments/1/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "status": "CANCELLED",
  "comment": "Xato to'lov, qaytarildi"
}

# Response:
{
  "id": 1,
  "status": "CANCELLED",
  "comment": "Xato to'lov, qaytarildi",
  ...
}

# Talabaga bildirishnoma yuboriladi:
# "To'lovingiz bekor qilindi. Summa: 500000 so'm. Sabab: Xato to'lov, qaytarildi"
```

## 6. To'lovni O'chirish (Admin)

```bash
DELETE /api/payments/1/
Authorization: Bearer [admin_token]

# Response: 204 No Content
```

## 7. Talaba O'z To'lovlarini Ko'rish

```bash
GET /api/student/payments/
Authorization: Bearer [student_token]

# Response:
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "amount": 500000,
      "paid_date": "2024-01-15T10:00:00Z",
      "valid_until": "2024-02-15",
      "method": "Card",
      "status": "APPROVED",
      "comment": "Yanvar oyi uchun to'lov"
    }
  ]
}
```

## Bildirishnomalar

To'lov qo'shilganda yoki o'zgartirilganda talabaga avtomatik bildirishnoma yuboriladi:

### To'lov Tasdiqlanganda:
```
"To'lovingiz qabul qilindi. Summa: 500000 so'm. Amal qilish muddati: 2024-02-15"
```

### To'lov Bekor Qilinganda:
```
"To'lovingiz bekor qilindi. Summa: 500000 so'm. Sabab: Xato to'lov, qaytarildi"
```

## To'lov Statuslari

- `APPROVED` - Tasdiqlangan to'lov
- `CANCELLED` - Bekor qilingan to'lov

## To'lov Usullari

- `Card` - Karta orqali
- `Cash` - Naqd pul

## Muhim Eslatmalar

1. **Dormitory Avtomatik Aniqlanadi**:
   - Agar talaba floor ga biriktirilgan bo'lsa → floor.dormitory
   - Agar talaba dormitory ga biriktirilgan bo'lsa → student.dormitory
   - Agar admin o'z yotoqxonasiga qo'shayotgan bo'lsa → admin.dormitory

2. **Talaba Biriktirilmagan Bo'lsa**:
   ```json
   {
     "error": "Talaba hech qaysi yotoqxonaga biriktirilmagan. Avval talabani yotoqxonaga biriktiring."
   }
   ```

3. **Bildirishnoma**:
   - To'lov yaratilganda (status=APPROVED)
   - Status APPROVED ga o'zgartirilganda
   - Status CANCELLED ga o'zgartirilganda

4. **Huquqlar**:
   - Faqat admin to'lov qo'shishi/tahrirlashi mumkin
   - Talaba faqat o'z to'lovlarini ko'rishi mumkin
   - Admin faqat o'z yotoqxonasidagi to'lovlarni ko'radi

## Xatolar

### 400 Bad Request
```json
{
  "error": "Talaba hech qaysi yotoqxonaga biriktirilmagan"
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```
