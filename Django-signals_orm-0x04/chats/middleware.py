import logging
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        This method is called when the middleware is instantiated.
        The get_response is the next middleware or view to call.
        """
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)
        
    def __call__(self, request):
        """
        This method is called for each request.
        It logs the user's request path and the timestamp.
        """
        # Get user information
        user = request.user.get_fullname if request.user.is_authenticated else 'Anonymous'
        
        # Log request data (timestamp, user, request path)
        log_message = f'{datetime.now()} - User: {user} - Path: {request.path}'
        
        # Log to the file
        with open('requests.log', 'a') as log_file:
            log_file.write(log_message + '\n')
        
        # Ensure the request continues to the next middleware/view
        response = self.get_response(request)
        
        return response  
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        """
        Initializes the middleware. This method will be called when the middleware is instantiated.
        """
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Checks the current time and restricts access to the chat outside the allowed time range (9 AM - 6 PM).
        """
        start_time = 9
        end_time = 18
        
        current_hour = datetime.now().hour # Get the current hour
        
        # If the current hour is outside the allowed range (not between 9 AM and 6 PM)
        if current_hour < start_time or current_hour >= end_time:
            # Deny access to the chats
            return HttpResponseForbidden("Access to the chat is restricted to between 9 AM and 6 PM.")
        
        # If the time is within the allowed range, continue processing the request
        response = self.get_response
        return response   

class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST requests (messages) a user can send
    within a certain time window based on their IP address.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware.
        
        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_reponse = get_response
        self.ip_requests = defaultdict(deque)
        
        # Configuration
        self.max_requests = 5  # Maximum requests allowed
        self.time_window = 60  # Time window in seconds (1 minute)  
        
    def __call__(self, request):
        """
        Track POST requests by IP address and enforce rate limits.
        
        Args:
            request: The HTTP request object
            
        Returns:
            HTTP 429 Too Many Requests if limit exceeded,
            otherwise continues with normal response
        """
        # Only apply rate limiting to POST requests (message sending)
        if request.method == 'POST':
            # Get client ip address
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            self.cleanup_old_requests(ip_address, current_time)
            
            # Check if user has exceeded the rate limit
            if len(self.ip_requests[ip_address]) >= self.max_requests:
                error_message = {
                    "error": "Rate limit exceeded",
                    "message": f"You have exceeded the maximum of {self.max_requests} messages per minute. Please wait before sending more messages.",
                    "limit": self.max_requests,
                    "time_window": "1 minute",
                    "retry_after": self.time_window
                }  
                return JsonResponse(error_message, status=429)
        # Add current request timestamp
        self.ip_requests[ip_address].append(current_time)
    
    def get_client_ip(self, request):
        """
        Extract client IP address from request, considering proxy headers.
        
        Args:
            request: The HTTP request object
            
        Returns:
            str: Client IP address
        """
        # Check for IP address in proxy headers first
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            # Take the first IP if there are multiple (in case of multiple proxies)
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            # Fall back to REMOTE_ADDR
            ip = request.META.get('REMOTE_ADDR')
            
        return ip 
    
    def cleanup_old_requests(self, ip_address, current_time):
        """
        Remove timestamps that are outside the time window.
        
        Args:
            ip_address (str): Client IP address
            current_time (float): Current timestamp in seconds
        """
        cutoff_time = current_time - self.time_window
        
        # Remove old timestamps
        while self.ip_requests[ip_address] and self.ip_requests[ip_address][0] < cutoff_time:
            self.ip_requests[ip_address].popleft()  


class RolepermissionMiddleware:
    """
    Middleware that checks the user's role (admin or moderator) before allowing access.
    Returns 403 Forbidden if the user is not admin or moderator.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        This is called once when the web server starts.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and check user roles before allowing access.
        This method is called for each request.
        """
        # Check if user is authenticated
        if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated:
            # Allow unauthenticated users to access login/register pages
            if self._is_public_view(request):
                return self.get_response(request)
            
            # Unauthorized access attempt
            return HttpResponseForbidden(
                json.dumps({
                    "error": "Authentication required",
                    "message": "You must be logged in to access this resource."
                }),
                content_type='application/json'
            )
        
        # Check user role
        user_role = self._get_user_role(request.user)
        
        # Allow only admin or moderator roles
        if user_role not in ['admin', 'moderator']:
            return HttpResponseForbidden(
                json.dumps({
                    "error": "Access denied", 
                    "message": "Admin or moderator role required.",
                    "user_role": user_role,
                    "required_roles": ["admin", "moderator"]
                }),
                content_type='application/json'
            )
        
        # If user has proper role, continue with the request
        response = self.get_response(request)
        return response
    
    def _get_user_role(self, user):
        """
        Extract user role from user object.
        Modify this method based on how roles are stored in your system.
        """
        # Option 1: If role is stored as user attribute
        if hasattr(user, 'role'):
            return user.role
        
        # Option 2: If using user groups (admin or moderator)
        if user.groups.filter(name__in=['admin', 'moderator']).exists():
            return user.groups.filter(name__in=['admin', 'moderator']).first().name.lower()
        
        # Option 3: If using user profile with role field
        if hasattr(user, 'profile') and hasattr(user.profile, 'role'):
            return user.profile.role
        
        # Option 4: Check if user is Django superuser
        if user.is_superuser:
            return 'admin'
        
        # Default: return regular user role
        return 'user'
    
    def _is_public_view(self, request):
        """
        Define which views should be accessible without role checking.
        Modify this list based on your application needs.
        """
        public_paths = [
            '/login/',
            '/register/',
            '/logout/',
            '/admin/login/',
            '/accounts/login/',
        ]
        
        # Check if current path is in public paths
        return any(request.path.startswith(path) for path in public_paths)            
                                 