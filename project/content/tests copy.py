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


# choices = tuple(map(lambda x: (x[0], x[1]), Ct.choices))

# print(choices)
# print(lambda x: (x[0], x[1]), Ct.choices)
# print(map(lambda x: (x[0], x[1]), Ct.choices))
# print(type(Ct.tanks))
# print(tuple(Ct.choices))
# print(Ct.choices)
x = 'BS'
# for i in Ct.choices:
#     print(i)
# print([i[1] for i in Ct.choices if i[0] == x])
# print(y)
print(Ct.choices)
print(Ct.labels)
print(Ct.values)
print(Ct.names)
print(Ct(x).label)
