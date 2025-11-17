from rest_framework import generics, status, filters, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import *
from .serializers import *
from .permisssions import *


# ==================== AUTH VIEWS ====================
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi"}, 
            status=status.HTTP_201_CREATED
        )


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


# ==================== USER VIEWS ====================
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['username', 'email']
    filterset_fields = ['role', 'is_active']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


# ==================== USER PROFILE VIEWS ====================
class UserProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserProfile.objects.none()
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserProfile.objects.none()
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)


# ==================== PROVINCE VIEWS ====================
class ProvinceListView(generics.ListCreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [AllowAny]


class ProvinceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [AllowAny]


# ==================== DISTRICT VIEWS ====================
class DistrictListView(generics.ListCreateAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['province']


class DistrictDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]


# ==================== UNIVERSITY VIEWS ====================
class UniversityListView(generics.ListCreateAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]


class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [AllowAny]


# ==================== AMENITY VIEWS ====================
class AmenityListView(generics.ListCreateAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


class AmenityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== DORMITORY VIEWS ====================
class DormitoryListView(generics.ListAPIView):
    serializer_class = DormitorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_fields = ['university', 'is_active']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Dormitory.objects.filter(is_active=True)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'role') and self.request.user.role == 'admin':
            return Dormitory.objects.filter(admin=self.request.user)
        return Dormitory.objects.filter(is_active=True)


class DormitoryCreateView(generics.CreateAPIView):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer
    permission_classes = [IsAdminUser]


class DormitoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dormitory.objects.all()
    serializer_class = DormitorySerializer
    permission_classes = [IsOwnerOrIsAdmin]


# ==================== DORMITORY IMAGE VIEWS ====================
class DormitoryImageListView(generics.ListCreateAPIView):
    queryset = DormitoryImage.objects.all()
    serializer_class = DormitoryImageSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dormitory']


class DormitoryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DormitoryImage.objects.all()
    serializer_class = DormitoryImageSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== RULE VIEWS ====================
class RuleListView(generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dormitory']


class RuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== FLOOR VIEWS ====================
class FloorListView(generics.ListCreateAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != 'admin':
            raise PermissionDenied("Siz yotoqxona admini emassiz !!!")

        try:
            dormitory = Dormitory.objects.get(admin=user)
        except Dormitory.DoesNotExist:
            raise PermissionDenied("Sizga tegishli yotoqxona mavjud emas !!!")

        serializer.save(dormitory=dormitory)

class FloorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== ROOM VIEWS ====================
class RoomListView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'status',]


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== STUDENT VIEWS ====================
class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'last_name', 'passport', 'phone']
    filterset_fields = ['dormitory', 'floor', 'room', 'course', 'gender', 'status']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        elif hasattr(user, 'role') and user.role == 'sardor':
            floor_leader = FloorLeader.objects.filter(user=user).first()
            if floor_leader:
                return Student.objects.filter(floor=floor_leader.floor)
        return Student.objects.filter(user=user)


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        return Student.objects.filter(user=user)


# ==================== APPLICATION VIEWS ====================
class ApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'last_name', 'passport']
    filterset_fields = ['dormitory', 'status']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Application.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Application.objects.filter(dormitory__admin=user)
        return Application.objects.filter(user=user)


class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Application.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Application.objects.filter(dormitory__admin=user)
        return Application.objects.filter(user=user)


class ApplicationApproveView(APIView):
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def post(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            application.status = 'Approved'
            application.save()
            return Response({"message": "Ariza tasdiqlandi"}, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Ariza topilmadi"}, status=status.HTTP_404_NOT_FOUND)


class ApplicationRejectView(APIView):
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def post(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            application.status = 'Rejected'
            application.comment = request.data.get('comment', '')
            application.save()
            return Response({"message": "Ariza rad etildi"}, status=status.HTTP_200_OK)
        except Application.DoesNotExist:
            return Response({"error": "Ariza topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# ==================== PAYMENT VIEWS ====================
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'status', 'method']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Payment.objects.filter(dormitory__admin=user)
        return Payment.objects.none()


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]

    def perform_create(self, serializer):
        student = serializer.validated_data['student']

        try:
            dormitory = student.floor.dormitory
        except AttributeError:
            raise serializers.ValidationError("Studentning floor yoki dormitorysi mavjud emas!")

        serializer.save(dormitory=dormitory)

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Payment.objects.filter(dormitory__admin=user)
        return Payment.objects.none()


# ==================== TASK VIEWS ====================
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()
        return Task.objects.filter(user=self.request.user)


# ==================== APARTMENT VIEWS ====================
class ApartmentListView(generics.ListAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'exact_address']
    filterset_fields = ['province', 'room_type', 'gender', 'is_active']
    
    def get_queryset(self):
        return Apartment.objects.filter(is_active=True)


class ApartmentCreateView(generics.CreateAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ApartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Apartment.objects.filter(is_active=True)
        if self.request.method == 'GET':
            return Apartment.objects.filter(is_active=True)
        return Apartment.objects.filter(user=self.request.user)


# ==================== APARTMENT IMAGE VIEWS ====================
class ApartmentImageListView(generics.ListCreateAPIView):
    queryset = ApartmentImage.objects.all()
    serializer_class = ApartmentImageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['apartment']


class ApartmentImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApartmentImage.objects.all()
    serializer_class = ApartmentImageSerializer
    permission_classes = [IsAuthenticated]


# ==================== NOTIFICATION VIEWS ====================
class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.filter(is_active=True)
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['target_type', 'is_active']


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== USER NOTIFICATION VIEWS ====================
class UserNotificationListView(generics.ListAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserNotification.objects.none()
        return UserNotification.objects.filter(user=self.request.user)


class UserNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserNotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserNotification.objects.none()
        return UserNotification.objects.filter(user=self.request.user)


class UserNotificationMarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notification = UserNotification.objects.get(pk=pk, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "O'qilgan deb belgilandi"}, status=status.HTTP_200_OK)
        except UserNotification.DoesNotExist:
            return Response({"error": "Bildirishnoma topilmadi"}, status=status.HTTP_404_NOT_FOUND)


# ==================== APPLICATION NOTIFICATION VIEWS ====================
class ApplicationNotificationListView(generics.ListAPIView):
    serializer_class = ApplicationNotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ApplicationNotification.objects.none()
        return ApplicationNotification.objects.filter(user=self.request.user)


class ApplicationNotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationNotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ApplicationNotification.objects.none()
        return ApplicationNotification.objects.filter(user=self.request.user)


# ==================== FLOOR LEADER VIEWS ====================
class FloorLeaderListView(generics.ListCreateAPIView):
    queryset = FloorLeader.objects.all()
    serializer_class = FloorLeaderSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor']


class FloorLeaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FloorLeader.objects.all()
    serializer_class = FloorLeaderSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


# ==================== ATTENDANCE SESSION VIEWS ====================
class AttendanceSessionListView(generics.ListAPIView):
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'date']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AttendanceSession.objects.none()
        user = self.request.user
        if user.is_superuser:
            return AttendanceSession.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return AttendanceSession.objects.filter(floor__dormitory__admin=user)
        elif hasattr(user, 'role') and user.role == 'sardor':
            floor_leader = FloorLeader.objects.filter(user=user).first()
            if floor_leader:
                return AttendanceSession.objects.filter(floor=floor_leader.floor)
        return AttendanceSession.objects.none()


class AttendanceSessionCreateView(generics.CreateAPIView):
    queryset = AttendanceSession.objects.all()
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsFloorLeader]


class AttendanceSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AttendanceSessionSerializer
    permission_classes = [IsFloorLeader]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return AttendanceSession.objects.none()
        user = self.request.user
        if user.is_superuser:
            return AttendanceSession.objects.all()
        elif hasattr(user, 'role') and user.role == 'sardor':
            floor_leader = FloorLeader.objects.filter(user=user).first()
            if floor_leader:
                return AttendanceSession.objects.filter(floor=floor_leader.floor)
        return AttendanceSession.objects.none()


# ==================== ATTENDANCE RECORD VIEWS ====================
class AttendanceRecordListView(generics.ListCreateAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsFloorLeader]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['session', 'student', 'status']


class AttendanceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsFloorLeader]


# ==================== COLLECTION VIEWS ====================
class CollectionListView(generics.ListAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Collection.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Collection.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Collection.objects.filter(floor__dormitory__admin=user)
        elif hasattr(user, 'role') and user.role == 'sardor':
            floor_leader = FloorLeader.objects.filter(user=user).first()
            if floor_leader:
                return Collection.objects.filter(floor=floor_leader.floor)
        return Collection.objects.none()


class CollectionCreateView(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsFloorLeader]


class CollectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CollectionSerializer
    permission_classes = [IsFloorLeader]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Collection.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Collection.objects.all()
        elif hasattr(user, 'role') and user.role == 'sardor':
            floor_leader = FloorLeader.objects.filter(user=user).first()
            if floor_leader:
                return Collection.objects.filter(floor=floor_leader.floor)
        return Collection.objects.none()


# ==================== COLLECTION RECORD VIEWS ====================
class CollectionRecordListView(generics.ListCreateAPIView):
    queryset = CollectionRecord.objects.all()
    serializer_class = CollectionRecordSerializer
    permission_classes = [IsFloorLeader]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['collection', 'student', 'status']


class CollectionRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CollectionRecord.objects.all()
    serializer_class = CollectionRecordSerializer
    permission_classes = [IsFloorLeader]


# ==================== TASK FOR LEADER VIEWS ====================
class TaskForLeaderListView(generics.ListAPIView):
    serializer_class = TaskForLeaderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TaskForLeader.objects.none()
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'sardor':
            return TaskForLeader.objects.filter(user=user)
        elif hasattr(user, 'role') and user.role == 'admin':
            floor_leaders = FloorLeader.objects.filter(floor__dormitory__admin=user)
            return TaskForLeader.objects.filter(user__in=[fl.user for fl in floor_leaders])
        return TaskForLeader.objects.none()


class TaskForLeaderCreateView(generics.CreateAPIView):
    queryset = TaskForLeader.objects.all()
    serializer_class = TaskForLeaderSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


class TaskForLeaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskForLeaderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return TaskForLeader.objects.none()
        user = self.request.user
        if hasattr(user, 'role') and user.role == 'sardor':
            return TaskForLeader.objects.filter(user=user)
        elif hasattr(user, 'role') and user.role == 'admin':
            floor_leaders = FloorLeader.objects.filter(floor__dormitory__admin=user)
            return TaskForLeader.objects.filter(user__in=[fl.user for fl in floor_leaders])
        return TaskForLeader.objects.none()


# ==================== DUTY SCHEDULE VIEWS ====================
class DutyScheduleListView(generics.ListCreateAPIView):
    queryset = DutySchedule.objects.all()
    serializer_class = DutyScheduleSerializer
    permission_classes = [IsFloorLeader]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'room', 'date']


class DutyScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DutySchedule.objects.all()
    serializer_class = DutyScheduleSerializer
    permission_classes = [IsFloorLeader]
