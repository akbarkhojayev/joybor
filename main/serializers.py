from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'email']
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

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',          # <-- MUHIM!
            'image',
            'bio',
            'phone',
            'birth_date',
            'address',
            'telegram',
        ]

class UserMeSerializer(serializers.ModelSerializer):
    """Joriy foydalanuvchi profili - ko'rish va tahrirlash"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name', required=False, allow_blank=True)
    last_name = serializers.CharField(source='user.last_name', required=False, allow_blank=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'image',
            'bio',
            'phone',
            'birth_date',
            'address',
            'telegram',
        ]
    
    def update(self, instance, validated_data):
        # User ma'lumotlarini yangilash
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        if 'email' in user_data:
            user.email = user_data['email']
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        user.save()
        
        # UserProfile ma'lumotlarini yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'role', 'first_name', 'last_name']

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

class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


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


class RoomSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['current_occupancy', 'status']



class DormitorySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    images = DormitoryImageSerializer(many=True, read_only=True)
    amenities_list = AmenitySerializer(source='amenities', many=True, read_only=True)
    
    class Meta:
        model = Dormitory
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'


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
            return {
                'id': obj.room.id,
                'name': obj.room.name,
                'capacity': obj.room.capacity,
                'current_occupancy': obj.room.current_occupancy,
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


class ApplicationSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('status','admin_comment')

class ApplicationAdminUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'comment']

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['student','amount', 'paid_date','valid_until','method','status','comment']


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
    
    class Meta:
        model = FloorLeader
        fields = '__all__'


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    
    class Meta:
        model = AttendanceRecord
        fields = '__all__'


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
        
        # Xonada joy borligini tekshirish
        if room.current_occupancy >= room.capacity:
            raise serializers.ValidationError({
                "room": "Bu xonada bo'sh joy yo'q"
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
        
        # Talabaning jinsi va xona jinsi mos kelishini tekshirish
        student_gender = 'male' if instance.gender == 'Erkak' else 'female'
        if room.gender != student_gender:
            raise serializers.ValidationError({
                "error": f"Talaba jinsi ({instance.gender}) va xona jinsi ({room.gender}) mos kelmaydi"
            })
        
        # Eski xonadan o'chirish (agar mavjud bo'lsa)
        if instance.room:
            old_room = instance.room
            old_room.current_occupancy -= 1
            if old_room.current_occupancy == 0:
                old_room.status = 'AVAILABLE'
            elif old_room.current_occupancy < old_room.capacity:
                old_room.status = 'PARTIALLY_OCCUPIED'
            old_room.save()
        
        # Yangi xonaga joylashtirish
        instance.floor = floor
        instance.room = room
        instance.is_active = True
        instance.placement_status = 'Joylashdi'
        instance.save()
        
        # Xona occupancy ni yangilash
        room.current_occupancy += 1
        if room.current_occupancy >= room.capacity:
            room.status = 'FULLY_OCCUPIED'
        else:
            room.status = 'PARTIALLY_OCCUPIED'
        room.save()
        
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
        
        # Xona occupancy ni yangilash
        old_room.current_occupancy -= 1
        if old_room.current_occupancy == 0:
            old_room.status = 'AVAILABLE'
        elif old_room.current_occupancy < old_room.capacity:
            old_room.status = 'PARTIALLY_OCCUPIED'
        old_room.save()
        
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
