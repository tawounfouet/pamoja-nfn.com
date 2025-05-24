from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, SubCategory, Listing, Review, Media
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ListingSerializer,
    ListingListSerializer,
    ReviewSerializer,
    MediaSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]


class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows subcategories to be viewed.
    """

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "slug"]
    filterset_fields = ["category"]


class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """

    queryset = Listing.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "description", "company_name"]
    filterset_fields = ["category", "subcategory", "type", "status"]

    def get_serializer_class(self):
        if self.action == "list":
            return ListingListSerializer
        return ListingSerializer

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        """
        Return a list of all reviews for a listing.
        """
        listing = self.get_object()
        reviews = listing.reviews.filter(is_visible=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Optionally restricts the returned listings based on query parameters.
        """
        queryset = super().get_queryset()

        # Filter to exclude specified categories
        exclude_categories = self.request.query_params.getlist("exclude_category")
        if exclude_categories:
            queryset = queryset.exclude(category__slug__in=exclude_categories)

        # Filter to include only specified categories
        include_categories = self.request.query_params.getlist("include_category")
        if include_categories:
            queryset = queryset.filter(category__slug__in=include_categories)

        # Filter based on minimum rating
        min_rating = self.request.query_params.get("min_rating", None)
        if min_rating is not None:
            queryset = queryset.filter(average_rating__gte=float(min_rating))

        # Filter based on other custom fields as needed

        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """

    queryset = Review.objects.filter(is_visible=True)
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["listing", "rating"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MediaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows media to be viewed or edited.
    """

    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["listing", "type"]
