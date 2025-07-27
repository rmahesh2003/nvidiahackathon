import requests
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import re
import json

class LibraryDocAgent:
    """Agent responsible for identifying external libraries and fetching their documentation."""
    
    def __init__(self):
        self.npm_base_url = "https://www.npmjs.com/package/"
        self.pypi_base_url = "https://pypi.org/project/"
        self.mdn_base_url = "https://developer.mozilla.org/en-US/docs/Web/"
        
        # Common library documentation mappings
        self.library_docs = {
            # JavaScript/React libraries
            'react': {
                'name': 'React',
                'doc_summary': 'A JavaScript library for building user interfaces',
                'link': 'https://reactjs.org/docs/getting-started.html'
            },
            'lodash': {
                'name': 'Lodash',
                'doc_summary': 'A modern JavaScript utility library',
                'link': 'https://lodash.com/docs'
            },
            'axios': {
                'name': 'Axios',
                'doc_summary': 'Promise-based HTTP client for the browser and node.js',
                'link': 'https://axios-http.com/docs/intro'
            },
            'express': {
                'name': 'Express',
                'doc_summary': 'Fast, unopinionated, minimalist web framework for Node.js',
                'link': 'https://expressjs.com/'
            },
            
            # Python libraries
            'requests': {
                'name': 'Requests',
                'doc_summary': 'Python HTTP library for making API calls',
                'link': 'https://requests.readthedocs.io/en/latest/'
            },
            'pandas': {
                'name': 'Pandas',
                'doc_summary': 'Data manipulation and analysis library',
                'link': 'https://pandas.pydata.org/docs/'
            },
            'numpy': {
                'name': 'NumPy',
                'doc_summary': 'Fundamental package for scientific computing',
                'link': 'https://numpy.org/doc/'
            },
            'flask': {
                'name': 'Flask',
                'doc_summary': 'Lightweight web application framework',
                'link': 'https://flask.palletsprojects.com/'
            },
            'fastapi': {
                'name': 'FastAPI',
                'doc_summary': 'Modern, fast web framework for building APIs',
                'link': 'https://fastapi.tiangolo.com/'
            }
        }
    
    def analyze_libraries(self, all_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze all files and extract external library information."""
        all_libraries = []
        library_map = {}
        
        for file_data in all_files:
            imports = file_data.get('imports', [])
            for import_name in imports:
                # Clean the import name
                clean_name = self._clean_import_name(import_name)
                if clean_name and clean_name not in library_map:
                    library_info = self._get_library_info(clean_name)
                    if library_info:
                        library_map[clean_name] = library_info
        
        return list(library_map.values())
    
    def _clean_import_name(self, import_name: str) -> Optional[str]:
        """Clean and extract the base library name from import statement."""
        if not import_name:
            return None
        
        # Remove common prefixes and suffixes
        clean_name = import_name.lower()
        
        # Handle scoped packages (e.g., @angular/core -> angular)
        if clean_name.startswith('@'):
            parts = clean_name.split('/')
            if len(parts) > 1:
                clean_name = parts[1]
            else:
                clean_name = parts[0][1:]  # Remove @
        
        # Remove file extensions and paths
        clean_name = clean_name.split('/')[-1]  # Get last part
        clean_name = clean_name.split('.')[0]   # Remove extension
        
        # Remove common suffixes
        suffixes_to_remove = ['-js', '-jsx', '-ts', '-tsx', '-react']
        for suffix in suffixes_to_remove:
            if clean_name.endswith(suffix):
                clean_name = clean_name[:-len(suffix)]
        
        return clean_name if clean_name else None
    
    def _get_library_info(self, library_name: str) -> Optional[Dict[str, Any]]:
        """Get library information from various sources."""
        
        # Check our predefined library docs first
        if library_name in self.library_docs:
            return self.library_docs[library_name]
        
        # Try to fetch from npm (for JavaScript libraries)
        npm_info = self._fetch_npm_info(library_name)
        if npm_info:
            return npm_info
        
        # Try to fetch from PyPI (for Python libraries)
        pypi_info = self._fetch_pypi_info(library_name)
        if pypi_info:
            return pypi_info
        
        # Check if it's a browser API
        browser_info = self._check_browser_api(library_name)
        if browser_info:
            return browser_info
        
        # Return basic info if nothing found
        return {
            'name': library_name,
            'doc_summary': f'External library: {library_name}',
            'link': None
        }
    
    def _fetch_npm_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Fetch package information from npm registry."""
        try:
            url = f"https://registry.npmjs.org/{package_name}/latest"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data.get('name', package_name),
                    'doc_summary': data.get('description', f'NPM package: {package_name}'),
                    'link': f"{self.npm_base_url}{package_name}",
                    'version': data.get('version')
                }
        except Exception as e:
            print(f"Error fetching npm info for {package_name}: {e}")
        
        return None
    
    def _fetch_pypi_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Fetch package information from PyPI."""
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                info = data.get('info', {})
                return {
                    'name': info.get('name', package_name),
                    'doc_summary': info.get('summary', f'Python package: {package_name}'),
                    'link': info.get('home_page') or f"{self.pypi_base_url}{package_name}",
                    'version': info.get('version')
                }
        except Exception as e:
            print(f"Error fetching PyPI info for {package_name}: {e}")
        
        return None
    
    def _check_browser_api(self, api_name: str) -> Optional[Dict[str, Any]]:
        """Check if the import is a browser API."""
        browser_apis = {
            'fetch': {
                'name': 'Fetch API',
                'doc_summary': 'Web API for making HTTP requests',
                'link': 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API'
            },
            'localstorage': {
                'name': 'localStorage',
                'doc_summary': 'Web API for storing data in the browser',
                'link': 'https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage'
            },
            'sessionstorage': {
                'name': 'sessionStorage',
                'doc_summary': 'Web API for storing session data',
                'link': 'https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage'
            },
            'console': {
                'name': 'Console API',
                'doc_summary': 'Web API for browser console logging',
                'link': 'https://developer.mozilla.org/en-US/docs/Web/API/Console'
            }
        }
        
        return browser_apis.get(api_name.lower())
    
    def get_library_usage_context(self, library_name: str, file_context: str) -> str:
        """Generate context about how a library is used in the codebase."""
        # This would be enhanced with actual usage analysis
        return f"Library {library_name} is imported and used in the codebase for various functionality."
    
    def categorize_libraries(self, libraries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize libraries by type (frontend, backend, utility, etc.)."""
        categories = {
            'frontend': [],
            'backend': [],
            'utility': [],
            'testing': [],
            'build_tools': []
        }
        
        frontend_libs = ['react', 'vue', 'angular', 'jquery', 'lodash', 'axios']
        backend_libs = ['express', 'fastapi', 'flask', 'django', 'sqlalchemy']
        testing_libs = ['jest', 'mocha', 'pytest', 'unittest']
        build_libs = ['webpack', 'vite', 'rollup', 'babel']
        
        for lib in libraries:
            lib_name = lib['name'].lower()
            
            if lib_name in frontend_libs:
                categories['frontend'].append(lib)
            elif lib_name in backend_libs:
                categories['backend'].append(lib)
            elif lib_name in testing_libs:
                categories['testing'].append(lib)
            elif lib_name in build_libs:
                categories['build_tools'].append(lib)
            else:
                categories['utility'].append(lib)
        
        return categories 