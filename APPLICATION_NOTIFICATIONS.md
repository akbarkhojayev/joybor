# Ariza Bildirishnomalari

## Bildirishnoma Oqimi

```
Student                Admin                 Student
   |                     |                      |
   |--1. Ariza yuborish->|                      |
   |                     |<-Bildirishnoma       |
   |                     |  "Yangi ariza keldi" |
   |                     |                      |
   |                     |--2. Tasdiqlash       |
   |                     |                      |
   |<--------------------|-Bildirishnoma--------|
   |  "Arizangiz tasdiqlandi"                  |
```

## 1. Student Ariza Yuboradi

```bash
POST /api/applications/create/
Authorization: Bearer [student_token]
Content-Type: multipart/form-data

{
  "dormitory": 1,
  "name": "Alisher",
  "last_name": "Navoiy",
  "passport": "AB1234567",
  "faculty": "Informatika",
  "course": "1-kurs",
  ...
}

# Response:
{
  "id": 1,
  "name": "Alisher",
  "status": "Pending",
  ...
}
```

### Natija:
✅ Ariza yaratildi
✅ Admin bildirishnoma oldi: "Yangi ariza keldi: Alisher Navoiy (AB1234567). Fakultet: Informatika"

## 2. Admin Bildirishnomani Ko'radi

```bash
GET /api/notifications/
Authorization: Bearer [admin_token]

# Response:
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "type": "application",
      "message": "Yangi ariza keldi: Alisher Navoiy (AB1234567). Fakultet: Informatika",
      "is_read": false,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ]
}
```

## 3. Admin Arizani Tasdiqlaydi

```bash
PUT /api/applications/1/approve/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi."
}

# Response:
{
  "message": "Ariza tasdiqlandi va talaba ro'yxatga olindi",
  "admin_comment": "Barcha hujjatlar to'liq. Tasdiqlandi.",
  ...
}
```

### Natija:
✅ Ariza tasdiqlandi
✅ Student yaratildi
✅ Student bildirishnoma oldi: "Tabriklaymiz! Arizangiz tasdiqlandi. Siz Yotoqxona #1 yotoqxonasiga qabul qilindingiz."

## 4. Student Bildirishnomani Ko'radi

```bash
GET /api/notifications/
Authorization: Bearer [student_token]

# Response:
{
  "count": 1,
  "results": [
    {
      "id": 2,
      "type": "application",
      "message": "Tabriklaymiz! Arizangiz tasdiqlandi. Siz Yotoqxona #1 yotoqxonasiga qabul qilindingiz.",
      "is_read": false,
      "created_at": "2024-01-15T10:05:00Z"
    }
  ]
}
```

## 5. Admin Arizani Rad Etadi (Alternativ)

```bash
PUT /api/applications/1/reject/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "admin_comment": "Passport rasmlari aniq emas. Iltimos, qayta yuklang."
}

# Response:
{
  "message": "Ariza rad etildi",
  "admin_comment": "Passport rasmlari aniq emas. Iltimos, qayta yuklang.",
  ...
}
```

### Natija:
✅ Ariza rad etildi
✅ Student bildirishnoma oldi: "Arizangiz rad etildi. Sabab: Passport rasmlari aniq emas. Iltimos, qayta yuklang."

## Bildirishnoma Turlari

### Admin Uchun:
1. **Yangi Ariza** - Student ariza yuborsa
   ```
   "Yangi ariza keldi: [Ism] [Familiya] ([Passport]). Fakultet: [Fakultet]"
   ```

### Student Uchun:
1. **Ariza Tasdiqlandi**
   ```
   "Tabriklaymiz! Arizangiz tasdiqlandi. Siz [Yotoqxona nomi] yotoqxonasiga qabul qilindingiz."
   ```

2. **Ariza Rad Etildi**
   ```
   "Arizangiz rad etildi. Sabab: [Admin izohi]"
   ```

3. **Xonaga Joylashtirildi**
   ```
   "Siz [Qavat nomi] qavat, [Xona nomi] xonaga joylashtirilgansiz."
   ```

4. **Xonadan Chiqarildi**
   ```
   "Siz [Qavat nomi] qavat, [Xona nomi] xonadan chiqarildingiz."
   ```

5. **To'lov Qabul Qilindi**
   ```
   "To'lovingiz qabul qilindi. Summa: [Summa] so'm. Amal qilish muddati: [Sana]"
   ```

6. **To'lov Tasdiqlandi**
   ```
   "To'lovingiz tasdiqlandi. Summa: [Summa] so'm. Amal qilish muddati: [Sana]"
   ```

7. **To'lov Bekor Qilindi**
   ```
   "To'lovingiz bekor qilindi. Summa: [Summa] so'm. Sabab: [Sabab]"
   ```

## Bildirishnomalarni Boshqarish

### O'qilgan Deb Belgilash
```bash
POST /api/notifications/mark-read/
Authorization: Bearer [token]
Content-Type: application/json

{
  "type": "application",
  "id": 1
}
```

### Barcha Bildirishnomalarni O'qilgan Deb Belgilash
```bash
POST /api/notifications/mark-all-read/
Authorization: Bearer [token]
```

### O'qilmagan Bildirishnomalar Soni
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

## Test Qilish

### 1. Student Ariza Yuboradi
```bash
POST /api/applications/create/
Authorization: Bearer [student_token]
{...}
```

### 2. Admin Bildirishnomani Tekshiradi
```bash
GET /api/notifications/
Authorization: Bearer [admin_token]

# Kutilayotgan:
"Yangi ariza keldi: ..."
```

### 3. Admin Arizani Tasdiqlaydi
```bash
PUT /api/applications/1/approve/
Authorization: Bearer [admin_token]
```

### 4. Student Bildirishnomani Tekshiradi
```bash
GET /api/notifications/
Authorization: Bearer [student_token]

# Kutilayotgan:
"Tabriklaymiz! Arizangiz tasdiqlandi..."
```

## Xulosa

Endi ariza yuborilganda:
1. ✅ Admin bildirishnoma oladi
2. ✅ Admin arizani ko'rib chiqadi
3. ✅ Admin tasdiqlasa/rad etsa, student bildirishnoma oladi
4. ✅ Barcha bildirishnomalar `/api/notifications/` da ko'rinadi
