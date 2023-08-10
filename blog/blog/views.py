import datetime

from django.http import HttpResponse

from blog.blog.tasks import send_daily_emails


def schedule_daily_emails(request):
    # Запланируйте первичную задачу на завтра
    tomorrow = datetime.now() + datetime.timedelta(days=1)
    send_daily_emails.apply_async(eta=tomorrow.replace(hour=0, minute=0, second=0, microsecond=0))
    return HttpResponse("Первичная задача запланирована")