// Utility functions for the search application

/**
 * Formats a date string into a readable format
 * @param {string} dateString - ISO date string
 * @returns {string} Formatted date string
 */
export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

/**
 * Truncates text to a specified length
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

/**
 * Validates search query
 * @param {string} query - Search query to validate
 * @returns {boolean} Whether the query is valid
 */
export const validateSearchQuery = (query) => {
  if (!query || typeof query !== 'string') return false;
  if (query.trim().length < 2) return false;
  return true;
};

/**
 * Filters results based on search criteria
 * @param {Array} results - Array of search results
 * @param {string} query - Search query
 * @returns {Array} Filtered results
 */
export const filterResults = (results, query) => {
  if (!query || !results) return results;
  
  const lowerQuery = query.toLowerCase();
  return results.filter(result => 
    result.title.toLowerCase().includes(lowerQuery) ||
    result.description.toLowerCase().includes(lowerQuery)
  );
};

/**
 * Sorts results by relevance
 * @param {Array} results - Array of search results
 * @param {string} query - Search query
 * @returns {Array} Sorted results
 */
export const sortByRelevance = (results, query) => {
  if (!query || !results) return results;
  
  const lowerQuery = query.toLowerCase();
  
  return results.sort((a, b) => {
    const aTitleMatch = a.title.toLowerCase().includes(lowerQuery);
    const bTitleMatch = b.title.toLowerCase().includes(lowerQuery);
    
    // Prioritize title matches
    if (aTitleMatch && !bTitleMatch) return -1;
    if (!aTitleMatch && bTitleMatch) return 1;
    
    // Then sort by date (newer first)
    return new Date(b.date) - new Date(a.date);
  });
}; 