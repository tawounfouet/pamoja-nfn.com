# Pamoja Listings API

This document provides information about the RESTful API endpoints available for the Pamoja Listings application.

## Base URL

All API endpoints are accessible under:

```
http://localhost:8000/api/listing/
```

## Authentication

Most API endpoints require authentication. The API supports:

- Session authentication (for browser-based applications)
- Basic authentication (for testing purposes)

Authentication headers should be included with all requests except those that are explicitly marked as supporting anonymous access.

## Endpoints

### Categories

**GET /api/listing/categories/**

Returns a list of all categories.

Query Parameters:
- `search`: Filter categories by name or slug

Example Response:
```json
{
  "count": 13,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Activité enfants",
      "slug": "activite-enfants",
      "description": "Activities for children"
    },
    ...
  ]
}
```

**GET /api/listing/categories/{id}/**

Returns details for a specific category.

---

### Subcategories

**GET /api/listing/subcategories/**

Returns a list of all subcategories.

Query Parameters:
- `search`: Filter subcategories by name or slug
- `category`: Filter subcategories by parent category ID

Example Response:
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Arts plastiques",
      "slug": "arts-plastiques",
      "description": "Painting and crafts activities",
      "category": 1
    },
    ...
  ]
}
```

**GET /api/listing/subcategories/{id}/**

Returns details for a specific subcategory.

---

### Listings

**GET /api/listing/listings/**

Returns a list of all listings.

Query Parameters:
- `search`: Filter listings by title, description, or company name
- `category`: Filter listings by category ID
- `subcategory`: Filter listings by subcategory ID
- `type`: Filter listings by type (IND/COM)
- `status`: Filter listings by status (ACT/INA/PEN)
- `exclude_category`: Exclude listings with specified category slug(s)
- `include_category`: Include only listings with specified category slug(s)
- `min_rating`: Filter listings by minimum rating

Example Response:
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/listing/listings/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Example Listing",
      "slug": "example-listing-abc12",
      "company_name": "Example Company",
      "logo": "http://localhost:8000/media/listing_images/example.jpg",
      "category": 1,
      "category_name": "Alimentation",
      "subcategory": 3,
      "subcategory_name": "Restaurants",
      "location": "Paris, France",
      "average_rating": 4.5,
      "status": "ACT"
    },
    ...
  ]
}
```

**GET /api/listing/listings/{id}/**

Returns detailed information for a specific listing.

**GET /api/listing/listings/{id}/reviews/**

Returns all reviews for a specific listing.

---

### Reviews

**GET /api/listing/reviews/**

Returns a list of all visible reviews.

Query Parameters:
- `listing`: Filter reviews by listing ID
- `rating`: Filter reviews by rating value

Example Response:
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 5,
      "user_username": "john_doe",
      "rating": 4,
      "comment": "Great service, highly recommended!",
      "created_at": "2025-05-10T14:23:10Z"
    },
    ...
  ]
}
```

**POST /api/listing/reviews/**

Create a new review (requires authentication).

Required fields:
- `listing`: ID of the listing
- `rating`: Rating value (1-5)
- `comment`: Review text

---

### Media

**GET /api/listing/media/**

Returns a list of all media items.

Query Parameters:
- `listing`: Filter media by listing ID
- `type`: Filter media by type (IMG/DOC/VID)

Example Response:
```json
{
  "count": 30,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "file": "http://localhost:8000/media/listing_media/example.jpg",
      "type": "IMG",
      "title": "Store Front",
      "description": "Front view of the store",
      "is_primary": true
    },
    ...
  ]
}
```

## Error Handling

The API returns standard HTTP status codes:

- 200: Success
- 400: Bad Request (invalid parameters)
- 401: Unauthorized (authentication required)
- 403: Forbidden (authenticated but not authorized)
- 404: Not Found
- 500: Internal Server Error

Error responses include a detail message explaining the error.

Example error response:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

## Rate Limiting

The API currently does not implement rate limiting, but this may change in future versions.

## Pagination

All list endpoints return paginated results. The default page size is 10 items.

Pagination information is included in the response:
```json
{
  "count": 50,  // Total number of items
  "next": "http://localhost:8000/api/listing/listings/?page=2",  // URL for next page
  "previous": null,  // URL for previous page
  "results": [...]  // Current page items
}
```

You can navigate pages using the `page` query parameter.

## Example curl Commands

Get all categories:
```bash
curl -X GET http://localhost:8000/api/listing/categories/ -H "Accept: application/json"
```

Get listings excluding specific categories:
```bash
curl -X GET "http://localhost:8000/api/listing/listings/?exclude_category=sante&exclude_category=avocats" -H "Accept: application/json"
```
