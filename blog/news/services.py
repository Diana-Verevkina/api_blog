from django.contrib.contenttypes.models import ContentType

from .models import Read_post


def add_read(obj, user):
    """Отмечает прочитанным `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    read, is_created = Read_post.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return read


def remove_read(obj, user):
    """Отмечает не прочитанным `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Read_post.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_read(obj, user) -> bool:
    """Проверяет, прочитал ли `user` `obj`."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    reads = Read_post.objects.filter(content_type=obj_type, object_id=obj.id,
                                    user=user)
    return reads.exists()
