// Example React component for showing a single listing detail
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/listing';

const ListingDetail = ({ slug }) => {
  const [listing, setListing] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchListingDetail = async () => {
      try {
        setLoading(true);
        
        // First get listing ID from slug
        const listingsResponse = await axios.get(`${API_URL}/listings/?search=${slug}`);
        
        if (listingsResponse.data.results.length === 0) {
          setError('Listing not found');
          setLoading(false);
          return;
        }
        
        const listingId = listingsResponse.data.results[0].id;
        
        // Get full listing details
        const detailResponse = await axios.get(`${API_URL}/listings/${listingId}/`);
        setListing(detailResponse.data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching listing details. Please try again later.');
        setLoading(false);
        console.error('Error fetching listing details:', err);
      }
    };
    
    if (slug) {
      fetchListingDetail();
    }
  }, [slug]);
  
  if (loading) return <div>Loading listing details...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!listing) return <div>No listing found</div>;
  
  return (
    <div className="listing-detail">
      <div className="container">
        <div className="row">
          <div className="col-md-8">
            {listing.logo && (
              <img 
                src={listing.logo} 
                className="img-fluid mb-4" 
                alt={listing.title}
              />
            )}
            
            <h1>{listing.title}</h1>
            <p className="lead">{listing.category_name} &gt; {listing.subcategory_name}</p>
            
            <div className="mb-4">
              <h3>Description</h3>
              <p>{listing.description}</p>
            </div>
            
            {listing.website_url && (
              <div className="mb-4">
                <h3>Website</h3>
                <a href={listing.website_url} target="_blank" rel="noopener noreferrer">
                  {listing.website_url}
                </a>
              </div>
            )}
            
            <div className="mb-4">
              <h3>Location</h3>
              <p>{listing.location}</p>
            </div>
            
            {listing.reviews && listing.reviews.length > 0 && (
              <div className="mb-4">
                <h3>Reviews</h3>
                {listing.reviews.map(review => (
                  <div className="card mb-2" key={review.id}>
                    <div className="card-body">
                      <div className="d-flex justify-content-between">
                        <h5>{review.user_username}</h5>
                        <div>Rating: {review.rating}/5</div>
                      </div>
                      <p>{review.comment}</p>
                      <small className="text-muted">
                        Posted on {new Date(review.created_at).toLocaleDateString()}
                      </small>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="col-md-4">
            <div className="card mb-4">
              <div className="card-header">
                <h4>Contact Information</h4>
              </div>
              <div className="card-body">
                {listing.contact_details && (
                  <>
                    {listing.contact_details.mobile_phone && (
                      <p>
                        <strong>Phone:</strong> {listing.contact_details.mobile_phone}
                      </p>
                    )}
                    
                    {listing.contact_details.whatsapp_number && (
                      <p>
                        <strong>WhatsApp:</strong> {listing.contact_details.whatsapp_number}
                      </p>
                    )}
                    
                    {listing.contact_details.contact_email && (
                      <p>
                        <strong>Email:</strong> {listing.contact_details.contact_email}
                      </p>
                    )}
                  </>
                )}
                
                {listing.social_media && (
                  <div className="mt-3">
                    <h5>Social Media</h5>
                    <div className="d-flex gap-2">
                      {listing.social_media.facebook && (
                        <a href={listing.social_media.facebook} target="_blank" rel="noopener noreferrer">
                          Facebook
                        </a>
                      )}
                      
                      {listing.social_media.instagram && (
                        <a href={listing.social_media.instagram} target="_blank" rel="noopener noreferrer">
                          Instagram
                        </a>
                      )}
                      
                      {listing.social_media.twitter && (
                        <a href={listing.social_media.twitter} target="_blank" rel="noopener noreferrer">
                          Twitter
                        </a>
                      )}
                      
                      {listing.social_media.linkedin && (
                        <a href={listing.social_media.linkedin} target="_blank" rel="noopener noreferrer">
                          LinkedIn
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ListingDetail;
