# React Components for Pamoja Listings API

This directory contains example React components that demonstrate how to integrate with the Pamoja Listings API.

## Components

### ListingsList.jsx

This component fetches and displays a list of listings, with optional filtering by category.

**Props:**
- `excludeCategories`: Array of category slugs to exclude from the results (e.g., ['sante', 'avocats'])

### ListingDetail.jsx

This component displays detailed information about a single listing.

**Props:**
- `slug`: The slug of the listing to display

## Usage

1. Install required dependencies in your React project:

```bash
npm install axios react react-dom
```

2. Import and use the components:

```jsx
import React from 'react';
import ListingsList from './ListingsList';
import ListingDetail from './ListingDetail';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ListingsList excludeCategories={['sante', 'avocats']} />} />
        <Route path="/listing/:slug" element={<ListingDetailWrapper />} />
      </Routes>
    </Router>
  );
}

// Wrapper to extract slug from URL parameters
function ListingDetailWrapper() {
  const params = useParams();
  return <ListingDetail slug={params.slug} />;
}

export default App;
```

## API Configuration

These components are configured to connect to `http://localhost:8000/api/listing/`. 
If your API is hosted at a different URL, update the `API_URL` constant in each component.

## Authentication

If your API requires authentication, you'll need to modify the axios requests to include 
authentication headers. For example:

```jsx
// For token-based authentication:
const token = localStorage.getItem('auth_token');
axios.get(url, {
  headers: {
    'Authorization': `Token ${token}`
  }
})
```

## Error Handling

Both components include basic error handling. You can customize the error messages and UI as needed.
