from rest_framework import generics, status, filters, mixins
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import *
from .serializers import *
from .permisssions import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import PermissionDenied


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


class CurrentUserView(generics.RetrieveUpdateAPIView):
    """Joriy foydalanuvchi ma'lumotlarini ko'rish va tahrirlash"""
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        # SUPERUSER ⇒ 404 bo'lmaydi
        if user.is_superuser:
            # Agar profil mavjud bo'lsa — qaytaramiz
            try:
                return user.profile
            except UserProfile.DoesNotExist:
                # Profil yo'q bo'lsa yaratamiz
                return UserProfile.objects.create(user=user)

        # ODDIY USER ⇒ Profil bo'lmasa yaratamiz
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            return UserProfile.objects.create(user=user)


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

class DormitoryImageListView(generics.ListCreateAPIView):
    serializer_class = DormitoryImageSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user

        # Superuser hammasini ko‘ra oladi
        if user.is_superuser:
            return DormitoryImage.objects.all()

        # Admin faqat o‘z dormitory rasmlarini
        return DormitoryImage.objects.filter(
            dormitory__admin=user
        )

    def perform_create(self, serializer):
        user = self.request.user

        # user admin bo‘lgan dormitoryni topamiz
        dormitory = Dormitory.objects.filter(admin=user).first()
        if not dormitory:
            raise PermissionDenied(
                "Sizga tegishli dormitory topilmadi"
            )

        serializer.save(dormitory=dormitory)


class DormitoryImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DormitoryImageSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return DormitoryImage.objects.all()

        return DormitoryImage.objects.filter(
            dormitory__admin=user
        )



# ==================== RULE VIEWS ====================
class RuleListView(generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dormitory']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rule.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Rule.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Rule.objects.filter(dormitory__admin=user)
        # Barcha foydalanuvchilar dormitory qoidalarini ko'rishi mumkin
        return Rule.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'role') or user.role != 'admin':
            raise PermissionDenied("Faqat admin qoida qo'sha oladi")
        
        try:
            dormitory = Dormitory.objects.get(admin=user)
        except Dormitory.DoesNotExist:
            raise PermissionDenied("Sizga tegishli yotoqxona topilmadi")
        
        serializer.save(dormitory=dormitory)



class RuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RuleSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rule.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Rule.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining qoidalarini ko'radi
            return Rule.objects.filter(dormitory__admin=user)
        return Rule.objects.none()


# ==================== FLOOR VIEWS ====================
class FloorListView(generics.ListCreateAPIView):
    serializer_class = FloorSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['gender']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Floor.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Floor.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining qavatlarini ko'radi
            return Floor.objects.filter(dormitory__admin=user)
        return Floor.objects.none()

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
    serializer_class = FloorSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Floor.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Floor.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining qavatlarini ko'radi
            return Floor.objects.filter(dormitory__admin=user)
        return Floor.objects.none()


# ==================== ROOM VIEWS ====================
class RoomListView(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor', 'status', 'gender']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Room.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining xonalarini ko'radi
            return Room.objects.filter(floor__dormitory__admin=user)
        return Room.objects.none()


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Room.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return Room.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining xonalarini ko'radi
            return Room.objects.filter(floor__dormitory__admin=user)
        return Room.objects.none()


# ==================== STUDENT VIEWS ====================
class StudentListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]  # Hamma authenticated user ko'ra oladi
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'last_name', 'passport', 'phone']
    filterset_fields = ['dormitory', 'floor', 'room', 'course', 'gender', 'status']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        
        # Superuser - barcha talabalarni ko'radi
        if user.is_superuser:
            return Student.objects.all()
        
        # Admin - o'z yotoqxonasidagi talabalarni ko'radi
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        
        # Sardor (Floor Leader) - faqat o'z qavatidagi talabalarni ko'radi
        elif hasattr(user, 'role') and user.role == 'sardor':
            try:
                floor_leader = FloorLeader.objects.get(user=user)
                # Faqat o'z qavatidagi talabalar
                return Student.objects.filter(
                    floor=floor_leader.floor,
                    dormitory=floor_leader.floor.dormitory,
                    is_active=True  # Faqat faol talabalar
                )
            except FloorLeader.DoesNotExist:
                return Student.objects.none()
        
        # Student - faqat o'zini ko'radi
        return Student.objects.filter(user=user)


class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]  # Hamma authenticated user ko'ra oladi

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        
        # Superuser - barcha talabalarni ko'radi
        if user.is_superuser:
            return Student.objects.all()
        
        # Admin - o'z yotoqxonasidagi talabalarni ko'radi va tahrirlashi mumkin
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        
        # Sardor (Floor Leader) - faqat o'z qavatidagi talabalarni ko'radi (faqat o'qish)
        elif hasattr(user, 'role') and user.role == 'sardor':
            try:
                floor_leader = FloorLeader.objects.get(user=user)
                return Student.objects.filter(
                    floor=floor_leader.floor,
                    dormitory=floor_leader.floor.dormitory,
                    is_active=True
                )
            except FloorLeader.DoesNotExist:
                return Student.objects.none()
        
        # Student - faqat o'zini ko'radi
        return Student.objects.filter(user=user)
    
    def update(self, request, *args, **kwargs):
        """Faqat admin tahrirlashi mumkin"""
        user = request.user
        if not user.is_superuser and (not hasattr(user, 'role') or user.role != 'admin'):
            return Response(
                {"error": "Faqat admin talaba ma'lumotlarini tahrirlashi mumkin"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Faqat admin o'chirishi mumkin"""
        user = request.user
        if not user.is_superuser and (not hasattr(user, 'role') or user.role != 'admin'):
            return Response(
                {"error": "Faqat admin talabani o'chirishi mumkin"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


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
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        # Agar foydalanuvchi tizimga kirgan bo'lsa, user ni biriktirish
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


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

class ApplicationApproveView(generics.UpdateAPIView):
    """Arizani tasdiqlash va avtomatik Student yaratish"""
    queryset = Application.objects.all()
    serializer_class = ApplicationApproveSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Application.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Application.objects.filter(dormitory__admin=user)
        return Application.objects.none()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "message": "Ariza tasdiqlandi va talaba ro'yxatga olindi",
            "admin_comment": instance.admin_comment,
            "application": ApplicationSerializer(instance).data
        }, status=status.HTTP_200_OK)


class ApplicationRejectView(generics.UpdateAPIView):
    """Arizani rad etish"""
    queryset = Application.objects.all()
    serializer_class = ApplicationRejectSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Application.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Application.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Application.objects.filter(dormitory__admin=user)
        return Application.objects.none()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "message": "Ariza rad etildi",
            "admin_comment": instance.admin_comment,
            "application": ApplicationSerializer(instance).data
        }, status=status.HTTP_200_OK)

# ==================== PAYMENT VIEWS ====================
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'status', 'method', 'dormitory']
    ordering_fields = ['paid_date', 'amount', 'valid_until']
    ordering = ['-paid_date']  # Eng yangi to'lovlar birinchi

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Payment.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Payment.objects.select_related('student', 'dormitory').all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Payment.objects.select_related('student', 'dormitory').filter(dormitory__admin=user)
        return Payment.objects.none()

class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        
        # Dormitory ni aniqlash
        dormitory = None
        
        # 1. Agar student floor ga biriktirilgan bo'lsa
        if student.floor and student.floor.dormitory:
            dormitory = student.floor.dormitory
        # 2. Agar student dormitory ga biriktirilgan bo'lsa (lekin floor yo'q)
        elif student.dormitory:
            dormitory = student.dormitory
        # 3. Agar admin o'z yotoqxonasiga to'lov qo'shayotgan bo'lsa
        elif hasattr(self.request.user, 'role') and self.request.user.role == 'admin':
            dormitory = Dormitory.objects.filter(admin=self.request.user).first()
        
        if not dormitory:
            raise serializers.ValidationError({
                "error": "Talaba hech qaysi yotoqxonaga biriktirilmagan. Avval talabani yotoqxonaga biriktiring."
            })
        
        # To'lovni saqlash
        payment = serializer.save(dormitory=dormitory)
        
        # Talabaga bildirishnoma yuborish
        if student.user and payment.status == 'APPROVED':
            ApplicationNotification.objects.create(
                user=student.user,
                message=f"To'lovingiz qabul qilindi. Summa: {payment.amount} so'm. Amal qilish muddati: {payment.valid_until or 'Korsatilmagan'}"
            )

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
    
    def perform_update(self, serializer):
        """To'lov yangilanganda talabaga bildirishnoma yuborish"""
        old_status = self.get_object().status
        payment = serializer.save()
        
        # Agar status APPROVED ga o'zgartirilgan bo'lsa
        if old_status != 'APPROVED' and payment.status == 'APPROVED':
            if payment.student.user:
                ApplicationNotification.objects.create(
                    user=payment.student.user,
                    message=f"To'lovingiz tasdiqlandi. Summa: {payment.amount} so'm. Amal qilish muddati: {payment.valid_until or 'Ko\'rsatilmagan'}"
                )
        
        # Agar status CANCELLED ga o'zgartirilgan bo'lsa
        elif old_status != 'CANCELLED' and payment.status == 'CANCELLED':
            if payment.student.user:
                ApplicationNotification.objects.create(
                    user=payment.student.user,
                    message=f"To'lovingiz bekor qilindi. Summa: {payment.amount} so'm. Sabab: {payment.comment or 'Ko\'rsatilmagan'}"
                )


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

# ==================== FLOOR LEADER VIEWS ====================
class FloorLeaderListView(generics.ListCreateAPIView):
    serializer_class = FloorLeaderSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FloorLeader.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return FloorLeader.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining qavat sardorlarini ko'radi
            return FloorLeader.objects.filter(floor__dormitory__admin=user)
        return FloorLeader.objects.none()


class FloorLeaderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FloorLeaderSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return FloorLeader.objects.none()
        
        user = self.request.user
        if user.is_superuser:
            return FloorLeader.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            # Admin faqat o'z yotoqxonasining qavat sardorlarini ko'radi
            return FloorLeader.objects.filter(floor__dormitory__admin=user)
        return FloorLeader.objects.none()


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


# ==================== STUDENT DASHBOARD VIEWS ====================
class StudentDashboardView(APIView):
    """Talaba uchun to'liq dashboard ma'lumotlari"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            student = Student.objects.select_related(
                'user', 'dormitory', 'floor', 'room', 'province', 'district'
            ).get(user=request.user)
            
            serializer = StudentDashboardSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response(
                {"error": "Siz hali talaba sifatida ro'yxatdan o'tmagansiz"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class StudentPaymentsView(generics.ListAPIView):
    """Talabaning barcha to'lovlari"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'method']
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return Payment.objects.filter(student=student).order_by('-paid_date')
        except Student.DoesNotExist:
            return Payment.objects.none()


class StudentRoommatesView(generics.ListAPIView):
    """Talabaning xonadoshlari"""
    serializer_class = RoommateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            if student.room:
                return Student.objects.filter(room=student.room).exclude(id=student.id)
            return Student.objects.none()
        except Student.DoesNotExist:
            return Student.objects.none()


class StudentAttendanceView(generics.ListAPIView):
    """Talabaning davomat ma'lumotlari"""
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'session__date']
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return AttendanceRecord.objects.filter(student=student).order_by('-created_at')
        except Student.DoesNotExist:
            return AttendanceRecord.objects.none()


class StudentCollectionsView(generics.ListAPIView):
    """Talabaning yig'im ma'lumotlari"""
    serializer_class = CollectionRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'collection']
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return CollectionRecord.objects.filter(student=student).select_related('collection')
        except Student.DoesNotExist:
            return CollectionRecord.objects.none()


class NotificationsView(APIView):
    """Barcha bildirishnomalar - bitta unified endpoint (UserNotification + ApplicationNotification)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if getattr(self, 'swagger_fake_view', False):
            return Response([])
        
        # UserNotification larni olish
        user_notifications = UserNotification.objects.filter(
            user=request.user
        ).select_related('notification').order_by('-received_at')
        
        # ApplicationNotification larni olish
        app_notifications = ApplicationNotification.objects.filter(
            user=request.user
        ).order_by('-created_at')
        
        # Ikkalasini birlashtirib, vaqt bo'yicha saralash
        all_notifications = list(user_notifications) + list(app_notifications)
        all_notifications.sort(
            key=lambda x: x.received_at if isinstance(x, UserNotification) else x.created_at,
            reverse=True
        )
        
        # Filter by is_read if provided
        is_read_filter = request.query_params.get('is_read')
        if is_read_filter is not None:
            is_read_bool = is_read_filter.lower() in ['true', '1', 'yes']
            all_notifications = [n for n in all_notifications if n.is_read == is_read_bool]
        
        # Pagination
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        
        page = paginator.paginate_queryset(all_notifications, request)
        if page is not None:
            serializer = UnifiedNotificationSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = UnifiedNotificationSerializer(all_notifications, many=True)
        return Response(serializer.data)



class MarkNotificationAsReadView(APIView):
    """Bildirishnomani o'qilgan deb belgilash (har ikki tur uchun)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        notification_type = request.data.get('type')  # 'user' yoki 'application'
        notification_id = request.data.get('id')
        
        if not notification_type or not notification_id:
            return Response(
                {"error": "type va id majburiy"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if notification_type == 'user':
                notification = UserNotification.objects.get(
                    id=notification_id,
                    user=request.user
                )
                notification.is_read = True
                notification.save()
                return Response(
                    {"message": "Bildirishnoma o'qilgan deb belgilandi"},
                    status=status.HTTP_200_OK
                )
            
            elif notification_type == 'application':
                notification = ApplicationNotification.objects.get(
                    id=notification_id,
                    user=request.user
                )
                notification.is_read = True
                notification.save()
                return Response(
                    {"message": "Bildirishnoma o'qilgan deb belgilandi"},
                    status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {"error": "Noto'g'ri type. 'user' yoki 'application' bo'lishi kerak"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except (UserNotification.DoesNotExist, ApplicationNotification.DoesNotExist):
            return Response(
                {"error": "Bildirishnoma topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )


class MarkAllNotificationsAsReadView(APIView):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # UserNotification larni yangilash
        user_count = UserNotification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        # ApplicationNotification larni yangilash
        app_count = ApplicationNotification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        
        total = user_count + app_count
        
        return Response(
            {"message": f"{total} ta bildirishnoma o'qilgan deb belgilandi"},
            status=status.HTTP_200_OK
        )


class UnreadNotificationCountView(APIView):
    """O'qilmagan bildirishnomalar soni"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_count = UserNotification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        app_count = ApplicationNotification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
        
        return Response({
            "unread_count": user_count + app_count,
            "user_notifications": user_count,
            "application_notifications": app_count
        })


# ==================== ADMIN NOTIFICATION MANAGEMENT ====================
class NotificationCreateView(generics.CreateAPIView):
    """Admin tomonidan bildirishnoma yaratish"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]


class NotificationListView(generics.ListAPIView):
    """Admin tomonidan yaratilgan bildirishnomalar ro'yxati"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['target_type', 'is_active']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.all().order_by('-created_at')


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin tomonidan yaratilgan bildirishnomani ko'rish/tahrirlash/o'chirish"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    parser_classes = [MultiPartParser, FormParser, JSONParser]



class AssignRoomToStudentView(generics.UpdateAPIView):
    """Talabaga qavat va xona biriktirish"""
    queryset = Student.objects.all()
    serializer_class = AssignRoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        return Student.objects.none()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "message": "Talaba muvaffaqiyatli xonaga joylashtirildi",
            "student": {
                "id": instance.id,
                "name": f"{instance.name} {instance.last_name}",
                "floor": instance.floor.name if instance.floor else None,
                "room": instance.room.name if instance.room else None,
                "is_active": instance.is_active,
                "placement_status": instance.placement_status
            }
        }, status=status.HTTP_200_OK)


class RemoveStudentFromRoomView(generics.UpdateAPIView):
    """Talabani xonadan chiqarish"""
    queryset = Student.objects.all()
    serializer_class = RemoveRoomSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        user = self.request.user
        if user.is_superuser:
            return Student.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            return Student.objects.filter(dormitory__admin=user)
        return Student.objects.none()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "message": "Talaba xonadan chiqarildi",
            "student": {
                "id": instance.id,
                "name": f"{instance.name} {instance.last_name}",
                "is_active": instance.is_active,
                "placement_status": instance.placement_status
            }
        }, status=status.HTTP_200_OK)


class UnassignedStudentsView(generics.ListAPIView):
    """Xonaga joylashtirilmagan talabalar ro'yxati"""
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrDormitoryAdmin]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'last_name', 'passport']
    filterset_fields = ['dormitory', 'gender', 'course']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Student.objects.none()
        
        user = self.request.user
        queryset = Student.objects.filter(is_active=False, room__isnull=True)
        
        if user.is_superuser:
            return queryset
        elif hasattr(user, 'role') and user.role == 'admin':
            return queryset.filter(dormitory__admin=user)
        
        return Student.objects.none()



# ==================== ADMIN DASHBOARD STATISTICS ====================
class AdminDashboardStatsView(APIView):
    """Admin uchun to'liq statistika - bitta endpoint"""
    permission_classes = [IsAdminOrDormitoryAdmin]
    
    def get(self, request):
        user = request.user
        
        # Admin o'z yotoqxonasi statistikasini ko'radi
        if user.is_superuser:
            students = Student.objects.all()
            rooms = Room.objects.all()
            payments = Payment.objects.all()
            applications = Application.objects.all()
        elif hasattr(user, 'role') and user.role == 'admin':
            dormitory = Dormitory.objects.filter(admin=user).first()
            if not dormitory:
                return Response(
                    {"error": "Sizga biriktirilgan yotoqxona topilmadi"},
                    status=status.HTTP_404_NOT_FOUND
                )
            students = Student.objects.filter(dormitory=dormitory)
            rooms = Room.objects.filter(floor__dormitory=dormitory)
            payments = Payment.objects.filter(dormitory=dormitory)
            applications = Application.objects.filter(dormitory=dormitory)
        else:
            return Response(
                {"error": "Ruxsat yo'q"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Talabalar statistikasi
        total_students = students.count()
        male_students = students.filter(gender='Erkak').count()
        female_students = students.filter(gender='Ayol').count()
        active_students = students.filter(is_active=True).count()
        inactive_students = students.filter(is_active=False).count()
        
        # Bo'sh joylar statistikasi (Django ORM aggregate ishlatish)
        from django.db.models import Sum
        
        total_rooms = rooms.count()
        total_capacity = rooms.aggregate(Sum('capacity'))['capacity__sum'] or 0
        total_occupied = rooms.aggregate(Sum('current_occupancy'))['current_occupancy__sum'] or 0
        total_free = total_capacity - total_occupied
        
        male_rooms = rooms.filter(gender='male')
        male_capacity = male_rooms.aggregate(Sum('capacity'))['capacity__sum'] or 0
        male_occupied = male_rooms.aggregate(Sum('current_occupancy'))['current_occupancy__sum'] or 0
        male_free = male_capacity - male_occupied
        
        female_rooms = rooms.filter(gender='female')
        female_capacity = female_rooms.aggregate(Sum('capacity'))['capacity__sum'] or 0
        female_occupied = female_rooms.aggregate(Sum('current_occupancy'))['current_occupancy__sum'] or 0
        female_free = female_capacity - female_occupied
        
        # Xonalar status bo'yicha
        available_rooms = rooms.filter(status='AVAILABLE').count()
        partially_occupied_rooms = rooms.filter(status='PARTIALLY_OCCUPIED').count()
        fully_occupied_rooms = rooms.filter(status='FULLY_OCCUPIED').count()
        
        # Occupancy rate (band bo'lish foizi)
        total_occupancy_rate = round((total_occupied / total_capacity * 100) if total_capacity > 0 else 0, 1)
        male_occupancy_rate = round((male_occupied / male_capacity * 100) if male_capacity > 0 else 0, 1)
        female_occupancy_rate = round((female_occupied / female_capacity * 100) if female_capacity > 0 else 0, 1)
        
        # To'lovlar statistikasi
        from django.db.models import Sum
        
        total_payments = payments.count()
        approved_payments = payments.filter(status='APPROVED').count()
        cancelled_payments = payments.filter(status='CANCELLED').count()
        
        # To'lov summasi
        total_amount = payments.filter(status='APPROVED').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Qarzdorlar (hech to'lov qilmagan yoki oxirgi to'lovi 30 kundan ko'p bo'lgan)
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        students_with_recent_payment = payments.filter(
            status='APPROVED',
            paid_date__gte=thirty_days_ago
        ).values_list('student_id', flat=True).distinct()
        
        debtors_count = active_students - len(set(students_with_recent_payment))
        paid_students_count = len(set(students_with_recent_payment))
        
        # Arizalar statistikasi
        total_applications = applications.count()
        pending_applications = applications.filter(status='Pending').count()
        approved_applications = applications.filter(status='Approved').count()
        rejected_applications = applications.filter(status='Rejected').count()
        cancelled_applications = applications.filter(status='Cancelled').count()
        
        # Kurs bo'yicha talabalar
        students_by_course = {}
        for course in ['1-kurs', '2-kurs', '3-kurs', '4-kurs', '5-kurs']:
            students_by_course[course] = students.filter(course=course).count()
        
        return Response({
            "students": {
                "total": total_students,
                "male": male_students,
                "female": female_students,
                "active": active_students,
                "inactive": inactive_students,
                "by_course": students_by_course
            },
            "rooms": {
                "total": {
                    "rooms": total_rooms,
                    "capacity": total_capacity,
                    "occupied": total_occupied,
                    "free": total_free,
                    "occupancy_rate": total_occupancy_rate
                },
                "male": {
                    "rooms": male_rooms.count(),
                    "capacity": male_capacity,
                    "occupied": male_occupied,
                    "free": male_free,
                    "occupancy_rate": male_occupancy_rate
                },
                "female": {
                    "rooms": female_rooms.count(),
                    "capacity": female_capacity,
                    "occupied": female_occupied,
                    "free": female_free,
                    "occupancy_rate": female_occupancy_rate
                },
                "by_status": {
                    "available": available_rooms,
                    "partially_occupied": partially_occupied_rooms,
                    "fully_occupied": fully_occupied_rooms
                }
            },
            "payments": {
                "total": total_payments,
                "approved": approved_payments,
                "cancelled": cancelled_payments,
                "total_amount": total_amount,
                "paid_students": paid_students_count,
                "debtors": debtors_count
            },
            "applications": {
                "total": total_applications,
                "pending": pending_applications,
                "approved": approved_applications,
                "rejected": rejected_applications,
                "cancelled": cancelled_applications
            }
        }, status=status.HTTP_200_OK)



class MyDormitoryView(generics.RetrieveUpdateAPIView):
    """Admin o'z yotoqxonasini ko'rish va tahrirlash"""
    serializer_class = DormitorySerializer
    permission_classes = [IsDormitoryAdmin]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        
        user = self.request.user
        
        # Superuser barcha yotoqxonalarni ko'radi (birinchisini)
        if user.is_superuser:
            dormitory = Dormitory.objects.first()
            if not dormitory:
                raise NotFound("Hech qanday yotoqxona topilmadi")
            return dormitory
        
        # Admin o'z yotoqxonasini ko'radi
        try:
            return Dormitory.objects.get(admin=user)
        except Dormitory.DoesNotExist:
            raise NotFound("Sizga biriktirilgan yotoqxona topilmadi")


class MyDormitoriesListView(generics.ListAPIView):
    """Admin o'z yotoqxonalari ro'yxati (agar bir nechta bo'lsa)"""
    serializer_class = DormitorySerializer
    permission_classes = [IsDormitoryAdmin]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
    filterset_fields = ['is_active']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Dormitory.objects.none()
        
        user = self.request.user
        
        # Superuser barcha yotoqxonalarni ko'radi
        if user.is_superuser:
            return Dormitory.objects.all()
        
        # Admin o'z yotoqxonalarini ko'radi
        return Dormitory.objects.filter(admin=user)


class StudentApplicationView(generics.RetrieveAPIView):
    """Talabaning o'z arizasini ko'rish"""
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        try:
            return Application.objects.get(user=self.request.user)
        except Application.DoesNotExist:
            raise NotFound("Sizning arizangiz topilmadi")


class GeneralStatsView(APIView):
    """Umumiy statistika - yotoqxonalar, foydalanuvchilar, universitetlar soni"""
    permission_classes = [AllowAny]  # Hamma ko'ra oladi

    def get(self, request):
        # Yotoqxonalar statistikasi
        total_dormitories = Dormitory.objects.filter(is_active=True).count()
        active_dormitories = Dormitory.objects.filter(is_active=True).count()

        # Foydalanuvchilar statistikasi
        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        students_count = User.objects.filter(role='student').count()
        admins_count = User.objects.filter(role='admin').count()
        ijarachi_count = User.objects.filter(role='ijarachi').count()
        sardor_count = User.objects.filter(role='sardor').count()

        # Universitetlar statistikasi
        total_universities = University.objects.count()

        # Arizalar statistikasi
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(status='Pending').count()
        approved_applications = Application.objects.filter(status='Approved').count()
        rejected_applications = Application.objects.filter(status='Rejected').count()

        # Xonalar statistikasi (Django ORM aggregate ishlatish)
        from django.db.models import Sum
        
        total_rooms = Room.objects.count()
        total_capacity = Room.objects.aggregate(Sum('capacity'))['capacity__sum'] or 0
        total_occupied = Room.objects.aggregate(Sum('current_occupancy'))['current_occupancy__sum'] or 0
        total_free = total_capacity - total_occupied

        # Viloyatlar statistikasi
        total_provinces = Province.objects.count()

        # Kvartiralar statistikasi
        total_apartments = Apartment.objects.filter(is_active=True).count()

        return Response({
            "dormitories": {
                "total": total_dormitories,
                "active": active_dormitories
            },
            "users": {
                "total": total_users,
                "active": active_users,
                "students": students_count,
                "admins": admins_count,
                "ijarachi": ijarachi_count,
                "sardor": sardor_count
            },
            "universities": {
                "total": total_universities
            },
            "applications": {
                "total": total_applications,
                "pending": pending_applications,
                "approved": approved_applications,
                "rejected": rejected_applications
            },
            "rooms": {
                "total": total_rooms,
                "capacity": total_capacity,
                "occupied": total_occupied,
                "free": total_free,
                "occupancy_rate": round((total_occupied / total_capacity * 100) if total_capacity > 0 else 0, 1)
            },
            "provinces": {
                "total": total_provinces
            },
            "apartments": {
                "total": total_apartments
            }
        }, status=status.HTTP_200_OK)