from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
from .models import Listing
from .forms import ListingForm, BusinessHoursFormSet

def listings(request):
    listings = Listing.objects.all()

    context = {
        'listings': listings
    }
    return render(request, 'listing/listings.html', context)

def listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    tags = listing.tags.all()
    context = {
        'listing': listing,
        'tags': tags
    }
    return render(request, 'listing/listing_details.html', context)


def createListing(request):

    form = ListingForm()
    #form = ListingForm(request.POST or None)

    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listings')
    else:
        form = ListingForm()


    context = {
        'form': form,
    }
    return render(request, 'listing/listing-form.html', context)



def updateListing(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    form = ListingForm(request.POST or None, instance=listing)

    if form.is_valid():
        form.save()
        return redirect('listings')

    context = {
        'form': form,
    }
    return render(request, 'listing/listing-form.html', context)



def deleteListing(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if request.method == 'POST':
        listing.delete()
        return redirect('listings')

    context = {
        'listing': listing
    }
    return render(request, 'listing/listing-delete.html', context)


# Detelte Template
def deleteListing2(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    context = {
        'object': listing
    }
    return render(request, 'listing/delete_template.html', context= context)


def createListing2(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        business_hours_formset = BusinessHoursFormSet(request.POST)
        
        if form.is_valid() and business_hours_formset.is_valid():
            listing = form.save()
            business_hours = business_hours_formset.save(commit=False)
            for bh in business_hours:
                bh.listing = listing
                bh.save()
            return redirect('listings')
    else:
        form = ListingForm()
        business_hours_formset = BusinessHoursFormSet()

    context = {
        'form': form,
        'business_hours_formset': business_hours_formset,
    }
    return render(request, 'listing/listing-create.html', context)