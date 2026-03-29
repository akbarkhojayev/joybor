from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Application, Student, ApplicationNotification, Notification, UserNotification, Room


@receiver(post_save, sender=Student)
def update_room_occupancy_on_save(sender, instance, created, **kwargs):
    """
    Student saqlanganda yoki o'zgartirilganda xona occupancy ni yangilash
    """
    # Agar yangi yaratilgan bo'lsa va xonaga biriktirilgan bo'lsa
    if created:
        if instance.room:
            instance.room.update_occupancy()
    else:
        # O'zgartirilgan bo'lsa - faqat hozirgi xonani yangilash
        if instance.room:
            instance.room.update_occupancy()


@receiver(post_delete, sender=Student)
def update_room_occupancy_on_delete(sender, instance, **kwargs):
    """
    Student o'chirilganda xona occupancy ni yangilash
    """
    # Agar student xonaga biriktirilgan bo'lgan bo'lsa
    if instance.room:
        instance.room.update_occupancy()


@receiver(post_save, sender=Application)
def handle_application_approval(sender, instance, created, **kwargs):
    """
    Ariza Approved holatiga o'zgarganda avtomatik Student yaratish
    """
    # Yangi ariza yaratilganda adminga bildirishnoma yuborish
    if created and instance.user:
        # Ariza yuborilgan yotoqxona adminiga bildirishnoma
        if instance.dormitory and instance.dormitory.admin:
            ApplicationNotification.objects.create(
                user=instance.dormitory.admin,
                message=f"Yangi ariza keldi: {instance.name} {instance.last_name} ({instance.passport}). Fakultet: {instance.faculty or 'Korsatilmagan'}"
            )
    
    # Faqat status o'zgarganda ishlaydi (created=False)
    if not created and instance.status == 'Approved':
        # Agar bu ariza uchun allaqachon Student yaratilgan bo'lsa, qayta yaratmaymiz
        if Student.objects.filter(passport=instance.passport).exists():
            # Lekin bildirishnoma yuborilmagan bo'lsa, yuboramiz
            if instance.user:
                # Avval yuborilgan bildirishnoma bormi tekshiramiz
                existing_notification = ApplicationNotification.objects.filter(
                    user=instance.user,
                    message__contains=f"{instance.dormitory.name} yotoqxonasiga qabul qilindingiz"
                ).exists()
                
                if not existing_notification:
                    ApplicationNotification.objects.create(
                        user=instance.user,
                        message=f"Tabriklaymiz! Arizangiz tasdiqlandi. Siz {instance.dormitory.name} yotoqxonasiga qabul qilindingiz."
                    )
            return
        
        # Yangi Student yaratish (is_active=False, xona biriktirilmagan)
        student = Student.objects.create(
            user=instance.user,
            name=instance.name,
            last_name=instance.last_name,
            middle_name=instance.middle_name,
            province=instance.province,
            district=instance.district,
            faculty=instance.faculty,
            direction=instance.direction,
            dormitory=instance.dormitory,
            passport=instance.passport,
            group=instance.group,
            course=instance.course,
            gender=instance.gender,
            phone=instance.phone,
            picture=instance.user_image if hasattr(instance, 'user_image') else None,
            passport_image_first=instance.passport_image_first,
            passport_image_second=instance.passport_image_second,
            document=instance.document,
            status='Tasdiqlandi',
            placement_status='Qabul qilindi',
            is_active=False
        )
        
        # Foydalanuvchiga bildirishnoma yuborish
        if instance.user:
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Tabriklaymiz! Arizangiz tasdiqlandi. Siz {instance.dormitory.name} yotoqxonasiga qabul qilindingiz."
            )
        else:
            # Agar user yo'q bo'lsa, log qilamiz (debug uchun)
            print(f"WARNING: Application {instance.id} approved but no user assigned!")
    
    elif not created and instance.status == 'Rejected':
        # Rad etilgan ariza uchun bildirishnoma
        if instance.user:
            # Avval yuborilgan bildirishnoma bormi tekshiramiz
            existing_notification = ApplicationNotification.objects.filter(
                user=instance.user,
                message__contains="Arizangiz rad etildi"
            ).exists()
            
            if not existing_notification:
                ApplicationNotification.objects.create(
                    user=instance.user,
                    message=f"Arizangiz rad etildi. Sabab: {instance.admin_comment or 'Sabab korsatilmagan'}"
                )
        else:
            print(f"WARNING: Application {instance.id} rejected but no user assigned!")


@receiver(post_save, sender=Notification)
def send_notification_to_users(sender, instance, created, **kwargs):
    """
    Notification yaratilganda avtomatik foydalanuvchilarga yuborish
    """
    if created:
        # Target type ga qarab foydalanuvchilarga yuborish
        if instance.target_type == 'all_students':
            # Barcha studentlarga yuborish
            from .models import User
            students = User.objects.filter(role='student')
            for student in students:
                UserNotification.objects.get_or_create(
                    user=student,
                    notification=instance
                )
        
        elif instance.target_type == 'all_admins':
            # Barcha adminlarga yuborish
            from .models import User
            admins = User.objects.filter(role='admin')
            for admin in admins:
                UserNotification.objects.get_or_create(
                    user=admin,
                    notification=instance
                )
        
        elif instance.target_type == 'specific_user' and instance.target_user:
            # Ma'lum foydalanuvchiga yuborish
            UserNotification.objects.get_or_create(
                user=instance.target_user,
                notification=instance
            )