from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import pagination
from .serializers import LogSerializer
from main.models import Log
from django.db.models import Sum, Count, Case, When, Value


class QuerysetFilter(object):

    def get_queryset(self):
        objects = Log.objects.all()

        filter_field = self.request.query_params.get('filter_field', None)
        filter_value = self.request.query_params.get('filter_value', None)
        
        if filter_field and filter_value and hasattr(Log, filter_field):
            if filter_field == 'http_method':
                filter_value = Log.http_methods[filter_value]
            else:
                filter_field = f'{filter_field}__icontains'
                
            objects = Log.objects.filter(**{filter_field: filter_value})
        
        sort_by = self.request.query_params.get('sort_by', None)
        sort_desc = self.request.query_params.get('sort_desc', None)
        
        if sort_by:
            objects = objects.order_by(f'-{sort_by}' if sort_desc == 'true' else sort_by)

        return objects


class StatView(QuerysetFilter, APIView):

    def get(self, request, format=None):
        data = {
            'top_ten': []
        }
        
        logs = self.get_queryset()
        
        stat_data = logs.values('ip_address', 'content_length').annotate(
            count=Count('id', distinct=True)
        ).aggregate(unique_ip=Count('count'), total_length=Sum('content_length', distinct=True))
        
        data.update(stat_data)
        
        aggregate_items = {method.name: Count(Case(When(http_method=method.value, then=Value(1)))) for method in Log.http_methods}

        top_ten = logs.values('ip_address').annotate(count=Count('id')).order_by('-count')[:10]
        for item in top_ten:
            methods_stat = logs.filter(ip_address=item['ip_address']
                ).aggregate(**aggregate_items, total_length=Sum('content_length'))
            
            item.update(methods_stat)
            data['top_ten'].append(item)        

        return Response(data)


class Pagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class LogList(QuerysetFilter, generics.ListAPIView):
    """
    Log List Data API
    """
    serializer_class = LogSerializer
    pagination_class = Pagination


