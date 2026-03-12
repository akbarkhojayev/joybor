# Bildirishnoma Muammosini Hal Qilish

## Muammo
Ariza tasdiqlanganda studentga bildirishnoma bormayapti.

## Bildirishnoma Turlari

### 1. Student → Admin (Yangi Ariza)
Student ariza yuborsa, yotoqxona adminiga bildirishnoma keladi:
```
"Yangi ariza keldi: Alisher Navoiy (AB1234567). Fakultet: Informatika"
```

### 2. Admin → Student (Ariza Tasdiqlandi)
Admin arizani tasdiqlasa, studentga bildirishnoma keladi:
```
"Tabriklaymiz! Arizangiz tasdiqlandi. Siz Yotoqxona #1 yotoqxonasiga qabul qilindingiz."
```

### 3. Admin → Student (Ariza Rad Etildi)
Admin arizani rad etsa, studentga bildirishnoma keladi:
```
"Arizangiz rad etildi. Sabab: Hujjatlar to'liq emas"
```

## Sabablari va Yechimlar

### 1. User Biriktirilmagan
**Sabab**: Ariza yaratilganda `user` field to'ldirilmagan bo'lishi mumkin.

**Yechim**: ApplicationCreateView da user avtomatik biriktiriladi:
```python
def perform_create(self, serializer):
    if self.request.user.is_authenticated:
        serializer.save(user=self.request.user)
    else:
        serializer.save()
```

### 2. Signal Ishlamayapti
**Sabab**: Signal to'g'ri import qilinmagan yoki apps.py da ready() metodi yo'q.

**Tekshirish**:
```python
# main/apps.py
class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # Bu qator bo'lishi kerak
```

### 3. Bildirishnoma Yaratilgan, Lekin Ko'rinmayapti
**Sabab**: API endpoint noto'g'ri ishlayapti.

**Tekshirish**:
```bash
# Bildirishnomalarni ko'rish
GET /api/notifications/
Authorization: Bearer [student_token]

# O'qilmagan bildirishnomalar soni
GET /api/notifications/unread-count/
Authorization: Bearer [student_token]
```

## Test Qilish Jarayoni

### 1. Ariza Yaratish (Student)
```bash
POST /api/applications/create/
Authorization: Bearer [student_token]
Content-Type: multipart/form-data

{
  "dormitory": 1,
  "name": "Test",
  "last_name": "Student",
  "province": 1,
  "district": 1,
  "faculty": "IT",
  "course": "1-kurs",
  "passport": "AB1234567",
  "phone": "+998901234567"
}
```

### 2. Arizani Tasdiqlash (Admin)
```bash
PUT /api/applications/1/approve/
Authorization: Bearer [admin_token]
Content-Type: application/json

{
  "admin_comment": "Tasdiqlandi"
}
```

### 3. Bildirishnomani Tekshirish (Student)
```bash
GET /api/notifications/
Authorization: Bearer [student_token]

# Kutilayotgan response:
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "type": "application",
      "message": "Tabriklaymiz! Arizangiz tasdiqlandi. Siz Yotoqxona #1 yotoqxonasiga qabul qilindingiz.",
      "is_read": false,
      "created_at": "2024-01-15T10:00:00Z",
      "image": null
    }
  ]
}
```

### 4. Database Tekshirish
```bash
# Django shell orqali
python manage.py shell

# ApplicationNotification larni tekshirish
from main.models import ApplicationNotification, User
user = User.objects.get(username='student_username')
notifications = ApplicationNotification.objects.filter(user=user)
print(notifications.count())
for n in notifications:
    print(f"ID: {n.id}, Message: {n.message}, Read: {n.is_read}")
```

## Agar Hali Ham Ishlamasa

### 1. Signal Qo'lda Chaqirish
```python
# Django shell
from main.models import Application
from main.signals import handle_application_approval

app = Application.objects.get(id=1)
handle_application_approval(Application, app, created=False, kwargs={})
```

### 2. Bildirishnomani Qo'lda Yaratish
```python
# Django shell
from main.models import ApplicationNotification, User, Application

app = Application.objects.get(id=1)
user = app.user

if user:
    ApplicationNotification.objects.create(
        user=user,
        message=f"Tabriklaymiz! Arizangiz tasdiqlandi. Siz {app.dormitory.name} yotoqxonasiga qabul qilindingiz."
    )
    print("Bildirishnoma yaratildi!")
else:
    print("User topilmadi!")
```

### 3. Log Tekshirish
Signal da print qo'shilgan:
```python
# Agar user yo'q bo'lsa
print(f"WARNING: Application {instance.id} approved but no user assigned!")
```

Server loglarini tekshiring:
```bash
# Development server loglarida ko'rinadi
python manage.py runserver
```

## Tuzatilgan Xususiyatlar

1. ✅ ApplicationCreateView da user avtomatik biriktiriladi
2. ✅ Signal da user mavjudligi tekshiriladi
3. ✅ Takroriy bildirishnoma yuborilmaydi (existing_notification check)
4. ✅ Debug uchun print qo'shilgan
5. ✅ Agar student allaqachon mavjud bo'lsa ham bildirishnoma yuboriladi

## API Endpointlar

### Bildirishnomalar
- `GET /api/notifications/` - Barcha bildirishnomalar
- `GET /api/notifications/?is_read=false` - O'qilmagan bildirishnomalar
- `GET /api/notifications/unread-count/` - O'qilmagan soni
- `POST /api/notifications/mark-read/` - O'qilgan deb belgilash
- `POST /api/notifications/mark-all-read/` - Hammasini o'qilgan deb belgilash

### Arizalar
- `POST /api/applications/create/` - Ariza yaratish
- `GET /api/applications/` - Arizalar ro'yxati
- `PUT /api/applications/{id}/approve/` - Arizani tasdiqlash
- `PUT /api/applications/{id}/reject/` - Arizani rad etish

## Xulosa

Agar bildirishnoma hali ham bormasa:
1. User biriktirilganligini tekshiring (Application.user)
2. Signal ishlaganligini tekshiring (print loglar)
3. ApplicationNotification yaratilganligini tekshiring (database)
4. API endpoint to'g'ri ishlayotganligini tekshiring (GET /api/notifications/)
