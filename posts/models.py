from django.db    import models
from django.db.models.deletion import CASCADE

from core.models  import TimeStamp
from users.models import User


class Post(TimeStamp):
    author  = models.CharField(max_length = 16)
    title   = models.CharField(max_length = 200)
    content = models.TextField()
    user    = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        db_table = 'posts'