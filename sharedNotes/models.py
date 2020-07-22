from django.db import models

# Create your models here.
from notes.models import User, NoteBoard


class SharedNotes(models.Model):
    note_from_board = models.ForeignKey(NoteBoard, on_delete=models.CASCADE)
    note_link = models.CharField('ссылка', max_length=40)

    def __str__(self):
        return str(self.note_from_board.user) + " id: " + str(self.note_from_board_id)
