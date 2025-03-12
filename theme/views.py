from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'theme/index.html')



def home1(request):
    return render(request, 'theme/home1.html')





def finderListings(request):


    person_list_category_slug = ['medecin', 'avocat']

    #filter listing excluding those with category in person_list_category_slug
    listings = Listing.objects.exclude(category__slug__in=person_list_category_slug)
    

    context = {
        'listings': listings
    }
  
    return render(request, 'listing/finder/finder-city.html', context)



def home2(request):
    person_list_category_slug = ['medecin', 'avocat']

    #filter listing excluding those with category in person_list_category_slug
    listings = Listing.objects.exclude(category__slug__in=person_list_category_slug)
    

    context = {
        'listings': listings
    }
    return render(request, 'theme/home2.html', context)



from listing.models import Listing
#from .forms import ListingForm, BusinessHoursFormSet



# def finderPeoples(request):



#     context = {
#         'listings': listings
#     }
  
#     return render(request, 'listing/finder/finder-doctors.html', context)

def home3(request):

    person_list_category_slug = ['medecin', 'avocat']

    #filter just listing with category in person_list_category_slug
    listings = Listing.objects.filter(category__slug__in=person_list_category_slug)

    return render(request, 'theme/home3.html', {'listings': listings})
