from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, Student, ApplicationNotification


@receiver(post_save, sender=Application)
def handle_application_approval(sender, instance, created, **kwargs):
    """
    Ariza Approved holatiga o'zgarganda avtomatik Student yaratish
    """
    if not created and instance.status == 'Approved':
        # Agar bu ariza uchun allaqachon Student yaratilgan bo'lsa, qayta yaratmaymiz
        if Student.objects.filter(passport=instance.passport).exists():
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
            phone=instance.phone,
            picture=instance.user_image if hasattr(instance, 'user_image') else None,
            passport_image_first=instance.passport_image_first,
            passport_image_second=instance.passport_image_second,
            document=instance.document,
            status='Tasdiqlandi',
            placement_status='Qabul qilindi',
            is_active=False  # Xona biriktirilmagan
        )
        
        # Foydalanuvchiga bildirishnoma yuborish
        if instance.user:
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Tabriklaymiz! Arizangiz tasdiqlandi. Siz {instance.dormitory.name} yotoqxonasiga qabul qilindingiz."
            )
    
    elif not created and instance.status == 'Rejected':
        # Rad etilgan ariza uchun bildirishnoma
        if instance.user:
            ApplicationNotification.objects.create(
                user=instance.user,
                message=f"Arizangiz rad etildi. Sabab: {instance.admin_comment or 'Sabab korsatilmagan'}"
            )