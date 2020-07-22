import jwt
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import View

from .forms import TaskForm
from .models import User, NoteBoard


class AjaxHandlerView(View):
    def get(self, request):
        d = request.GET
        isuser = request.session.get('isuser', '0')

        if str(d.get("d[1][value]")).__len__() > 0:
            user = User.objects.get(user_token=isuser)
            user.noteboard_set.create(
                note_title=d.get("d[1][value]"),
                note_text=d.get("rich"),
                note_tags=d.get("d[3][value]"),
                pub_date=timezone.localtime(timezone.now()))
            user.save()

            data = {
                'is_taken': True
            }
        else:
            data = {
                'is_taken': False
            }

        return JsonResponse(data)


# users funs
def index(request):
    isuser = request.session.get('isuser', '0')

    if isuser == '0':
        return HttpResponseRedirect(reverse('notes:sign_in'))
    else:
        return HttpResponseRedirect(reverse('notes:board'))


def sign_in(request):
    isuser = request.session.get('isuser', '0')
    if isuser != '0':
        return HttpResponseRedirect(reverse('notes:board'))

    if request.method == 'POST':
        mail = str(request.POST['email'])
        passw = str(request.POST['pass'])

        user = User.objects.filter(user_email=mail, user_pass=passw)
        if user.exists():
            encoded = str(jwt.encode({'email': mail, 'passw': passw}, 'secret', algorithm='HS256'))
            user[0].user_token = encoded
            user[0].save()

            request.session['isuser'] = str(encoded)
            return HttpResponseRedirect(reverse('notes:board'))

        else:
            message = "Not correct data"
            return render(request, "login/index.html", {"message": message})
    return render(request, "login/index.html")


def sign_up(request):
    isuser = request.session.get('isuser', '0')
    if isuser != '0':
        return HttpResponseRedirect(reverse('notes:board'))

    if request.method == 'POST':
        t = request.POST
        isnormal = check(t)
        if not isnormal[0] == 0:

            return render(request, 'login/register.html', {'ctx': isnormal[1], 'ans_mess': ans_to_mess(isnormal[0])})
        else:
            encoded = str(jwt.encode({'email': t['email'], 'passw': t['pass']}, 'secret', algorithm='HS256'))
            user = User.objects.create(user_name=t['name'],
                                       user_email=t['email'],
                                       user_pass=t['pass'],
                                       user_token=encoded)
            user.save()
            request.session['isuser'] = str(encoded)
            return HttpResponseRedirect(reverse('notes:board'))

    else:
        return render(request, 'login/register.html')


def logout(request):
    request.session['isuser'] = '0'
    return HttpResponseRedirect(reverse('notes:index'))


# end

# board funs
def create(request):
    isuser = request.session.get('isuser', '0')
    if isuser == '0':
        return HttpResponseRedirect(reverse('notes:index'))
    else:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                user = User.objects.get(user_token=isuser)
                t = form.data
                user.noteboard_set.create(note_title=t.get('note_title'),
                                          note_text=t.get('note_title'),
                                          note_tags=t.get('note_tags'))
                user.save()
        form = TaskForm()
        context = {'form': form}
        return render(request, 'board/create.html', context)


def board(request):
    isuser = request.session.get('isuser', '0')
    if isuser == '0':
        return HttpResponseRedirect(reverse('notes:index'))
    user = User.objects.get(user_token=isuser)
    boards = user.noteboard_set.order_by('-id')
    form = TaskForm()
    return render(request, 'board/index.html', {'user': user, 'note': boards, 'form': form})


def about(request):
    isuser = request.session.get('isuser', '0')
    if isuser == '0':
        return render(request, "login/index.html")
    user = User.objects.get(user_token=isuser)
    form = TaskForm()
    return render(request, 'board/about.html', {'user': user, 'form': form})


def settings(request):
    form = TaskForm()
    return render(request, 'board/settings.html', {'form': form})


def del_note(request, note_id):
    isuser = request.session.get('isuser', '0')
    user = User.objects.get(user_token=isuser)
    NoteBoard.objects.get(user=user, id=note_id).delete()
    return HttpResponseRedirect(reverse('notes:board'))


def edit_note(request, note_id):
    isuser = request.session.get('isuser', '0')
    if isuser == '0':
        return render(request, "login/index.html")
    else:
        user = User.objects.get(user_token=isuser)

        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                user = User.objects.get(user_token=isuser)
                t = form.data
                notes = user.noteboard_set.get(id=note_id)
                notes.note_title = t.get('note_title')
                notes.note_text = t.get('note_text')
                notes.note_tags = t.get('note_tags')
                notes.save()
                user.save()
                return HttpResponseRedirect(reverse('notes:board'))

        data = user.noteboard_set.get(id=note_id)
        form = TaskForm()
        editform = TaskForm(auto_id=True)

        editform.fields['note_title'].initial = data.note_title
        editform.fields['note_text'].initial = data.note_text
        editform.fields['note_tags'].initial = data.note_tags

    context = {'form': form, 'editform': editform}
    return render(request, 'board/editer.html', context)


# end


# extra
def check(t):
    ans_code = 0
    if User.objects.filter(user_email=t['email']).exists():
        ans_code = ans_code + 1
    if not str(t['pass']) == str(t['reppass']):
        ans_code = ans_code - 2

    context = {
        "ans": ans_code,
        "name": t['name'],
        "email": t['email'],
        "pass": t['pass'],
        "reppass": t['reppass']
    }
    return [ans_code, context]


def ans_to_mess(ans):
    mess = ""
    if ans == 1:
        mess = "Эта почта уже используется."
    elif ans == -1:
        mess = "Эта почта уже используется и пароли не совпадают."
    elif ans == -2:
        mess = "Пароли не совпадают."
    return mess
