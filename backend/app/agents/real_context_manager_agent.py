import re
from typing import List, Dict, Any, Set
from datetime import datetime

class RealContextManagerAgent:
    """Real ContextManagerAgent with status tracking and cross-references"""
    
    def __init__(self):
        self.analysis_status = {}
        self.file_contents = {}
        self.cross_references = []
        self.project_summary = ""
        self.external_libraries = []
    
    def update_status(self, upload_id: str, status: str, progress: int = 0, message: str = ""):
        """Update analysis status"""
        if upload_id not in self.analysis_status:
            self.analysis_status[upload_id] = {}
        
        self.analysis_status[upload_id].update({
            "status": status,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_status(self, upload_id: str) -> Dict[str, Any]:
        """Get current analysis status"""
        return self.analysis_status.get(upload_id, {
            "status": "not_found",
            "progress": 0,
            "message": "Upload not found"
        })
    
    def store_file_content(self, filename: str, content: str):
        """Store file content for cross-reference analysis"""
        self.file_contents[filename] = content
    
    def find_cross_references(self) -> List[Dict[str, Any]]:
        """Find cross-references between files"""
        cross_refs = []
        
        for filename, content in self.file_contents.items():
            # Find import statements
            import_patterns = [
                r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',  # import x from 'y'
                r'import\s+[\'"]([^\'"]+)[\'"]',  # import 'y'
                r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',  # require('y')
            ]
            
            for pattern in import_patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    import_path = match.group(1)
                    
                    # Check if it's a local import
                    if import_path.startswith('./') or import_path.startswith('../'):
                        imported_file = self._resolve_import_path(filename, import_path)
                        if imported_file and imported_file in self.file_contents:
                            cross_refs.append({
                                "from": filename,
                                "to": imported_file,
                                "type": "import",
                                "description": f"{filename} imports {imported_file}"
                            })
        
        self.cross_references = cross_refs
        return cross_refs
    
    def _resolve_import_path(self, current_file: str, import_path: str) -> str:
        """Resolve relative import path to actual filename"""
        if import_path.startswith('./'):
            # Same directory
            base_dir = '/'.join(current_file.split('/')[:-1])
            filename = import_path[2:]  # Remove './'
            if not filename.endswith('.js'):
                filename += '.js'
            return f"{base_dir}/{filename}" if base_dir else filename
        elif import_path.startswith('../'):
            # Parent directory
            parts = current_file.split('/')
            if len(parts) > 1:
                parts.pop()  # Remove current file
                parts.pop()  # Remove current directory
                filename = import_path[3:]  # Remove '../'
                if not filename.endswith('.js'):
                    filename += '.js'
                return '/'.join(parts + [filename])
        
        return None
    
    def generate_project_summary(self, files: List[Dict[str, Any]]) -> str:
        """Generate comprehensive project summary"""
        if not files:
            return "No files analyzed"
        
        # Count files by type
        file_types = {}
        total_functions = 0
        total_libraries = set()
        
        for file_info in files:
            file_ext = file_info.get('filename', '').split('.')[-1]
            file_types[file_ext] = file_types.get(file_ext, 0) + 1
            
            # Count functions
            functions = file_info.get('functions', [])
            total_functions += len(functions)
            
            # Collect libraries
            libraries = file_info.get('external_libraries', [])
            for lib in libraries:
                total_libraries.add(lib.get('name', ''))
        
        # Generate summary
        summary_parts = []
        
        if len(files) == 1:
            summary_parts.append(f"Single {file_types.get('js', 'JavaScript')} file")
        else:
            summary_parts.append(f"{len(files)} files")
        
        if total_functions > 0:
            summary_parts.append(f"with {total_functions} functions")
        
        if total_libraries:
            summary_parts.append(f"using {len(total_libraries)} external libraries")
        
        # Add specific details based on content
        if any('react' in str(file).lower() for file in files):
            summary_parts.append("React application")
        
        if any('search' in str(file).lower() for file in files):
            summary_parts.append("with search functionality")
        
        if any('debounce' in str(file).lower() for file in files):
            summary_parts.append("including debounced input handling")
        
        summary = " ".join(summary_parts)
        self.project_summary = summary
        return summary
    
    def build_function_usage_map(self, files: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build a map of function usage across files"""
        usage_map = {}
        
        for file_info in files:
            filename = file_info.get('filename', '')
            functions = file_info.get('functions', [])
            
            for func in functions:
                func_name = func.get('name', '')
                if func_name:
                    if func_name not in usage_map:
                        usage_map[func_name] = []
                    usage_map[func_name].append(filename)
        
        return usage_map
    
    def analyze_code_complexity(self, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze code complexity metrics"""
        total_lines = 0
        total_functions = 0
        total_imports = 0
        
        for file_info in files:
            filename = file_info.get('filename', '')
            content = self.file_contents.get(filename, '')
            
            if content:
                lines = content.split('\n')
                total_lines += len(lines)
                
                # Count functions
                functions = file_info.get('functions', [])
                total_functions += len(functions)
                
                # Count imports
                import_matches = re.findall(r'import\s+|require\s*\(', content)
                total_imports += len(import_matches)
        
        return {
            "total_files": len(files),
            "total_lines": total_lines,
            "total_functions": total_functions,
            "total_imports": total_imports,
            "average_lines_per_file": total_lines / len(files) if files else 0,
            "average_functions_per_file": total_functions / len(files) if files else 0
        }
    
    def get_comprehensive_analysis(self, upload_id: str) -> Dict[str, Any]:
        """Get comprehensive analysis results"""
        return {
            "project_summary": self.project_summary,
            "analysis_status": self.get_status(upload_id),
            "cross_references": self.cross_references,
            "complexity_metrics": self.analyze_code_complexity([]),  # Will be populated with actual files
            "external_libraries_summary": self.external_libraries,
            "timestamp": datetime.now().isoformat()
        } 