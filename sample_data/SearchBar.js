import React, { useState, useCallback } from 'react';
import { debounce } from 'lodash';
import axios from 'axios';

const SearchBar = ({ onSearch, placeholder = "Search..." }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Debounced search function to limit API calls
  const debouncedSearch = useCallback(
    debounce(async (searchTerm) => {
      if (!searchTerm.trim()) {
        onSearch([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await axios.get(`/api/search?q=${encodeURIComponent(searchTerm)}`);
        onSearch(response.data.results);
      } catch (error) {
        console.error('Search failed:', error);
        onSearch([]);
      } finally {
        setIsLoading(false);
      }
    }, 300),
    [onSearch]
  );

  const handleChange = (event) => {
    const newQuery = event.target.value;
    setQuery(newQuery);
    debouncedSearch(newQuery);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    debouncedSearch.flush();
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <div className="search-input-wrapper">
        <input
          type="text"
          value={query}
          onChange={handleChange}
          placeholder={placeholder}
          className="search-input"
          disabled={isLoading}
        />
        {isLoading && (
          <div className="loading-spinner">
            <div className="spinner"></div>
          </div>
        )}
      </div>
      <button type="submit" className="search-button" disabled={isLoading}>
        Search
      </button>
    </form>
  );
};

export default SearchBar; 