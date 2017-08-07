from django.db import models
from django.conf import settings

from sorl.thumbnail import ImageField

def user_path(instance, filename):
    from random import choice
    import string
    arr = [choice(string.ascii_letters) for _ in range(8)]  # string.ascii_letters는 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz를 출력함
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    # file will be uploaded to MEDIA_ROOT/user_<id>/<random>
    return '%s/%s.%s' % (instance.owner.username, pid, extension)


class Photo(models.Model):
    image = models.ImageField(upload_to = user_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.CharField(max_length = 255)
    pub_date = models.DateTimeField(auto_now_add = True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {}'.format(self.owner.username, self.comment, self.is_public)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    profile_photo = models.ImageField(blank = True)
    nickname = models.CharField(max_length = 64)