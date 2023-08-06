from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_page_size(self, request):
        limit = request.query_params.get('limit')
        if limit:
            return int(limit)
        return self.page_size
