// Example React component for fetching and displaying listings
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/listing';

const ListingsList = ({ excludeCategories = [] }) => {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchListings = async () => {
      try {
        setLoading(true);
        
        // Build URL with query parameters
        let url = `${API_URL}/listings/`;
        
        // Add category exclusion if needed
        if (excludeCategories.length > 0) {
          const excludeParams = excludeCategories.map(cat => `exclude_category=${cat}`).join('&');
          url = `${url}?${excludeParams}`;
        }
        
        const response = await axios.get(url);
        setListings(response.data.results);
        setLoading(false);
      } catch (err) {
        setError('Error fetching listings. Please try again later.');
        setLoading(false);
        console.error('Error fetching listings:', err);
      }
    };
    
    fetchListings();
  }, [excludeCategories]);
  
  if (loading) return <div>Loading listings...</div>;
  if (error) return <div className="error">{error}</div>;
  
  return (
    <div className="listings-container">
      <h2>Listings</h2>
      <div className="row">
        {listings.map(listing => (
          <div className="col-md-4" key={listing.id}>
            <div className="card mb-4">
              {listing.logo && (
                <img 
                  src={listing.logo} 
                  className="card-img-top" 
                  alt={listing.title}
                />
              )}
              <div className="card-body">
                <h5 className="card-title">{listing.title}</h5>
                <h6 className="card-subtitle mb-2 text-muted">{listing.subcategory_name}</h6>
                <p className="card-text">{listing.location}</p>
                <a href={`/listing/${listing.slug}`} className="btn btn-primary">
                  View Details
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Example usage:
const App = () => {
  // Exclude listings from 'sante' and 'avocats' categories
  return <ListingsList excludeCategories={['sante', 'avocats']} />;
};

export default ListingsList;
