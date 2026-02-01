from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    
    # Admin Dashboard
    path('admin/dashboard/', AdminDashboardStatsView.as_view(), name='admin-dashboard'),
    path('admin/my-dormitories/', MyDormitoriesListView.as_view(), name='my-dormitories-list'),
    path('admin/my-dormitory/', MyDormitoryView.as_view(), name='my-dormitory'),
    
    # Users
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    
    # User Profiles
    path('profiles/', UserProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    
    # Provinces
    path('provinces/', ProvinceListView.as_view(), name='province-list'),
    path('provinces/<int:pk>/', ProvinceDetailView.as_view(), name='province-detail'),
    
    # Districts
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('districts/<int:pk>/', DistrictDetailView.as_view(), name='district-detail'),
    
    # Universities
    path('universities/', UniversityListView.as_view(), name='university-list'),
    path('universities/<int:pk>/', UniversityDetailView.as_view(), name='university-detail'),
    
    # Amenities
    path('amenities/', AmenityListView.as_view(), name='amenity-list'),
    path('amenities/<int:pk>/', AmenityDetailView.as_view(), name='amenity-detail'),
    
    # Dormitories
    path('dormitories/', DormitoryListView.as_view(), name='dormitory-list'),
    path('dormitories/create/', DormitoryCreateView.as_view(), name='dormitory-create'),
    path('dormitories/<int:pk>/', DormitoryDetailView.as_view(), name='dormitory-detail'),
    
    # Dormitory Images
    path('dormitory-images/', DormitoryImageListView.as_view(), name='dormitory-image-list'),
    path('dormitory-images/<int:pk>/', DormitoryImageDetailView.as_view(), name='dormitory-image-detail'),
    
    # Rules
    path('rules/', RuleListView.as_view(), name='rule-list'),
    path('rules/<int:pk>/', RuleDetailView.as_view(), name='rule-detail'),
    
    # Floors
    path('floors/', FloorListView.as_view(), name='floor-list'),
    path('floors/<int:pk>/', FloorDetailView.as_view(), name='floor-detail'),
    
    # Rooms
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    
    # Students
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/create/', StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('students/unassigned/', UnassignedStudentsView.as_view(), name='unassigned-students'),
    path('students/<int:student_id>/assign-room/', AssignRoomToStudentView.as_view(), name='assign-room'),
    path('students/<int:student_id>/remove-room/', RemoveStudentFromRoomView.as_view(), name='remove-room'),
    
    # Student Dashboard (Talaba uchun maxsus endpointlar)
    path('student/dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),
    path('student/payments/', StudentPaymentsView.as_view(), name='student-payments'),
    path('student/roommates/', StudentRoommatesView.as_view(), name='student-roommates'),
    path('student/attendance/', StudentAttendanceView.as_view(), name='student-attendance'),
    path('student/collections/', StudentCollectionsView.as_view(), name='student-collections'),
    path('student/application/', StudentApplicationView.as_view(), name='student-application'),
    # Notifications - Bitta unified endpoint
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('notifications/mark-read/', MarkNotificationAsReadView.as_view(), name='mark-notification-read'),
    path('notifications/mark-all-read/', MarkAllNotificationsAsReadView.as_view(), name='mark-all-notifications-read'),
    path('notifications/unread-count/', UnreadNotificationCountView.as_view(), name='unread-notification-count'),
    
    # Applications
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/approve/', ApplicationApproveView.as_view(), name='application-approve'),  # PUT/PATCH
    path('applications/<int:pk>/reject/', ApplicationRejectView.as_view(), name='application-reject'),  # PUT/PATCH
    
    # Payments
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
    
    # Tasks
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    
    # Apartments
    path('apartments/', ApartmentListView.as_view(), name='apartment-list'),
    path('apartments/create/', ApartmentCreateView.as_view(), name='apartment-create'),
    path('apartments/<int:pk>/', ApartmentDetailView.as_view(), name='apartment-detail'),
    
    # Apartment Images
    path('apartment-images/', ApartmentImageListView.as_view(), name='apartment-image-list'),
    path('apartment-images/<int:pk>/', ApartmentImageDetailView.as_view(), name='apartment-image-detail'),
    
    # Notifications - Faqat bitta unified endpoint
    
    # Floor Leaders
    path('floor-leaders/', FloorLeaderListView.as_view(), name='floor-leader-list'),
    path('floor-leaders/<int:pk>/', FloorLeaderDetailView.as_view(), name='floor-leader-detail'),
    
    # Attendance Sessions
    path('attendance-sessions/', AttendanceSessionListView.as_view(), name='attendance-session-list'),
    path('attendance-sessions/create/', AttendanceSessionCreateView.as_view(), name='attendance-session-create'),
    path('attendance-sessions/<int:pk>/', AttendanceSessionDetailView.as_view(), name='attendance-session-detail'),
    
    # Attendance Records
    path('attendance-records/', AttendanceRecordListView.as_view(), name='attendance-record-list'),
    path('attendance-records/<int:pk>/', AttendanceRecordDetailView.as_view(), name='attendance-record-detail'),
    
    # Collections
    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/create/', CollectionCreateView.as_view(), name='collection-create'),
    path('collections/<int:pk>/', CollectionDetailView.as_view(), name='collection-detail'),
    
    # Collection Records
    path('collection-records/', CollectionRecordListView.as_view(), name='collection-record-list'),
    path('collection-records/<int:pk>/', CollectionRecordDetailView.as_view(), name='collection-record-detail'),
    
    # Tasks for Leaders
    path('tasks-for-leaders/', TaskForLeaderListView.as_view(), name='task-for-leader-list'),
    path('tasks-for-leaders/create/', TaskForLeaderCreateView.as_view(), name='task-for-leader-create'),
    path('tasks-for-leaders/<int:pk>/', TaskForLeaderDetailView.as_view(), name='task-for-leader-detail'),
    
    # Duty Schedules
    path('duty-schedules/', DutyScheduleListView.as_view(), name='duty-schedule-list'),
    path('duty-schedules/<int:pk>/', DutyScheduleDetailView.as_view(), name='duty-schedule-detail'),

]
