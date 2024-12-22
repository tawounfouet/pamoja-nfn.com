# analytics/middleware.py

from .utils import get_ip_info
from user_agents import parse
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

from .models import PageView

class VisitorLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        ip_info = get_ip_info(ip_address)
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        
        page_requested = request.path
        
        try:
            page_view = PageView.objects.get(ip_address=ip_address, page_requested=page_requested)
            # Update last_time_viewed
            page_view.last_time_viewed = timezone.now()
            page_view.view_count += 1
            page_view.save()
        except PageView.DoesNotExist:
            PageView.objects.create(
                first_time_view=timezone.now(),  # Set first_time_view to current timestamp
                last_time_viewed=timezone.now(),  # Set last_time_viewed to current timestamp
                viewed_at=timezone.now(),

                ip_address=ip_address, 
                #hostname=request.META.get('REMOTE_HOST', ''),
                operating_system=user_agent.os.family,
                browser=user_agent.browser.family,
                page_requested=page_requested,
                view_count=1,  # Initialize view count

                # info collected with ipinfo
                hostname=ip_info["hostname"],
                city=ip_info["city"],
                region=ip_info["region"],
                country=ip_info["country"],
                loc=ip_info["loc"],
                org=ip_info["org"],
                postal=ip_info["postal"],
                timezone_info=ip_info["timezone"],
               
            )

        return None
