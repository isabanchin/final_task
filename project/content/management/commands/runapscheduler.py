import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ...models import User, Post
import datetime

logger = logging.getLogger(__name__)  # выводит сообщение о запуске


def my_job():  # функция которая срабатывает по триггеру
    print('hello from job')
    # Создаем класс для контекстного объекта передачи данных в шаблон

    class Subscrib:
        post_set = {}

    # Находим дату недельной давности:
    minus_week = datetime.datetime.now() - datetime.timedelta(days=7)
    # Формируем список получателей:
    subscribers_query_set = User.objects.all()
    email_list = []
    for subscriber in subscribers_query_set:
        email_list.append(subscriber.email)
    print(email_list)
    # Формируем объект для передачи контекста
    post_list = []
    # context_obj = Subscrib()
    context_obj = Post.objects.filter(time__gt=minus_week)
    for post in context_obj:
        post.url = f'http://127.0.0.1:8000/{post.get_absolute_url()}'
        post_list.append(f'Объявление "{post.title}" от {post.user}, ')
        print(post.url)
    # адресуем контекст альтернативному шаблону еженедельной рассыылки
    html_content = render_to_string(
        'content/email_weekly.html',
        {
            'context_obj': context_obj,
        }
    )
    # формируем текстовое сообщение:
    msg = EmailMultiAlternatives(
        subject='Еженедельная сводка фанатского сервера "MMORPG"',
        # это то же, что и message
        body=f"Сводка объявлений опубликованных за неделю: {post_list}",
        from_email='sabanchini@yandex.ru',
        to=email_list,
    )
    msg.attach_alternative(
        html_content, "text/html")  # добавляем html
    msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            trigger=CronTrigger(day_of_week="tue", hour="18", minute="07"),
            # trigger=CronTrigger(day_of_week="mon", hour="01", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            # изменение имени функции при запуске при неоконченной предыдущей.
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
