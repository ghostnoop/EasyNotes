from django.core.signing import Signer
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from notes.models import User
from .models import SharedNotes


def create(request, note_id):
    isuser = request.session.get('isuser', '0')
    if isuser == '0':
        return HttpResponseRedirect(reverse('notes:index'))

    user = User.objects.get(user_token=isuser)
    notes = user.noteboard_set.filter(id=note_id)

    if notes.exists():
        note = notes[0]
        signer = Signer(salt="yellowTulpans")

        value = signer.sign(str(note.id) + "||" + str(note.pub_date) + "||").split("||")
        link = str(value[0] + value[2] + ":" + str(note.user.id))
        print(link)

        prev = SharedNotes.objects.filter(note_from_board_id=note.id)
        s = request.build_absolute_uri().replace(request.path, '/share/')
        if not prev.exists():
            SharedNotes.objects.create(
                note_from_board=note,
                note_link=link
            )
            return render(request, 'share/create.html', {'link': "share/" + link, "full_link": s + link})
        else:
            return render(request, 'share/create.html', {'link': "share/" + prev[0].note_link, "full_link": s + link})

    return HttpResponse("Not exist 404")


def shared(request, unique_id):
    uniq_array = str(unique_id).split(":")

    note = SharedNotes.objects.filter(note_from_board__user_id=uniq_array[2], note_from_board_id=uniq_array[0])
    if note.exists():
        if note[0].note_link == unique_id:
            nboard = note[0].note_from_board
            context = {
                "title": nboard.note_title,
                "text": nboard.note_text,
                "tags": str(nboard.note_tags).split(","),
                "date": nboard.pub_date
            }
            return render(request, 'share/show.html', {"notes": context})

    return HttpResponse("404")
