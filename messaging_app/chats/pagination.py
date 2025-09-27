# chats/pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20  # default: 20 messages per page
    page_size_query_param = "page_size"  # allows ?page_size=50 override
    max_page_size = 100  # prevent abuse

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,   # 👈 total messages
            "total_pages": self.page.paginator.num_pages,  # 👈 total pages
            "current_page": self.page.number,    # 👈 current page
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,   # the actual messages
        })
