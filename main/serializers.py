from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'email', 'phone', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        request_user = self.context['request'].user
        role = attrs.get('role')
        dormitory = attrs.get('dormitory')

        if request_user.role == 'admin':
            if role in ['teacher', 'student', 'manager']:
                if not dormitory or dormitory.admin != request_user:
                    raise serializers.ValidationError("Siz faqat o'z Dormitoryingizga foydalanuvchi qo'sha olasiz.")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    student_info = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()
    payment_summary = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'image',
            'bio',
            'phone',
            'birth_date',
            'address',
            'telegram',
            'student_info',
            'payments',
            'payment_summary',
        ]
    
    def get_student_info(self, obj):
        """Agar foydalanuvchi talaba bo'lsa, talaba ma'lumotlari"""
        try:
            student = Student.objects.get(user=obj.user)
            return {
                'id': student.id,
                'name': f"{student.name} {student.last_name}",
                'course': student.course,
                'faculty': student.faculty,
                'group': student.group,
                'dormitory_name': student.dormitory.name if student.dormitory else None,
                'room_name': student.room.name if student.room else None,
                'is_active': student.is_active,
                'placement_status': student.placement_status,
            }
        except Student.DoesNotExist:
            return None
    
    def get_payments(self, obj):
        """Agar talaba bo'lsa, oxirgi 10 ta to'lov"""
        try:
            student = Student.objects.get(user=obj.user)
            payments = Payment.objects.filter(student=student).order_by('-paid_date')[:10]
            return [{
                'id': payment.id,
                'amount': payment.amount,
                'paid_date': payment.paid_date,
                'valid_until': payment.valid_until,
                'method': payment.method,
                'status': payment.status,
                'comment': payment.comment,
            } for payment in payments]
        except Student.DoesNotExist:
            return []
    
    def get_payment_summary(self, obj):
        """To'lovlar xulosasi"""
        try:
            student = Student.objects.get(user=obj.user)
            payments = Payment.objects.filter(student=student)
            
            total_payments = payments.count()
            approved_payments = payments.filter(status='APPROVED').count()
            total_amount = sum(p.amount for p in payments.filter(status='APPROVED'))
            
            # Oxirgi to'lov
            last_payment = payments.filter(status='APPROVED').order_by('-paid_date').first()
            last_payment_date = last_payment.paid_date if last_payment else None
            last_payment_amount = last_payment.amount if last_payment else 0
            
            # Qarzdorlik (30 kundan ko'p to'lov qilmagan)
            from django.utils import timezone
            from datetime import timedelta
            thirty_days_ago = timezone.now() - timedelta(days=30)
            is_debtor = not payments.filter(status='APPROVED', paid_date__gte=thirty_days_ago).exists()
            
            return {
                'total_payments': total_payments,
                'approved_payments': approved_payments,
                'total_amount': total_amount,
                'last_payment_date': last_payment_date,
                'last_payment_amount': last_payment_amount,
                'is_debtor': is_debtor,
            }
        except Student.DoesNotExist:
            return None

class UserMeSerializer(serializers.ModelSerializer):
    """Joriy foydalanuvchi profili - ko'rish va tahrirlash"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    role = serializers.CharField(source='user.role', read_only=True)
    user_phone = serializers.CharField(source='user.phone', required=False, allow_blank=True, allow_null=True)

    student_info = serializers.SerializerMethodField()
    recent_payments = serializers.SerializerMethodField()
    payment_summary = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'user_phone',
            'image',
            'bio',
            'phone',
            'birth_date',
            'address',
            'telegram',
            'student_info',
            'recent_payments',
            'payment_summary',
        ]
    
    def get_student_info(self, obj):
        """Agar foydalanuvchi talaba bo'lsa, talaba ma'lumotlari"""
        try:
            student = Student.objects.get(user=obj.user)
            return {
                'id': student.id,
                'name': f"{student.name} {student.last_name}",
                'course': student.course,
                'faculty': student.faculty,
                'group': student.group,
                'dormitory_name': student.dormitory.name if student.dormitory else None,
                'room_name': student.room.name if student.room else None,
                'is_active': student.is_active,
                'placement_status': student.placement_status,
            }
        except Student.DoesNotExist:
            return None
    
    def get_recent_payments(self, obj):
        """Oxirgi 5 ta to'lov"""
        try:
            student = Student.objects.get(user=obj.user)
            payments = Payment.objects.filter(student=student).order_by('-paid_date')[:5]
            return [{
                'id': payment.id,
                'amount': payment.amount,
                'paid_date': payment.paid_date,
                'valid_until': payment.valid_until,
                'method': payment.method,
                'status': payment.status,
                'comment': payment.comment,
            } for payment in payments]
        except Student.DoesNotExist:
            return []
    
    def get_payment_summary(self, obj):
        """To'lovlar xulosasi"""
        try:
            student = Student.objects.get(user=obj.user)
            payments = Payment.objects.filter(student=student)
            
            total_payments = payments.count()
            approved_payments = payments.filter(status='APPROVED').count()
            total_amount = sum(p.amount for p in payments.filter(status='APPROVED'))
            
            # Oxirgi to'lov
            last_payment = payments.filter(status='APPROVED').order_by('-paid_date').first()
            last_payment_date = last_payment.paid_date if last_payment else None
            
            # Qarzdorlik (30 kundan ko'p to'lov qilmagan)
            from django.utils import timezone
            from datetime import timedelta
            thirty_days_ago = timezone.now() - timedelta(days=30)
            is_debtor = not payments.filter(status='APPROVED', paid_date__gte=thirty_days_ago).exists()
            
            return {
                'total_payments': total_payments,
                'approved_payments': approved_payments,
                'total_amount': total_amount,
                'last_payment_date': last_payment_date,
                'is_debtor': is_debtor,
            }
        except Student.DoesNotExist:
            return None
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        if 'email' in user_data:
            user.email = user_data['email']
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'phone' in user_data:
            user.phone = user_data['phone']
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2','phone', 'email', 'role', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class DormitoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DormitoryImage
        fields = '__all__'
        extra_kwargs = {
            'dormitory': {'read_only': True}
        }


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        read_only_fields = ['dormitory']

class FloorSerializer(serializers.ModelSerializer):
    available_rooms = serializers.IntegerField(read_only=True)
    partially_occupied_rooms = serializers.IntegerField(read_only=True)
    fully_occupied_rooms = serializers.IntegerField(read_only=True)

    class Meta:
        model = Floor
        fields = ['id', 'name', 'gender',
                  'available_rooms',
                  'partially_occupied_rooms',
                  'fully_occupied_rooms']

class RoomStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'last_name', 'course', 'group', 'phone']


class RoomSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    students = RoomStudentSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['current_occupancy', 'status']



class DormitorySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    images = DormitoryImageSerializer(many=True, read_only=True)
    amenities_list = AmenitySerializer(source='amenities', many=True, read_only=True)
    rules = RuleSerializer(source='rule_set', many=True, read_only=True)
    room_statistics = serializers.SerializerMethodField()
    
    class Meta:
        model = Dormitory
        fields = '__all__'
    
    def get_room_statistics(self, obj):
        """Yotoqxona xonalari va bo'sh joylar statistikasi (real Student soni)"""
        from django.db.models import Count

        rooms = Room.objects.filter(floor__dormitory=obj)
        room_ids = list(rooms.values_list('id', flat=True))

        occ_qs = (
            Student.objects.filter(room_id__in=room_ids, is_active=True)
            .values('room_id')
            .annotate(cnt=Count('id'))
        )
        occ_map = {r['room_id']: r['cnt'] for r in occ_qs}

        m_rooms = rooms.filter(gender='male')
        f_rooms = rooms.filter(gender='female')

        t_cap = sum(r.capacity or 0 for r in rooms)
        m_cap = sum(r.capacity or 0 for r in m_rooms)
        f_cap = sum(r.capacity or 0 for r in f_rooms)

        t_occ = sum(occ_map.values())

        # Talaba jinsi bo'yicha (Student.gender ga qarab)
        m_occ = Student.objects.filter(
            room_id__in=room_ids, is_active=True, gender='Erkak'
        ).count()
        f_occ = Student.objects.filter(
            room_id__in=room_ids, is_active=True, gender='Ayol'
        ).count()

        def rate(occ, cap):
            return round(occ / cap * 100, 1) if cap > 0 else 0.0

        # Status real hisoblash
        available = partially = fully = 0
        for r in rooms:
            occ = occ_map.get(r.id, 0)
            cap = r.capacity or 0
            if occ == 0:
                available += 1
            elif cap > 0 and occ >= cap:
                fully += 1
            else:
                partially += 1

        return {
            'total':  {'rooms': rooms.count(), 'capacity': t_cap, 'occupied': t_occ, 'free': max(t_cap - t_occ, 0), 'occupancy_rate': rate(t_occ, t_cap)},
            'male':   {'rooms': m_rooms.count(), 'capacity': m_cap, 'occupied': m_occ, 'free': max(m_cap - m_occ, 0), 'occupancy_rate': rate(m_occ, m_cap)},
            'female': {'rooms': f_rooms.count(), 'capacity': f_cap, 'occupied': f_occ, 'free': max(f_cap - f_occ, 0), 'occupancy_rate': rate(f_occ, f_cap)},
            'by_status': {'available': available, 'partially_occupied': partially, 'fully_occupied': fully},
        }


class StudentSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    payments = serializers.SerializerMethodField()
    payment_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def get_payments(self, obj):
        """Talabaning barcha to'lovlari"""
        payments = Payment.objects.filter(student=obj).order_by('-paid_date')[:10]
        return [{
            'id': payment.id,
            'amount': payment.amount,
            'paid_date': payment.paid_date,
            'valid_until': payment.valid_until,
            'method': payment.method,
            'status': payment.status,
            'comment': payment.comment,
        } for payment in payments]
    
    def get_payment_summary(self, obj):
        """To'lovlar xulosasi"""
        payments = Payment.objects.filter(student=obj)
        
        total_payments = payments.count()
        approved_payments = payments.filter(status='APPROVED').count()
        total_amount = sum(p.amount for p in payments.filter(status='APPROVED'))
        
        # Oxirgi to'lov
        last_payment = payments.filter(status='APPROVED').order_by('-paid_date').first()
        last_payment_date = last_payment.paid_date if last_payment else None
        last_payment_amount = last_payment.amount if last_payment else 0
        
        # Qarzdorlik (30 kundan ko'p to'lov qilmagan)
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        is_debtor = not payments.filter(status='APPROVED', paid_date__gte=thirty_days_ago).exists()
        
        return {
            'total_payments': total_payments,
            'approved_payments': approved_payments,
            'total_amount': total_amount,
            'last_payment_date': last_payment_date,
            'last_payment_amount': last_payment_amount,
            'is_debtor': is_debtor,
        }


class RoommateSerializer(serializers.ModelSerializer):
    """Xonadoshlar uchun sodda serializer"""
    class Meta:
        model = Student
        fields = ['id', 'name', 'last_name', 'middle_name', 'course', 'faculty', 'phone', 'picture']


class StudentDashboardSerializer(serializers.ModelSerializer):
    """Talaba dashboard uchun to'liq ma'lumotlar"""
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_info = serializers.SerializerMethodField()
    floor_info = serializers.SerializerMethodField()
    room_info = serializers.SerializerMethodField()
    roommates = serializers.SerializerMethodField()
    recent_payments = serializers.SerializerMethodField()
    application_info = serializers.SerializerMethodField()
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'
    
    def get_dormitory_info(self, obj):
        if obj.dormitory:
            return {
                'id': obj.dormitory.id,
                'name': obj.dormitory.name,
                'address': obj.dormitory.address,
                'month_price': obj.dormitory.month_price,
                'year_price': obj.dormitory.year_price,
            }
        return None
    
    def get_floor_info(self, obj):
        if obj.floor:
            return {
                'id': obj.floor.id,
                'name': obj.floor.name,
                'gender': obj.floor.gender,
            }
        return None
    
    def get_room_info(self, obj):
        if obj.room:
            real_occ = Student.objects.filter(room=obj.room, is_active=True).count()
            cap = obj.room.capacity or 0
            return {
                'id': obj.room.id,
                'name': obj.room.name,
                'capacity': cap,
                'current_occupancy': real_occ,
                'free': max(cap - real_occ, 0),
                'status': obj.room.status,
            }
        return None
    
    def get_roommates(self, obj):
        if obj.room:
            roommates = Student.objects.filter(room=obj.room).exclude(id=obj.id)
            return RoommateSerializer(roommates, many=True).data
        return []
    
    def get_recent_payments(self, obj):
        payments = Payment.objects.filter(student=obj).order_by('-paid_date')[:5]
        return PaymentSerializer(payments, many=True).data
    
    def get_application_info(self, obj):
        """Talabaning yuborgan arizasi ma'lumotlari"""
        if obj.user:
            try:
                application = Application.objects.get(user=obj.user)
                return {
                    'id': application.id,
                    'status': application.status,
                    'created_at': application.created_at,
                    'admin_comment': application.admin_comment,
                    'dormitory_name': application.dormitory.name if application.dormitory else None,
                }
            except Application.DoesNotExist:
                return None
        return None


class ApplicationSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    gender = serializers.ChoiceField(
        choices=[('Erkak', 'Erkak'), ('Ayol', 'Ayol')],
        required=True,
        help_text="Erkak yoki Ayol"
    )

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('status', 'admin_comment', 'user')

class ApplicationAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'comment']

class PaymentSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField()
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'student_info', 'student', 'dormitory', 'dormitory_name', 'amount', 'paid_date', 'valid_until', 'method', 'status', 'comment']
        read_only_fields = ['dormitory', 'paid_date']
    
    def get_student_info(self, obj):
        """Talaba haqida qisqacha ma'lumot"""
        return {
            'id': obj.student.id,
            'name': f"{obj.student.name} {obj.student.last_name}",
            'course': obj.student.course,
            'group': obj.student.group,
            'room_name': obj.student.room.name if obj.student.room else None,
            'floor_name': obj.student.floor.name if obj.student.floor else None,
        }



class TaskSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    province_name = serializers.CharField(source='province.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    images = ApartmentImageSerializer(many=True, read_only=True)
    amenities_list = AmenitySerializer(source='amenities', many=True, read_only=True)
    
    class Meta:
        model = Apartment
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    target_user_name = serializers.CharField(source='target_user.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = '__all__'


class UserNotificationSerializer(serializers.ModelSerializer):
    notification_detail = NotificationSerializer(source='notification', read_only=True)
    
    class Meta:
        model = UserNotification
        fields = '__all__'


class ApplicationNotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ApplicationNotification
        fields = '__all__'


class UnifiedNotificationSerializer(serializers.Serializer):
    """Barcha bildirishnomalarni birlashtirib beruvchi serializer"""
    id = serializers.IntegerField()
    type = serializers.CharField()  # 'user' yoki 'application'
    message = serializers.CharField()
    is_read = serializers.BooleanField()
    created_at = serializers.DateTimeField()
    image = serializers.ImageField(required=False, allow_null=True)
    
    def to_representation(self, instance):
        if isinstance(instance, UserNotification):
            return {
                'id': instance.id,
                'type': 'user',
                'message': instance.notification.message if instance.notification else '',
                'is_read': instance.is_read,
                'created_at': instance.received_at,
                'image': instance.notification.image.url if instance.notification and instance.notification.image else None,
            }
        elif isinstance(instance, ApplicationNotification):
            return {
                'id': instance.id,
                'type': 'application',
                'message': instance.message,
                'is_read': instance.is_read,
                'created_at': instance.created_at,
                'image': None,
            }
        return {}


class FloorLeaderSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    floor_info = FloorSerializer(source='floor', read_only=True)

    username   = serializers.CharField(write_only=True, help_text="Sardor username")
    password   = serializers.CharField(write_only=True, help_text="Sardor paroli")
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name  = serializers.CharField(write_only=True, required=False, allow_blank=True)
    phone      = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = FloorLeader
        fields = ['id', 'floor', 'user_info', 'floor_info',
                  'username', 'password', 'first_name', 'last_name', 'phone']
        extra_kwargs = {'user': {'read_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Bu username band")
        return value

    def create(self, validated_data):
        username   = validated_data.pop('username')
        password   = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        last_name  = validated_data.pop('last_name', '')
        phone      = validated_data.pop('phone', None)

        user = User.objects.create_user(
            username=username,
            password=password,
            role='sardor',
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        UserProfile.objects.create(user=user)

        return FloorLeader.objects.create(user=user, **validated_data)


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    session_date = serializers.DateField(source='session.date', read_only=True)
    floor_name = serializers.CharField(source='session.floor.name', read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id', 'session', 'session_date', 'floor_name',
                  'student', 'student_name', 'student_last_name',
                  'status', 'created_at']


class AttendanceSessionSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    leader_name = serializers.CharField(source='leader.user.username', read_only=True)
    records = AttendanceRecordSerializer(many=True, read_only=True)
    date = serializers.DateField(required=False)
    
    class Meta:
        model = AttendanceSession
        fields = '__all__'
    
    def create(self, validated_data):
        if 'date' not in validated_data:
            from datetime import date
            validated_data['date'] = date.today()
        return super().create(validated_data)


class CollectionRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = CollectionRecord
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    leader_name = serializers.CharField(source='leader.user.username', read_only=True)
    records = CollectionRecordSerializer(many=True, read_only=True)
    
    class Meta:
        model = Collection
        fields = '__all__'


class TaskForLeaderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TaskForLeader
        fields = '__all__'


class DutyScheduleSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = DutySchedule
        fields = '__all__'


class GoogleTokenSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Google ID Token yoki Access Token")


class AssignRoomSerializer(serializers.Serializer):
    """Talabaga xona biriktirish uchun serializer"""
    floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    
    def validate(self, data):
        floor = data.get('floor')
        room = data.get('room')
        
        # Xona shu qavatda ekanligini tekshirish
        if room.floor != floor:
            raise serializers.ValidationError({
                "room": f"Bu xona {floor.name} qavatida emas"
            })
        
        # Xonada joy borligini tekshirish (real-time hisoblash)
        current_students = Student.objects.filter(room=room, is_active=True).count()
        if current_students >= (room.capacity or 0):
            raise serializers.ValidationError({
                "room": f"Bu xonada bo'sh joy yo'q. Sig'im: {room.capacity}, Band: {current_students}"
            })
        
        return data
    
    def update(self, instance, validated_data):
        """Student instance ni yangilash"""
        floor = validated_data['floor']
        room = validated_data['room']
        
        # Agar talaba allaqachon xonaga joylashtirilgan bo'lsa
        if instance.is_active and instance.room:
            raise serializers.ValidationError({
                "detail": "Bu talaba allaqachon xonaga joylashtirilgan",
                "current_room": instance.room.name,
                "current_floor": instance.floor.name if instance.floor else None
            })
        
        # Talabaning jinsi va xona/qavat jinsi mos kelishini tekshirish
        student_gender = 'male' if instance.gender == 'Erkak' else 'female'
        
        if floor.gender != student_gender:
            raise serializers.ValidationError({
                "error": f"Talaba jinsi ({instance.gender}) va qavat jinsi ({floor.gender}) mos kelmaydi"
            })
        
        if room.gender != student_gender:
            raise serializers.ValidationError({
                "error": f"Talaba jinsi ({instance.gender}) va xona jinsi ({room.gender}) mos kelmaydi"
            })
        
        # Eski xonani saqlash
        old_room = instance.room
        
        # Yangi xonaga joylashtirish
        instance.floor = floor
        instance.room = room
        instance.is_active = True
        instance.placement_status = 'Joylashdi'
        instance.save()
        
        # Eski xonani yangilash (agar mavjud bo'lsa)
        if old_room:
            old_room.update_occupancy()
        
        # Yangi xonani yangilash
        room.update_occupancy()
        
        # Talabaga bildirishnoma yuborish
        if instance.user:
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Siz {floor.name} qavat, {room.name} xonaga joylashtirilgansiz."
            )
        
        return instance


class RemoveRoomSerializer(serializers.Serializer):
    """Talabani xonadan chiqarish uchun serializer"""
    
    def update(self, instance, validated_data):
        """Student instance dan xonani olib tashlash"""
        
        if not instance.room:
            raise serializers.ValidationError({
                "detail": "Bu talaba hech qaysi xonada emas"
            })
        
        # Xonadan chiqarish
        old_room = instance.room
        old_floor = instance.floor
        
        instance.room = None
        instance.floor = None
        instance.is_active = False
        instance.placement_status = 'Qabul qilindi'
        instance.save()
        
        # Eski xonani yangilash
        old_room.update_occupancy()
        
        # Talabaga bildirishnoma
        if instance.user:
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Siz {old_floor.name} qavat, {old_room.name} xonadan chiqarildingiz."
            )
        
        return instance



class ApplicationApproveSerializer(serializers.Serializer):
    """Arizani tasdiqlash uchun serializer"""
    admin_comment = serializers.CharField(required=False, allow_blank=True, help_text="Admin izohi")
    
    def update(self, instance, validated_data):
        # Agar allaqachon tasdiqlangan bo'lsa
        if instance.status == 'Approved':
            raise serializers.ValidationError({"detail": "Bu ariza allaqachon tasdiqlangan"})
        
        # Arizani tasdiqlash
        instance.status = 'Approved'
        instance.admin_comment = validated_data.get('admin_comment', '')
        instance.save()
        
        # Signal avtomatik Student yaratadi
        return instance


class ApplicationRejectSerializer(serializers.Serializer):
    """Arizani rad etish uchun serializer"""
    admin_comment = serializers.CharField(required=False, allow_blank=True, default='Sabab ko\'rsatilmagan', help_text="Rad etish sababi")
    
    def update(self, instance, validated_data):
        # Agar allaqachon rad etilgan bo'lsa
        if instance.status == 'Rejected':
            raise serializers.ValidationError({"detail": "Bu ariza allaqachon rad etilgan"})
        
        # Arizani rad etish
        instance.status = 'Rejected'
        instance.admin_comment = validated_data.get('admin_comment', 'Sabab ko\'rsatilmagan')
        instance.save()
        
        # Signal avtomatik bildirishnoma yuboradi
        return instance


class ComplaintSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)

    class Meta:
        model = Complaint
        fields = '__all__'
        read_only_fields = ['student', 'dormitory', 'status', 'admin_response', 'created_at', 'updated_at']


class StaffSerializer(serializers.ModelSerializer):
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'id', 'dormitory', 'dormitory_name',
            'name', 'last_name', 'position', 'phone',
            'salary', 'photo', 'file', 'hired_date',
            'is_active', 'created_at',
        ]
        read_only_fields = ['dormitory']


class StaffAttendanceSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    staff_position = serializers.CharField(source='staff.get_position_display', read_only=True)

    class Meta:
        model = StaffAttendance
        fields = '__all__'


class TransferRoomSerializer(serializers.Serializer):
    """Talabani bir xonadan boshqa xonaga o'tkazish (to'la xonadan ham)"""
    new_floor = serializers.PrimaryKeyRelatedField(queryset=Floor.objects.all())
    new_room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    force = serializers.BooleanField(
        default=False,
        help_text="True bo'lsa to'la xonadan ham o'tkazadi"
    )

    def validate(self, data):
        new_floor = data['new_floor']
        new_room = data['new_room']

        if new_room.floor != new_floor:
            raise serializers.ValidationError({
                "new_room": f"Bu xona {new_floor.name} qavatida emas"
            })

        # Xonada joy borligini tekshirish
        current = Student.objects.filter(room=new_room, is_active=True).count()
        if current >= (new_room.capacity or 0):
            if not data.get('force'):
                raise serializers.ValidationError({
                    "new_room": f"Bu xona to'la ({current}/{new_room.capacity}). "
                                f"force=true yuborib majburan o'tkazishingiz mumkin."
                })
        return data

    def update(self, instance, validated_data):
        new_floor = validated_data['new_floor']
        new_room = validated_data['new_room']

        # Jins tekshiruvi
        student_gender = 'male' if instance.gender == 'Erkak' else 'female'
        
        if new_floor.gender != student_gender:
            raise serializers.ValidationError({
                "error": f"Talaba jinsi ({instance.gender}) va qavat jinsi ({new_floor.gender}) mos kelmaydi"
            })
        
        if new_room.gender != student_gender:
            raise serializers.ValidationError({
                "error": f"Talaba jinsi ({instance.gender}) va xona jinsi ({new_room.gender}) mos kelmaydi"
            })

        old_room = instance.room
        old_floor = instance.floor

        instance.floor = new_floor
        instance.room = new_room
        instance.is_active = True
        instance.placement_status = 'Joylashdi'
        instance.save()

        # Eski xonani yangilash
        if old_room:
            old_room.update_occupancy()

        # Yangi xonani yangilash
        new_room.update_occupancy()

        # Bildirishnoma
        if instance.user:
            old_info = f"{old_floor.name} qavat, {old_room.name} xona" if old_room else "eski xona"
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Xonangiz o'zgartirildi: {old_info} → {new_floor.name} qavat, {new_room.name} xona"
            )

        return instance


class AttendanceRecordInputSerializer(serializers.Serializer):
    student_id = serializers.IntegerField(help_text="Talaba ID si")
    status = serializers.ChoiceField(
        choices=[('in', 'Keldi'), ('out', 'Kelmadi')],
        default='in',
        help_text="in = keldi, out = kelmadi"
    )


class AttendanceSessionCreateSerializer(serializers.Serializer):
    """Sardor davomat sessiyasi yaratish - faqat date va records kerak"""
    date = serializers.DateField(
        required=False,
        help_text="Sana (bo'sh qolsa bugungi sana)"
    )
    records = AttendanceRecordInputSerializer(
        many=True,
        required=False,
        help_text="[{student_id: 1, status: 'in'}, ...] Bo'sh qolsa hammasi 'in'"
    )

    def create(self, validated_data):
        from datetime import date as date_cls

        # floor va leader view dan save() orqali keladi
        floor = validated_data.pop('floor')
        leader = validated_data.pop('leader')
        day = validated_data.get('date') or date_cls.today()
        records_data = validated_data.get('records', [])

        session, _ = AttendanceSession.objects.get_or_create(
            date=day,
            floor=floor,
            defaults={'leader': leader}
        )

        if records_data:
            for rec in records_data:
                try:
                    student = Student.objects.get(
                        id=rec['student_id'], is_active=True, floor=floor
                    )
                    AttendanceRecord.objects.update_or_create(
                        session=session,
                        student=student,
                        defaults={'status': rec.get('status', 'in')}
                    )
                except Student.DoesNotExist:
                    pass
        else:
            for student in Student.objects.filter(floor=floor, is_active=True):
                AttendanceRecord.objects.get_or_create(
                    session=session,
                    student=student,
                    defaults={'status': 'in'}
                )

        return session


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Tekshiriladigan username")
