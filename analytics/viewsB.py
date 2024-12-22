from django.shortcuts import render
from .models import PageView
from django.db.models import Sum, Count
from django.utils import timezone

def analytics_dashboard(request):
    # Fetch total views
    total_views = PageView.objects.aggregate(total_views=Sum('view_count'))['total_views']
    
    # Count unique visitors (distinct IPs)
    unique_visitors = PageView.objects.values('ip_address').distinct().count()
    
    # Top 5 pages based on view count
    top_pages = PageView.objects.values('page_requested').annotate(page_views=Sum('view_count')).order_by('-page_views')[:5]
    
    # Top 5 referrers
    referrers = PageView.objects.values('referrer').annotate(referrer_count=Count('referrer')).order_by('-referrer_count')[:5]
    
    # Get country labels and visitor counts
    countries = PageView.objects.values('country').annotate(visitor_count=Count('id')).order_by('-visitor_count')
    country_labels = [country['country'] for country in countries]
    country_counts = [country['visitor_count'] for country in countries]
    
    # Views per day (grouped by date)
    views_per_day_data = PageView.objects.values('viewed_at__date').annotate(total_views=Sum('view_count')).order_by('viewed_at__date')
    views_per_day_labels = [entry['viewed_at__date'].strftime('%Y-%m-%d') for entry in views_per_day_data]
    views_per_day_data_values = [entry['total_views'] for entry in views_per_day_data]
    
    # Top 5 devices (using 'browser' as a proxy for device)
    devices = PageView.objects.values('browser').annotate(device_count=Count('browser')).order_by('-device_count')[:5]
    device_labels = [device['browser'] for device in devices]
    device_counts = [device['device_count'] for device in devices]
    
    # Top 5 operating systems
    operating_systems = PageView.objects.values('operating_system').annotate(os_count=Count('operating_system')).order_by('-os_count')[:5]
    os_labels = [os['operating_system'] for os in operating_systems]
    os_counts = [os['os_count'] for os in operating_systems]
    
    # New: Top 5 cities based on views
    cities = PageView.objects.values('city').annotate(city_count=Count('city')).order_by('-city_count')[:5]
    city_labels = [city['city'] for city in cities]
    city_counts = [city['city_count'] for city in cities]
    
    # New: Top 5 regions based on views
    regions = PageView.objects.values('region').annotate(region_count=Count('region')).order_by('-region_count')[:5]
    region_labels = [region['region'] for region in regions]
    region_counts = [region['region_count'] for region in regions]
    
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
        'browser_labels': device_labels,  # Reused browser data as labels
        'browser_counts': device_counts,  # Reused browser data as counts
        'os_labels': os_labels,
        'os_counts': os_counts,
        'city_labels': city_labels,
        'city_counts': city_counts,
        'region_labels': region_labels,
        'region_counts': region_counts,
    }

    return render(request, 'analytics/dashboard.html', context)
