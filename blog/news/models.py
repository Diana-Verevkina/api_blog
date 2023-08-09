from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.models import User

User = get_user_model()

"""
class MyUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'MyUser'
        verbose_name_plural = 'MyUsers'

    def __str__(self):
        return self.username
"""

class Blog(models.Model):
    user = models.OneToOneField(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, related_name='blog')

    def __str__(self):
        return f'Блог пользователя {self.user.username}'


@receiver(post_save, sender=User)
def save_or_create_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance)
    else:
        try:
            instance.blog.save()
        except ObjectDoesNotExist:
            Blog.objects.create(user=instance)


class Post(models.Model):
    header = models.TextField(verbose_name='Заголовок поста',
                              help_text='Введите заголовок поста',
                              )
    text = models.CharField(verbose_name='Текст поста',
                            help_text='Введите текст поста', max_length=140,
                            null=True, blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='posts')

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.header


class Follow(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             on_delete=models.CASCADE, blank=True,
                             null=True, related_name='follower',
                             help_text='Ссылка на объект пользователя, '
                                       'который подписывается')
    blog = models.ForeignKey(Blog, verbose_name='Блог',
                               on_delete=models.CASCADE, blank=True,
                               null=True, related_name='following',
                               help_text='Ссылка на блог пользователя, '
                                         'на который подписываются')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.author.username
