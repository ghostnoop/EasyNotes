from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class User(models.Model):
    user_name = models.CharField('Имя пользователя', max_length=50)
    user_email = models.CharField('Почта', max_length=40)
    user_pass = models.CharField('Пароль', max_length=20)
    user_token = models.TextField('токен')

    def __str__(self):
        return self.user_name


class NoteBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.TextField("название заметки")
    #note_text = models.TextField("текст заметки")
    note_text = RichTextField(blank=True, null= True)
    note_tags = models.TextField('тэги')
    pub_date = models.DateTimeField('Дата публикации')

    def __str__(self):
        return "Заметка: " + self.user.user_name

    def get_tags(self):
        return self.note_tags.split(",")
