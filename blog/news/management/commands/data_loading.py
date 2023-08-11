import random

from RandomWordGenerator import RandomWord
from django.core.management import BaseCommand
from news.models import Blog, Post, User, Follow
from password_generator import PasswordGenerator
from random_username.generate import generate_username

pwo = PasswordGenerator()
pwo.excludeschars = "*#№@()&?!$%^=+,"
pwo.minlen = 7
pwo.maxlen = 15
pwo.minuchars = 1
pwo.minlchars = 3
pwo.minnumbers = 1

rw = RandomWord(max_word_size=10,
                constant_word_size=True,
                include_digits=False,
                special_chars=r"@_!#$%^&*()<>?/\|}{~:",
                include_special_chars=False)

first_id_user = User.objects.first().id
last_id_user = User.objects.last().id


class Command(BaseCommand):
    help = 'Загрузка данных в БД'

    def handle(self, *args, **options):

        # User.objects.all().delete()

        if User.objects.exists():
            raise Exception('Ошибка. Данные в модель User уже загружены.')
        else:
            print(f'Загрузка данных в модель User...')
        usernames = set()
        for user in range(600):
            usernames.add(generate_username()[0])

        for person in range(len(usernames)):
            User.objects.create(username=list(usernames)[person],
                                password=pwo.generate())

        # Post.objects.all().delete()

        if Post.objects.exists():
            raise Exception('Ошибка. Данные в модель Post уже загружены.')
        else:
            print(f'Загрузка данных в модель Post...')

        for post in range(500):
            Post.objects.create(
                header=' '.join(rw.getList(4)), text=' '.join(rw.getList(10)),
                author=User.objects.get(id=(random.randint(
                    first_id_user, last_id_user))))

        for post in Post.objects.all():
            post.blog = post.author.blog
            post.save()

        print(f'---------------------------')

        # Follow.objects.all().delete()

        if Follow.objects.exists():
            raise Exception('Ошибка. Данные в модель Follow уже загружены.')
        else:
            print(f'Загрузка данных в модель Follow...')

        for follow in range(300):
            user_id = random.randint(first_id_user, last_id_user)
            blog_exclude_id = User.objects.get(id=user_id).blog.id
            blog_id = random.choice([i for i in range(
                first_id_user, last_id_user) if i !=blog_exclude_id])
            Follow.objects.create(
                user=User.objects.get(
                    id=(random.randint(first_id_user, last_id_user))),
                blog=Blog.objects.get(id=blog_id),
                blog_author=Blog.objects.get(id=blog_id).user)
