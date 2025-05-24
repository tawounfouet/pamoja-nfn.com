from rest_framework import serializers
from .models import (
    Category,
    SubCategory,
    Listing,
    Review,
    Media,
    ContactInformation,
    SocialMediaLinks,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name", "slug", "description", "category"]


class ContactInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = [
            "mobile_phone",
            "whatsapp_number",
            "contact_email",
            "preferred_contact",
        ]


class SocialMediaLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLinks
        fields = ["facebook", "instagram", "twitter", "linkedin"]


class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ["id", "user", "user_username", "rating", "comment", "created_at"]
        read_only_fields = ["user"]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "file", "type", "title", "description", "is_primary"]


class ListingSerializer(TaggitSerializer, serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source="category.name")
    subcategory_name = serializers.ReadOnlyField(source="subcategory.name")
    contact_details = ContactInformationSerializer(read_only=True)
    social_media = SocialMediaLinksSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "slug",
            "company_name",
            "description",
            "category",
            "category_name",
            "subcategory",
            "subcategory_name",
            "type",
            "location",
            "logo",
            "website_url",
            "status",
            "average_rating",
            "contact_details",
            "social_media",
            "reviews",
            "media",
            "tags",
            "created_at",
            "updated_at",
        ]


class ListingListSerializer(serializers.ModelSerializer):
    """
    A simplified serializer for listing multiple items
    """

    category_name = serializers.ReadOnlyField(source="category.name")
    subcategory_name = serializers.ReadOnlyField(source="subcategory.name")

    class Meta:
        model = Listing
        fields = [
            "id",
            "title",
            "slug",
            "company_name",
            "logo",
            "category",
            "category_name",
            "subcategory",
            "subcategory_name",
            "location",
            "average_rating",
            "status",
        ]
