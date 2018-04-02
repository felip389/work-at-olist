from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


# Create your models here.

class CallRecordSignal(models.Model):
    recordId = models.IntegerField(default=0)
    callType = models.CharField(max_length=5, default='')
    call_id = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=11, default='', blank=True)
    destination = models.CharField(max_length=11, default='', blank=True)

    class Meta:
        ordering = (
            'recordId',
        )
