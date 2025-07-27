import React, { useState } from 'react';
import SearchBar from './SearchBar';

const SearchResults = () => {
  const [results, setResults] = useState([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = (searchResults) => {
    setResults(searchResults);
    setHasSearched(true);
  };

  const renderResult = (result, index) => (
    <div key={index} className="search-result-item">
      <h3 className="result-title">{result.title}</h3>
      <p className="result-description">{result.description}</p>
      <div className="result-meta">
        <span className="result-type">{result.type}</span>
        <span className="result-date">{result.date}</span>
      </div>
    </div>
  );

  return (
    <div className="search-results-container">
      <SearchBar onSearch={handleSearch} placeholder="Search for documents..." />
      
      <div className="results-section">
        {!hasSearched ? (
          <div className="empty-state">
            <p>Enter a search term to find documents</p>
          </div>
        ) : results.length === 0 ? (
          <div className="no-results">
            <p>No results found. Try a different search term.</p>
          </div>
        ) : (
          <div className="results-list">
            <h2 className="results-count">
              Found {results.length} result{results.length !== 1 ? 's' : ''}
            </h2>
            {results.map(renderResult)}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchResults; 