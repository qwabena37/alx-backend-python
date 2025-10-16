# messaging_app/chats/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20 
    page_size_query_param = 'page_size'  
    max_page_size = 100 
    
    def get_paginated_response(self, data):
        """
        This method will return the paginated data along with the total count of messages.
        """
        return Response({
            'count': self.page.paginator.count,  # Total number of messages
            'next': self.get_next_link(),  # Link to the next page of results (if any)
            'previous': self.get_previous_link(),  # Link to the previous page (if any)
            'results': data  # The actual message results for the current page
        })