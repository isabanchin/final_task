from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tanks = 'Tn'
    khila = 'Kh'
    dd = 'DD'
    traders = 'Tr'
    guildmasters = 'GM'
    questgivers = 'QG'
    blacksmiths = 'BS'
    tanners = 'Tn'
    potions_makers = 'PM'
    spell_masters = 'SM'
    CATEGORY_CHOICES = (
        (tanks, 'Танки'),
        (khila, 'Хилы'),
        (dd, 'ДД'),
        (traders, 'Торговцы'),
        (guildmasters, 'Гилдмастеры'),
        (questgivers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potions_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний')
    )
    category = models.CharField(
        max_length=15, choices=CATEGORY_CHOICES, verbose_name='Категория')
    time = models.DateTimeField(auto_now_add=True)
    tittle = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads_model', verbose_name='Файл')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acception = models.BooleanField(default=False, verbose_name='Принять')
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Содержимое')


