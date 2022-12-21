from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from Video import settings


class UserInfo(AbstractUser):
    pass


class Comments(models.Model):
    video_id = models.ForeignKey('Videos', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, verbose_name='Коментарий')
    com_date = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)

    class Meta:
        ordering = ['com_date']

    def __str__(self):
        return self.content[0:30]


# Create your models here.
class Videos(models.Model):
    VideoName = models.CharField(max_length=100, verbose_name="Название")
    VideoURL = models.CharField(max_length=100, verbose_name="Ссылка")
    VideoDesc = models.TextField(max_length=900, verbose_name="Описание")
    FrontImg = models.CharField(max_length=70, verbose_name="Титульное фото")
    releaseDate = models.DateField()
    Types = models.ManyToManyField('VideoType', verbose_name="Жанры")
    Countrу = models.ManyToManyField('VideoCountrу', verbose_name="Страны")
    VideoBy = models.ForeignKey('VideoDirector', on_delete=models.DO_NOTHING, verbose_name="Режиссер")
    actorsV = models.ManyToManyField('VideoActor', through='ActorToFilm')
    VideoClass = models.CharField(max_length=100, verbose_name="Серия")

    def videoTypes(self):
        return "%s" % (",\n".join([vtype.TypeName for vtype in self.Types.all()]))
    videoTypes.short_description = "Жанры"

    def videoCountry(self):
        return "%s" % (",\n".join([vtype.CountryName for vtype in self.Countrу.all()]))
    videoCountry.short_description = "Страны"

    def videoActors(self):
        return "%s" % (",\n".join(
            [vActors.Actors.ActorFIO for vActors in ActorToFilm.objects.filter(VideoN__VideoName=self.VideoName)]))
    videoActors.short_description = "Актеры"

    # def videoRating(self):
    #     return "%s" % (",\n".join(
    #         [vRat.reRating for vRat in Rating.objects.filter(VideoN__VideoName=self.VideoName)]))

    def __str__(self):
        return self.VideoName

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class VideoType(models.Model):
    TypeName = models.CharField(max_length=50, verbose_name="Жанр")
    TypeDesc = models.TextField(max_length=600, verbose_name="Описание")

    def __str__(self):
        return self.TypeName

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"



class VideoActor(models.Model):
    ActorFIO = models.CharField(max_length=70, verbose_name="ФИО")
    ActorPhoto = models.CharField(max_length=50, verbose_name="Фото")
    ActorInfo = models.TextField(max_length=600, verbose_name="Информация")

    def __str__(self):
        return self.ActorFIO

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class VideoDirector(models.Model):
    DirectFIO = models.CharField(max_length=70, verbose_name="ФИО")
    DirectPhoto = models.CharField(max_length=50, verbose_name="Фото")
    DirectInfo = models.TextField(max_length=600, verbose_name="Информация")

    def __str__(self):
        return self.DirectFIO

    class Meta:
        verbose_name = "Режисёр"
        verbose_name_plural = "Режисёры"


class RatingStar(models.Model):
    value = models.SmallIntegerField("Число", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Колличество звезд")
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, verbose_name="Название фильма")

    def __str__(self):
        return f"{self.video} - {self.star}"

    def reRating(self):
        if self.star.value > 0:
            return 6 - self.star.value

    reRating.short_description = "Итоговый оценка пользователем"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class ActorToFilm(models.Model):
    ActorRole = models.CharField(max_length=100, verbose_name="Роль актера")
    Actors = models.ForeignKey('VideoActor', on_delete=models.CASCADE, related_name='classOfActorFKay',
                               verbose_name="ФИО актера")
    VideoN = models.ForeignKey('Videos', on_delete=models.CASCADE, related_name='classOFVideoFKay',
                               verbose_name="Название видео")

    def __str__(self):
        return f'Фильм:{self.VideoN.VideoName} Роль:{self.ActorRole}'


class VideoCountrу(models.Model):
    CountryName = models.CharField(max_length=100, verbose_name="Название страны")

    def __str__(self):
        return self.CountryName
    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"