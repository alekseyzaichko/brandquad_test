from rest_framework import serializers
from main.models import Log


class LogSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    http_method = serializers.SerializerMethodField()

    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%d.%m.%Y %H:%M:%S')

    def get_http_method(self, obj):
        return obj.get_http_method_display().upper()

    class Meta:
        model = Log
        fields = ('ip_address', 'timestamp', 'http_method', 'uri',
                  'status_code', 'content_length', 'user_agent', 'referer')
