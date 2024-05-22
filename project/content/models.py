from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    # tanks = 'Tk'
    # khila = 'Kh'
    # dd = 'DD'
    # traders = 'Tr'
    # guildmasters = 'GM'
    # questgivers = 'QG'
    # blacksmiths = 'BS'
    # tanners = 'Tn'
    # potions_makers = 'PM'
    # spell_masters = 'SM'
    # CATEGORY_CHOICES = (
    #     (tanks, 'Танки'),
    #     (khila, 'Хилы'),
    #     (dd, 'ДД'),
    #     (traders, 'Торговцы'),
    #     (guildmasters, 'Гилдмастеры'),
    #     (questgivers, 'Квестгиверы'),
    #     (blacksmiths, 'Кузнецы'),
    #     (tanners, 'Кожевники'),
    #     (potions_makers, 'Зельевары'),
    #     (spell_masters, 'Мастера заклинаний')
    # )
    # category = models.CharField(max_length=15, choices=CATEGORY_CHOICES, verbose_name='Категория', default='Tk')
    time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')

    def get_absolute_url(self):
        return 'post/' + str(self.pk)


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads_model', verbose_name='Файл')


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='posts')
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    acception = models.BooleanField(default=False, verbose_name='Принять')
    time = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Комментарий')
