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
        fields = '__all__'


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

    class Meta:
        model = Floor
        fields = ['id', 'name', 'gender']

class RoomSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'


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


class ApplicationSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    province_name = serializers.CharField(source='province.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    
    class Meta:
        model = Application
        fields = '__all__'


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
