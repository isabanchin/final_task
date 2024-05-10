from django.db import models
class Ct(models.TextChoices):
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
category = models.CharField(max_length=15, choices=tuple(map(lambda x: (x[0], x[1]), Ct.choices)),
                                    default=Ct.tanks, verbose_name="Категория")


choices=tuple(map(lambda x: (x[0], x[1]), Ct.choices))

print(choices)
# print(lambda x: (x[0], x[1]), Ct.choices)
# print(map(lambda x: (x[0], x[1]), Ct.choices))
print(Ct.tanks)
# print(tuple(Ct.choices))
# print(Ct.choices)