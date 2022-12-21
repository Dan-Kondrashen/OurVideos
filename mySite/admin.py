from django.contrib import admin
from mySite.models import Videos, VideoType, VideoActor, ActorToFilm, VideoDirector, UserInfo, Comments, RatingStar, \
    Rating, VideoCountrу

# Register your models here.
admin.site.register([ActorToFilm, ])


class CommentsInline(admin.StackedInline):
    model = Comments
    extra = 0

@admin.register(VideoCountrу)
class VideoCountryAdmin(admin.ModelAdmin):
    list_display = ('CountryName',)

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ("username",)


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ("VideoName", "VideoDesc", "videoTypes", "videoActors", "VideoBy")
    list_filter = ("VideoBy", "Types", "releaseDate")
    search_fields = ("VideoName",)
    inlines = [
        CommentsInline
    ]


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("value",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("video", "star", "user", "reRating")
    list_filter = ("star",)



# "videoActors",
@admin.register(VideoActor)
class VideoActorAdmin(admin.ModelAdmin):
    list_display = ("ActorFIO", "ActorPhoto", "ActorInfo")
    search_fields = ("ActorFIO",)


@admin.register(VideoType)
class VideoTypeAdmin(admin.ModelAdmin):
    list_display = ("TypeName", "TypeDesc")


@admin.register(VideoDirector)
class VideoDirectorAdmin(admin.ModelAdmin):
    list_display = ("DirectFIO", "DirectPhoto", "DirectInfo")
    search_fields = ("DirectFIO",)
