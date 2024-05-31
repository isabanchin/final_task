from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор")

    class Cat(models.TextChoices):
        tanks = 'Tk', 'Танки'
        khila = 'Kh', 'Хилы'
        dd = 'DD', 'ДД'
        traders = 'Tr', 'Торговцы'
        guildmasters = 'GM', 'Гилдмастеры'
        questgivers = 'QG', 'Квестгиверы'
        blacksmiths = 'BS', 'Кузнецы'
        tanners = 'Tn', 'Кожевники'
        potions_makers = 'PM', 'Зельевары'
        spell_masters = 'SM', 'Мастера заклинаний'

    category = models.CharField(max_length=15, choices=tuple(
        map(lambda x: (x[0], x[1]), Cat.choices)), default='Tk', verbose_name="Категория")
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def get_absolute_url(self):
        return 'post/' + str(self.pk)

    def __str__(self):
        return self.title


class Media(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='files')
    # image = models.ImageField(
    #     upload_to='images', default=None, blank=True, verbose_name='Изображения')
    file = models.FileField(
        upload_to='files', verbose_name='Файл')
    file_type = models.CharField(
        max_length=5, default=None, verbose_name='Тип вложения')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, verbose_name="Автор комментария")
    acception = models.BooleanField(default=False, verbose_name='Подтверждено')
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Комментарий')

    def get_absolute_url(self):
        return 'comm/' + str(self.pk)
