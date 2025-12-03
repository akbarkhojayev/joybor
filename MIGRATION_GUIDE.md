# Migration Qo'llanmasi

## Room modeliga gender field qo'shildi

Room modeliga `gender` field qo'shildi. Bu field talabaning jinsi va xona jinsi mos kelishini tekshirish uchun kerak.

### Migration yaratish va qo'llash

```bash
# 1. Migration yaratish
python manage.py makemigrations

# 2. Migration qo'llash
python manage.py migrate
```

### Agar migration paytida xato bo'lsa

Agar mavjud Room obyektlari uchun default qiymat so'ralsa, quyidagilarni bajaring:

**Variant 1: Default qiymat berish**
```
Select an option: 1
Please enter the default value as valid Python.
>>> 'male'
```

**Variant 2: Migration faylini o'zgartirish**

Agar ko'p xonalar bo'lsa va ularni qo'lda o'zgartirish kerak bo'lsa:

1. Migration yarating
2. Migration faylini oching (masalan: `main/migrations/0002_room_gender.py`)
3. Quyidagi kodni qo'shing:

```python
from django.db import migrations, models

def set_room_gender_based_on_floor(apps, schema_editor):
    Room = apps.get_model('main', 'Room')
    Floor = apps.get_model('main', 'Floor')
    
    for room in Room.objects.all():
        if room.floor:
            # Qavat jinsi asosida xona jinsini belgilash
            room.gender = room.floor.gender
            room.save()

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0001_initial'),  # Oldingi migration nomi
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=20),
        ),
        migrations.RunPython(set_room_gender_based_on_floor),
    ]
```

### Mavjud ma'lumotlarni yangilash

Agar migration qo'llanganidan keyin xonalarning jinsini o'zgartirish kerak bo'lsa:

```python
# Django shell
python manage.py shell

from main.models import Room, Floor

# Barcha xonalarni qavat jinsi asosida yangilash
for room in Room.objects.all():
    if room.floor:
        room.gender = room.floor.gender
        room.save()
        print(f"Room {room.name} - {room.gender}")
```

### Admin panelda yangilash

Admin panelda har bir xonaning jinsini qo'lda o'zgartirish mumkin:

1. Admin panelga kiring: http://localhost:8000/admin/
2. Rooms bo'limiga o'ting
3. Har bir xonani tahrirlang va gender ni tanlang

### Tekshirish

```bash
python manage.py shell

from main.models import Room

# Barcha xonalarni ko'rish
for room in Room.objects.all():
    print(f"{room.name} - Floor: {room.floor.name} - Gender: {room.gender}")
```

## Muhim Eslatmalar

1. **Migration qo'llashdan oldin** - Ma'lumotlar bazasini backup qiling
2. **Gender field** - Har bir xona uchun jinsi belgilangan bo'lishi kerak
3. **Floor va Room** - Xona jinsi odatda qavat jinsi bilan bir xil bo'ladi
4. **Validatsiya** - Talaba xonaga joylashtirilganda jinsi tekshiriladi

## Xatolarni bartaraf etish

### AttributeError: 'Room' object has no attribute 'gender'

Bu xato migration qo'llanmaganligini bildiradi. Yuqoridagi qadamlarni bajaring.

### IntegrityError

Agar unique constraint xatosi bo'lsa, ma'lumotlar bazasida dublikat ma'lumotlar bor. Ularni tozalang.
