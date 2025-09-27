# chats/pagination.py
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # default: 20 messages per page
    page_size_query_param = "page_size"  # allows ?page_size=50 override
    max_page_size = 100  # prevent abuse
