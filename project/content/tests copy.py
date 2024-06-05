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


кусок:
<form >
                                <input type = "radio" id = "html" name = "fav_language" value = "HTML" >
                                <label for = "html" > HTML < /label > <br >
                                <input type = "radio" id = "css" name = "fav_language" value = "CSS" >
                                <label for = "css" > CSS < /label > <br >
                                <input type = "radio" id = "javascript" name = "fav_language" value = "JavaScript" >
                                <label for = "javascript" > JavaScript < /label >
</form >


if self.request.user == Post.objects.get(id=self.kwargs['pk']).user:
    print(self.request.user, Post.objects.get(
        id=self.kwargs['pk']).user)
else:
    return redirect('home')

    form = AddPostForm(request.POST)
    cd = Post(form.cleaned_data)
    post = Post.objects.get(id=pk)
    post.objects.update(
        title=cd.title, text=cd.text, category=cd.category)

{% if {{ f.file_type }} == "img" % }
<img src = {{f.file}} style = "width: 150px; height: 150px; object-fit: cover; margin: 0px 10px" >
{% endif % }

<input type = "text" id = "comm_edit" name = "comm_edit" value = {{comment.text}} > <br >
<label for = "comm_edit" > Комментарий < /label > <br >
