from django.db import models
from enum import Enum, auto


class Log(models.Model):

    http_methods = models.IntegerChoices(
        'Method', 'GET HEAD POST PUT DELETE CONNECT OPTIONS TRACE PATCH')

    ip_address = models.GenericIPAddressField(protocol='IPv4')
    timestamp = models.DateTimeField()
    http_method = models.PositiveSmallIntegerField(
        choices=http_methods.choices)
    uri = models.TextField()
    status_code = models.PositiveSmallIntegerField()
    content_length = models.PositiveIntegerField()
    user_agent = models.TextField()
    referer = models.TextField()

    class Meta:
        db_table = "logs"

    def __str__(self):
        return self.id
