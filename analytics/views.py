# # analytics/views.py
# from django.shortcuts import render
# from django.db.models import Count
# from .models import PageView
# from django.utils import timezone
# from django.db.models.functions import TruncDate
# from django.core.serializers.json import DjangoJSONEncoder
# import json

# def analytics_dashboard(request):
#     # Total views count
#     total_views = PageView.objects.count()

#     # Unique visitors by IP address
#     unique_visitors = PageView.objects.values('ip_address').distinct().count()

#     # Most visited pages (top 5 pages)
#     top_pages = (
#         PageView.objects.values('page_requested')
#         .annotate(view_count=Count('page_requested'))
#         .order_by('-view_count')[:10]
#     )

#         # Referrers
#     # referrers = (
#     #     PageView.objects.values('referrer')
#     #     .annotate(visitor_count=Count('referrer'))
#     #     .order_by('-visitor_count')[:5]
#     # )
#     # Utilisation de 'hostname' comme alternative
#     referrers = (
#         PageView.objects.values('hostname')
#         .annotate(visitor_count=Count('hostname'))
#         .order_by('-visitor_count')[:5]
#     )

#     # Visitors by country
#     countries = (
#         PageView.objects.values('country')
#         .annotate(visitor_count=Count('country'))
#         .order_by('-visitor_count')
#     )

#     # Browsers
#     browsers = (
#         PageView.objects.values('browser')
#         .annotate(visitor_count=Count('browser'))
#         .order_by('-visitor_count')
#     )

#     # Operating Systems
#     operating_systems = (
#         PageView.objects.values('operating_system')
#         .annotate(visitor_count=Count('operating_system'))
#         .order_by('-visitor_count')
#     )

#     # Views per day
#     views_per_day = (
#         PageView.objects
#         .annotate(day=TruncDate('viewed_at'))
#         .values('day')
#         .annotate(view_count=Count('id'))
#         .order_by('day')
#     )

#     # Prepare data for the JavaScript chart in the template
#     labels = [view['day'].strftime('%Y-%m-%d') for view in views_per_day]
#     data = [view['view_count'] for view in views_per_day]


  

#     # Serialize labels and data to JSON
#     context = {
#         'total_views': total_views,
#         'unique_visitors': unique_visitors,
#         'top_pages': top_pages,
#         'referrers': referrers,
#         'countries': countries,
#         'browsers': browsers,
#         'operating_systems': operating_systems,
#         'views_per_day_labels': json.dumps(labels, cls=DjangoJSONEncoder),
#         'views_per_day_data': json.dumps(data, cls=DjangoJSONEncoder),
#     }

#     # Render the template with the context
#     return render(request, 'analytics/dashboard.html', context)

# analytics/views.py
# from django.shortcuts import render
# from django.db.models import Count
# from .models import PageView
# from django.utils import timezone
# from django.db.models.functions import TruncDate
# from django.core.serializers.json import DjangoJSONEncoder
# import json
# import requests

# def analytics_dashboard(request):
#     # Total views count
#     total_views = PageView.objects.count()

#     # Unique visitors by IP address
#     unique_visitors = PageView.objects.values('ip_address').distinct().count()

#     # Most visited pages (top 10 pages)
#     top_pages = (
#         PageView.objects.values('page_requested')
#         .annotate(view_count=Count('page_requested'))
#         .order_by('-view_count')[:10]
#     )

#     # Referrers
#     referrers = (
#         PageView.objects.values('hostname')
#         .annotate(visitor_count=Count('hostname'))
#         .order_by('-visitor_count')[:5]
#     )

#     # Visitors by country
#     countries = (
#         PageView.objects.values('country')
#         .annotate(visitor_count=Count('country'))
#         .order_by('-visitor_count')
#     )

#     # Fetch additional country details from the REST Countries API
#     try:
#         response = requests.get("https://restcountries.com/v3.1/all")
#         response.raise_for_status()
#         country_data_api = response.json()
#     except requests.RequestException:
#         country_data_api = []  # Fallback to empty if the API call fails

#     # Map country details (flags and regions) to the country names
#     country_details = {}
#     for country in country_data_api:
#         name = country.get("name", {}).get("common")
#         if name:
#             country_details[name] = {
#                 "flag": country.get("flags", {}).get("png", ""),  # Flag image URL
#                 "region": country.get("region", ""),              # Region (e.g., Asia, Europe)
#             }

#     # Enhance countries data with additional details
#     enhanced_countries = []
#     for country in countries:
#         name = country["country"]
#         details = country_details.get(name, {})
#         enhanced_countries.append({
#             "country": name,
#             "visitor_count": country["visitor_count"],
#             "flag": details.get("flag", ""),
#             "region": details.get("region", "Unknown"),
#         })

#     # Browsers
#     browsers = (
#         PageView.objects.values('browser')
#         .annotate(visitor_count=Count('browser'))
#         .order_by('-visitor_count')
#     )

#     # Operating Systems
#     operating_systems = (
#         PageView.objects.values('operating_system')
#         .annotate(visitor_count=Count('operating_system'))
#         .order_by('-visitor_count')
#     )

#     # Views per day
#     views_per_day = (
#         PageView.objects
#         .annotate(day=TruncDate('viewed_at'))
#         .values('day')
#         .annotate(view_count=Count('id'))
#         .order_by('day')
#     )

#     # Prepare data for the JavaScript chart in the template
#     labels = [view['day'].strftime('%Y-%m-%d') for view in views_per_day]
#     data = [view['view_count'] for view in views_per_day]

#     # Serialize labels and data to JSON
#     context = {
#         'total_views': total_views,
#         'unique_visitors': unique_visitors,
#         'top_pages': top_pages,
#         'referrers': referrers,
#         'countries': enhanced_countries,  # Use the enhanced country data
#         'browsers': browsers,
#         'operating_systems': operating_systems,
#         'views_per_day_labels': json.dumps(labels, cls=DjangoJSONEncoder),
#         'views_per_day_data': json.dumps(data, cls=DjangoJSONEncoder),
#     }

#     # Render the template with the context
#     return render(request, 'analytics/dashboard.html', context)


from django.shortcuts import render
from .models import PageView
from django.db.models import Sum, Count

def analytics_dashboard(request):
    # Fetch total views (sum of all view counts)
    total_views = PageView.objects.aggregate(total_views=Sum('view_count'))['total_views'] or 0
    
    # Count unique visitors (distinct IPs)
    unique_visitors = PageView.objects.values('ip_address').distinct().count()
    
    # Top 5 pages based on view count
    top_pages = PageView.objects.values('page_requested') \
                                .annotate(page_views=Sum('view_count')) \
                                .order_by('-page_views')[:5]
    
    # Top 5 referrers
    referrers = PageView.objects.values('referrer') \
                                .annotate(referrer_count=Count('referrer')) \
                                .order_by('-referrer_count')[:5]
    
    # Get country labels and visitor counts
    countries = PageView.objects.values('country') \
                                .annotate(visitor_count=Count('id')) \
                                .order_by('-visitor_count')
    country_labels = [country['country'] for country in countries]
    country_counts = [country['visitor_count'] for country in countries]
    
    # Views per day (grouped by date)
    views_per_day_data = PageView.objects.values('viewed_at__date') \
                                         .annotate(total_views=Sum('view_count')) \
                                         .order_by('viewed_at__date')
    views_per_day_labels = [entry['viewed_at__date'].strftime('%Y-%m-%d') for entry in views_per_day_data]
    views_per_day_data_values = [entry['total_views'] for entry in views_per_day_data]
    
    # Top 5 devices (replace 'device' with 'browser' field if necessary)
    devices = PageView.objects.values('browser') \
                              .annotate(device_count=Count('browser')) \
                              .order_by('-device_count')[:5]
    device_labels = [device['browser'] for device in devices]
    device_counts = [device['device_count'] for device in devices]
    
    # Top 5 browsers
    browsers = PageView.objects.values('browser') \
                               .annotate(browser_count=Count('browser')) \
                               .order_by('-browser_count')[:5]
    browser_labels = [browser['browser'] for browser in browsers]
    browser_counts = [browser['browser_count'] for browser in browsers]
    
    # Top 5 operating systems
    operating_systems = PageView.objects.values('operating_system') \
                                        .annotate(os_count=Count('operating_system')) \
                                        .order_by('-os_count')[:5]
    os_labels = [os['operating_system'] for os in operating_systems]
    os_counts = [os['os_count'] for os in operating_systems]
    
    context = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'top_pages': top_pages,
        'referrers': referrers,
        'country_labels': country_labels,
        'country_counts': country_counts,
        'views_per_day_labels': views_per_day_labels,
        'views_per_day_data': views_per_day_data_values,
        'device_labels': device_labels,
        'device_counts': device_counts,
        'browser_labels': browser_labels,
        'browser_counts': browser_counts,
        'os_labels': os_labels,
        'os_counts': os_counts
    }

    return render(request, 'analytics/dashboard.html', context)

