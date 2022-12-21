import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ChoiseForm, LoginForm, ModelForm, RegisterForm, userChangeInfo, CreateComment, RatingForm
from mySite.models import *


def registerPage(request):
    # инициализируем объект формы

    if request.method == 'POST':
        # заполняем объект данными формы, если она была отправлена
        form = RegisterForm(request.POST)

        if form.is_valid():
            # если форма валидна - создаем нового пользователя
            form.save()
            return redirect('login')
        print(form.errors)
    else:
        form = RegisterForm()
    # ренедерим шаблон и передаем объект формы
    return render(request, 'registration.html', {'form': form})


def loginPage(request):
    # инициализируем объект класса формы
    form = LoginForm()

    # обрабатываем случай отправки формы на этот адрес
    if request.method == 'POST':

        # заполянем объект данными, полученными из запроса
        form = LoginForm(request.POST)

        # проверяем валидность формы
        if form.is_valid():
            # пытаемся авторизовать пользователя
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('Главная страница')
            else:

                form.add_error(None, 'Неверные данные!')

    return render(request, 'login.html', {'form': form})


def doLogout(request):
    # вызываем функцию django.contrib.auth.logout и делаем редирект на страницу входа
    logout(request)
    return redirect('Главная страница')


def index(request):
    return render(request, "homePage.html")


def userGetInf(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        form = userChangeInfo()
        if request.method == 'POST':
            form = userChangeInfo(request.POST)
        return render(request, 'userInfo.html', {'user': request.user, 'form': form})


def index2(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:

        vid = Videos.objects.all()
        if request.method == "GET":
            FormChoise = ChoiseForm(request.GET)
            if FormChoise.is_valid():

                if FormChoise.cleaned_data["types"]:
                    vid = vid.filter(Types__TypeName=FormChoise.cleaned_data["types"])
                if FormChoise.cleaned_data["types1"]:
                    vid = vid.filter(Types__TypeName=FormChoise.cleaned_data["types1"])
                if FormChoise.cleaned_data["videos"]:
                    vid = vid.filter(VideoBy__DirectFIO=FormChoise.cleaned_data["videos"])
                if FormChoise.cleaned_data["vids"]:
                    vid = vid.filter(VideoBy__DirectFIO=FormChoise.cleaned_data["vids"])
        else:
            FormChoise = ChoiseForm()
        return render(request, "catalogblock.html", {'form': FormChoise, 'vid': vid})


# video = request.POST.get("video")
# typeV = request.POST.get("typeV")
# if request.method == "POST":


#
#     # output = "<br><h2>Пользователь: {0}</h2></br> <h3>Имя: {0} Возраст: {1}"\
#     #     .format(typeV,video)
#     FormChoise = ChoiseForm(request.POST)
#     if FormChoise.is_valid():
#         print(FormChoise.cleaned_data)
# else:
#     FormChoise = ChoiseForm()
# return render(request, "Catalog.html", {'form': FormChoise})
def index3(request):
    return render(request, "videoVisual.html")


def dopoln(request):
    videoInf = Videos.objects.all()
    viFilter = Videos.objects.filter(releaseDate__gt=datetime.date(2010, 1, 1))

    context = {
        'videoInfo': videoInf,
        'viFilters': viFilter,

    }
    return render(request, "ForVideo.html", context)


def show_video(request, video_id):
    videos = get_object_or_404(Videos, id=video_id)
    link = ActorToFilm.objects.filter(VideoN__VideoName=videos.VideoName)
    getVideoRating = Rating.objects.filter(video__VideoName=videos.VideoName).aggregate(Avg('star'))['star__avg']
    gf = round(getVideoRating * 10) / 10
    viClass = Videos.objects.filter(VideoClass=videos.VideoClass)
    star_form = RatingForm()

    if request.method == "POST":
        form = CreateComment(request.POST)  # Получаем данные из формы

        if form.is_valid():  # Проверяем валидность формы
            if request.user.is_authenticated:  # Проверяем авторизацию пользователя
                user = request.user
                form.cleaned_data["video_id"] = videos  # Добавляем ключ и значение видео
                form.cleaned_data["user"] = user
                try:
                    Comments.objects.create(**form.cleaned_data)  # Создаем новую запись в таблицу
                    return redirect('videos', video_id)  # Обновляем страницу с видео
                except Exception as Ex:
                    print(Ex)
                    form.add_error(None, 'Ошибка добавления коммента')
            else:
                return redirect("login")

    else:
        form = CreateComment()

    context = {
        'star_form': star_form,
        'videos': videos,
        'content': videos.comments_set.all(),
        'form': form,
        'link': link,
        'video_class': viClass,
        'videoRatings': gf,
    }
    # videos_actorsV=videos.actorsV.all()
    # for i in videos_actorsV:
    #     print(videos_actorsV[i].ActorFIO)
    # actor= VideoActor.objects.filter(ActorFIO__contains=videos.videoActors)
    # actor = ActorToFilm.objects.filter(VideoN__VideoName=videos.VideoName)
    # act = VideoActor.objects.filter(ActorFIO=Videos.objects.filter(actor))
    # context = {
    #    'actor':actor
    # }
    return render(request, "videos.html", context)


def get_video_rating(request):
    if request.method == "POST":
        star = request.POST.get('star')

        video_id = request.POST.get('video')
        form1 = RatingForm(request.POST)
        if form1.is_valid():
            try:
                Rating.objects.update_or_create(
                    user=request.user,
                    video_id=video_id,
                    defaults={'star_id': star}
                ),

                return redirect('videos', video_id)
            except Exception as Ex:
                print(Ex)
                form1.add_error(None, 'Ошибка добавления рейтинга')
            return redirect('videos', video_id)
        else:
            return redirect('videos', video_id)


def search(request):
    if request.method == 'POST':
        searchText = request.POST["searchText"]
        vids = Videos.objects.filter(Q(VideoName__iregex=searchText) | Q(VideoClass__iregex=searchText))
        actor = VideoActor.objects.filter(ActorFIO__iregex=searchText)
        context = {
            'video1': vids,
            'actors': actor
        }
        return render(request, 'search.html', context)


def ourinfo(request):
    return render(request, "ourInfo.html")
