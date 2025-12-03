from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'email']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birth_date']
    search_fields = ['user__username', 'phone']

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'province']
    list_filter = ['province']
    search_fields = ['name']

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']
    search_fields = ['name']

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'admin', 'month_price', 'is_active']
    list_filter = ['university', 'is_active']
    search_fields = ['name', 'address']
    filter_horizontal = ['amenities']

@admin.register(DormitoryImage)
class DormitoryImageAdmin(admin.ModelAdmin):
    list_display = ['dormitory', 'image']

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['dormitory', 'rule']
    list_filter = ['dormitory']

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['name', 'dormitory', 'gender']
    list_filter = ['dormitory', 'gender']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor', 'capacity', 'current_occupancy', 'gender', 'status']
    list_filter = ['floor', 'gender', 'status']
    search_fields = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'passport', 'dormitory', 'room', 'course', 'status']
    list_filter = ['dormitory', 'course', 'gender', 'status', 'placement_status']
    search_fields = ['name', 'last_name', 'passport', 'phone']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'dormitory', 'status', 'created_at']
    list_filter = ['dormitory', 'status', 'created_at']
    search_fields = ['name', 'last_name', 'passport', 'phone']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'dormitory', 'amount', 'paid_date', 'method', 'status']
    list_filter = ['dormitory', 'method', 'status', 'paid_date']
    search_fields = ['student__name', 'student__passport']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'status', 'created_at', 'reminder_date']
    list_filter = ['status', 'created_at']
    search_fields = ['description', 'user__username']

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'province', 'room_type', 'monthly_price', 'gender', 'is_active']
    list_filter = ['province', 'room_type', 'gender', 'is_active']
    search_fields = ['title', 'exact_address']
    filter_horizontal = ['amenities']

@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'uploaded_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'target_type', 'target_user', 'created_at', 'is_active']
    list_filter = ['target_type', 'is_active', 'created_at']

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification', 'is_read', 'received_at']
    list_filter = ['is_read', 'received_at']
    search_fields = ['user__username']

@admin.register(ApplicationNotification)
class ApplicationNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']

@admin.register(FloorLeader)
class FloorLeaderAdmin(admin.ModelAdmin):
    list_display = ['user', 'floor']
    search_fields = ['user__username']

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ['date', 'floor', 'leader', 'created_at']
    list_filter = ['date', 'floor']

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'status', 'created_at']
    list_filter = ['status', 'session__date']
    search_fields = ['student__name']

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'floor', 'deadline', 'created_at']
    list_filter = ['floor', 'created_at']
    search_fields = ['title']

@admin.register(CollectionRecord)
class CollectionRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'collection', 'status']
    list_filter = ['status', 'collection']
    search_fields = ['student__name']

@admin.register(TaskForLeader)
class TaskForLeaderAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['description', 'user__username']

@admin.register(DutySchedule)
class DutyScheduleAdmin(admin.ModelAdmin):
    list_display = ['floor', 'room', 'date', 'created_at']
    list_filter = ['floor', 'date']
