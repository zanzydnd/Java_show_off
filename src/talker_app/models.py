from django.contrib.auth.models import User
from django.db import models


class BaseTalk(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Talk(BaseTalk):
    class Meta:
        verbose_name = "Talk"
        verbose_name_plural = "Talks"
        db_table = "talk"

class TalkAnswer(BaseTalk):
    head_talk = models.ForeignKey(Talk, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "answer_talk"
        verbose_name_plural = "answer_talks"
        db_table = "answer_talk"