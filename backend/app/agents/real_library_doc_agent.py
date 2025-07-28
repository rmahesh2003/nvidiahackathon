import requests
import re
from typing import List, Dict, Any
from bs4 import BeautifulSoup

class RealLibraryDocAgent:
    """Real LibraryDocAgent that fetches actual documentation"""
    
    def __init__(self):
        self.npm_base_url = "https://www.npmjs.com/package/"
        self.pypi_base_url = "https://pypi.org/project/"
        self.github_base_url = "https://github.com/"
        
        # Common library mappings
        self.library_mappings = {
            "lodash": {
                "name": "lodash",
                "type": "npm",
                "description": "A modern JavaScript utility library delivering modularity, performance & extras.",
                "link": "https://lodash.com/",
                "docs": "https://lodash.com/docs"
            },
            "axios": {
                "name": "axios",
                "type": "npm", 
                "description": "Promise based HTTP client for the browser and node.js",
                "link": "https://axios-http.com/",
                "docs": "https://axios-http.com/docs/intro"
            },
            "react": {
                "name": "react",
                "type": "npm",
                "description": "A JavaScript library for building user interfaces",
                "link": "https://reactjs.org/",
                "docs": "https://reactjs.org/docs/getting-started.html"
            },
            "react-dom": {
                "name": "react-dom",
                "type": "npm",
                "description": "React package for working with the DOM",
                "link": "https://reactjs.org/",
                "docs": "https://reactjs.org/docs/react-dom.html"
            }
        }
    
    def analyze_libraries(self, file_content: str) -> List[Dict[str, Any]]:
        """Analyze and fetch documentation for libraries used in the file"""
        libraries = self._extract_libraries(file_content)
        analyzed_libraries = []
        
        for lib in libraries:
            library_info = self._get_library_info(lib)
            if library_info:
                analyzed_libraries.append(library_info)
        
        return analyzed_libraries
    
    def _extract_libraries(self, content: str) -> List[str]:
        """Extract library imports from JavaScript/React code"""
        libraries = []
        
        # Pattern for import statements
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',  # import x from 'y'
            r'import\s+[\'"]([^\'"]+)[\'"]',  # import 'y'
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',  # require('y')
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                import_path = match.group(1)
                
                # Extract library name from import path
                library_name = self._extract_library_name(import_path)
                if library_name and library_name not in libraries:
                    libraries.append(library_name)
        
        return libraries
    
    def _extract_library_name(self, import_path: str) -> str:
        """Extract library name from import path"""
        # Handle scoped packages
        if import_path.startswith('@'):
            parts = import_path.split('/')
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"
        
        # Handle regular packages
        parts = import_path.split('/')
        return parts[0]
    
    def _get_library_info(self, library_name: str) -> Dict[str, Any]:
        """Get information about a library"""
        # Check our mappings first
        if library_name in self.library_mappings:
            return self.library_mappings[library_name]
        
        # Try to fetch from npm
        npm_info = self._fetch_npm_info(library_name)
        if npm_info:
            return npm_info
        
        # Try to fetch from PyPI
        pypi_info = self._fetch_pypi_info(library_name)
        if pypi_info:
            return pypi_info
        
        # Fallback
        return {
            "name": library_name,
            "type": "unknown",
            "description": f"Library: {library_name}",
            "link": f"https://www.npmjs.com/package/{library_name}",
            "docs": f"https://www.npmjs.com/package/{library_name}"
        }
    
    def _fetch_npm_info(self, package_name: str) -> Dict[str, Any]:
        """Fetch package information from npm"""
        try:
            url = f"https://registry.npmjs.org/{package_name}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                latest_version = data.get('dist-tags', {}).get('latest', '')
                version_data = data.get('versions', {}).get(latest_version, {})
                
                return {
                    "name": package_name,
                    "type": "npm",
                    "description": version_data.get('description', f'NPM package: {package_name}'),
                    "link": f"https://www.npmjs.com/package/{package_name}",
                    "docs": f"https://www.npmjs.com/package/{package_name}",
                    "version": latest_version
                }
        except Exception as e:
            print(f"Error fetching npm info for {package_name}: {e}")
        
        return None
    
    def _fetch_pypi_info(self, package_name: str) -> Dict[str, Any]:
        """Fetch package information from PyPI"""
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                info = data.get('info', {})
                
                return {
                    "name": package_name,
                    "type": "pypi",
                    "description": info.get('summary', f'PyPI package: {package_name}'),
                    "link": f"https://pypi.org/project/{package_name}/",
                    "docs": info.get('project_urls', {}).get('Documentation', f"https://pypi.org/project/{package_name}/"),
                    "version": info.get('version', '')
                }
        except Exception as e:
            print(f"Error fetching PyPI info for {package_name}: {e}")
        
        return None
    
    def get_library_summary(self, libraries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create a summary of all libraries used"""
        summary = []
        
        for lib in libraries:
            summary.append({
                "name": lib["name"],
                "usage": self._determine_usage(lib["name"]),
                "link": lib["link"],
                "docs": lib.get("docs", lib["link"]),
                "description": lib["description"]
            })
        
        return summary
    
    def _determine_usage(self, library_name: str) -> str:
        """Determine how a library is typically used"""
        usage_map = {
            "lodash": "Utility functions for data manipulation and functional programming",
            "axios": "HTTP client for making API requests",
            "react": "UI library for building component-based interfaces",
            "react-dom": "React package for DOM manipulation",
            "express": "Web application framework for Node.js",
            "moment": "Date and time manipulation library",
            "jquery": "DOM manipulation and AJAX requests",
            "bootstrap": "CSS framework for responsive design"
        }
        
        return usage_map.get(library_name, f"Library for {library_name} functionality") 