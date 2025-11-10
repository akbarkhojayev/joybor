from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'student'),
        ('admin', 'admin'),
        ('ijarachi', 'ijarachi'),
        ('sardor', 'sardor'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)
    email = models.EmailField(blank=True, null=True, unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='user_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telegram = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"

class Province(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=60)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=60)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name


class Amenity(models.Model):
    name = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Dormitory(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    month_price = models.IntegerField(blank=True, null=True)
    year_price = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    amenities = models.ManyToManyField(Amenity, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

class DormitoryImage(models.Model):
    image = models.ImageField(upload_to='dormitories/', blank=True, null=True)
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.dormitory.name


class Rule(models.Model):
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    rule = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.rule

class Floor(models.Model):
    name = models.CharField(max_length=60)
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    gender = models.CharField(choices=(('male', 'male'), ('female', 'female')), max_length=20, default='male')

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=60)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    capacity = models.IntegerField(blank=True, null=True)
    current_occupancy = models.IntegerField(default=0)
    gender = models.CharField(choices=(('male', 'male'), ('female', 'female')), max_length=20)
    status = models.CharField(choices=(('AVAILABLE', 'AVAILABLE'), ('PARTIALLY_OCCUPIED', 'PARTIALLY_OCCUPIED'),
                                       ('FULLY_OCCUPIED', 'FULLY_OCCUPIED')), max_length=20, default='AVAILABLE')

    def __str__(self):
        return self.name

class Student(models.Model):
    COURSE_CHOICES = (
    ('1-kurs', '1-kurs'),
    ('2-kurs', '2-kurs'),
    ('3-kurs', '3-kurs'),
    ('4-kurs', '4-kurs'),
    ('5-kurs', '5-kurs'),
    )

    GENDER_CHOICES = (
    ('Erkak','Erkak'),
    ('Ayol', 'Ayol'),
    )
    PLACEMENT_STATUS_CHOICES = (
        ('Qabul qilindi', 'Qabul qilindi'),
        ('Joylashdi', 'Joylashdi'),
    )
    STATUS_CHOICES = (
        ('Tekshirilmaydi', 'Tekshirilmaydi'),
        ('Tekshirilmoqda', 'Tekshirilmoqda'),
        ('Tasdiqlandi', 'Tasdiqlandi'),
        ('Rad etildi', 'Rad etildi'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', blank=True, null=True)
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    middle_name = models.CharField(max_length=120, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, default=1)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=1)
    faculty = models.CharField(max_length=120, blank=True, null=True)
    direction = models.CharField(max_length=120, blank=True, null=True)
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, blank=True, null=True, related_name='students')
    passport = models.CharField(max_length=9, unique=True, blank=True, null=True)
    group = models.CharField(max_length=120, blank=True, null=True)
    course = models.CharField(max_length=120, choices=COURSE_CHOICES, default='1-kurs')
    gender = models.CharField(max_length=120, choices=GENDER_CHOICES, default='Erkak')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='students', blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=25)
    picture = models.ImageField(upload_to='student_pictures/', blank=True, null=True)
    passport_image_first = models.ImageField(upload_to='passport_image/', blank=True, null=True)
    passport_image_second = models.ImageField(upload_to='passport_image/', blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    privilege = models.BooleanField(default=False)
    privilege_share = models.PositiveIntegerField(default=0)
    accepted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Tekshirilmaydi')
    placement_status = models.CharField(max_length=120, choices=PLACEMENT_STATUS_CHOICES, default='1-kurs')

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.name

class Application(models.Model):

    STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
    ('Cancelled', 'Cancelled'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='application', blank=True, null=True)
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True, null=True)
    middle_name = models.CharField(max_length=120, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, default=1)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=1)
    faculty = models.CharField(max_length=120, blank=True, null=True)
    direction = models.CharField(max_length=120, blank=True, null=True)
    course = models.CharField(max_length=120, blank=True, null=True)
    group = models.CharField(max_length=120, blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=25)
    passport = models.CharField(max_length=9, unique=True, blank=True, null=True)
    user_image = models.ImageField(upload_to='application_image/', blank=True, null=True)
    document = models.FileField(upload_to='application_documents/', blank=True, null=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default='Pending')
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    passport_image_first = models.ImageField(upload_to='passport_image/', blank=True, null=True)
    passport_image_second = models.ImageField(upload_to='passport_image/', blank=True, null=True)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

    def __str__(self):
        return self.name

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
    amount = models.IntegerField()
    paid_date = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField(blank=True, null=True)
    method = models.CharField(choices=(('Cash', 'Cash'), ('Card', 'Card')), max_length=20)
    status = models.CharField(choices=(('APPROVED', 'APPROVED'), ('CANCELLED', 'CANCELLED')),
                              max_length=20)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return self.student.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('IN_PROGRESS', 'IN_PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_date = models.DateTimeField(blank=True, null=True, help_text="Eslatma vaqti")
    reminder_sent = models.BooleanField(default=False, help_text="Eslatma yuborilganmi")

    def __str__(self):
        return self.description

class Apartment(models.Model):
    ROOM_TYPE_CHOICES = (
        ('1 kishilik', '1 kishilik'),
        ('2 kishilik', '2 kishilik'),
        ('3 kishilik', '3 kishilik'),
        ('Oilaviy', 'Oilaviy'),
    )
    GENDER_CHOICES = (
        ('Aralash', 'Aralash'),
        ('Erkak', 'Erkak'),
        ('Ayol', 'Ayol'),
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='apartments')
    exact_address = models.CharField(max_length=255, blank=True, null=True)
    monthly_price = models.IntegerField(blank=True, null=True)
    room_type = models.CharField(max_length=32, choices=ROOM_TYPE_CHOICES, default='Oilaviy')
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, default='Erkak')
    total_rooms = models.PositiveIntegerField(default=1)
    available_rooms = models.PositiveIntegerField(default=1)
    phone_number = models.CharField(blank=True, null=True, max_length=25)
    amenities = models.ManyToManyField(Amenity, related_name='apartments')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartments')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='apartment_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.apartment.title} - {self.id}"


class Notification(models.Model):
    TARGET_CHOICES = (
        ('all_students', 'Barcha studentlar'),
        ('all_admins', 'Barcha adminlar'),
        ('specific_user', 'Ma\'lum foydalanuvchi'),
    )
    message = models.TextField(help_text="Bildirishnoma matni")
    image = models.ImageField(upload_to='notifications/', blank=True, null=True, help_text="Bildirishnoma rasmi")
    target_type = models.CharField(max_length=20, choices=TARGET_CHOICES, default='specific_user')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,
                                    help_text="Agar specific_user tanlansa, bu foydalanuvchi")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Bildirishnoma faolmi")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.message} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications')
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='recipients')
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']
        unique_together = ['user', 'notification']

    def __str__(self):
        return f"{self.user.username} - {self.notification.message}"


class ApplicationNotification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="application_notifications"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"


class FloorLeader(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='leader')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='floor_leader')

    class Meta:
        unique_together = ("floor", "user")

    def __str__(self):
        return f"{self.user} - {self.floor} qavat sardori"


class AttendanceSession(models.Model):
    date = models.DateField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='sessions')
    leader = models.ForeignKey(FloorLeader, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("date", "floor")

    def __str__(self):
        return f"{self.date} - {self.floor} qavat davomat"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        IN = 'in', 'in'
        OUT = 'out', 'out'

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name="records"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "student")

    def __str__(self):
        return f"{self.student} - {self.session.date} - {self.status}"

class Collection(models.Model):
    title = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='collections', blank=True, null=True)
    leader = models.ForeignKey('FloorLeader', on_delete=models.CASCADE, related_name='collections', blank=True, null=True)

    def __str__(self):
        return self.title


class CollectionRecord(models.Model):
    class Status(models.TextChoices):
        PAID = "To‘lagan", "To‘lagan"
        UNPAID = "To‘lamagan", "To‘lamagan"

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='collection_records')
    status = models.CharField(choices=Status.choices, max_length=30)

    class Meta:
        unique_together = ("collection", "student")

    def __str__(self):
        return f"{self.student} - {self.collection} ({self.status})"


class TaskForLeader(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Kutilmoqda'),
        ('IN_PROGRESS', 'Jarayonda'),
        ('COMPLETED', 'Bajarilgan'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_fpr_leaders')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class DutySchedule(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='schedules')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.floor} - {self.room} - {self.date}"