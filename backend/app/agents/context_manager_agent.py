from typing import List, Dict, Any, Optional, Set
from collections import defaultdict
import json
import time

class ContextManagerAgent:
    """Agent responsible for maintaining context across files and managing agent coordination."""
    
    def __init__(self):
        self.context_memory = {}
        self.function_usage_map = defaultdict(list)
        self.file_dependencies = defaultdict(set)
        self.agent_status = {
            'internal_doc_agent': 'idle',
            'library_doc_agent': 'idle',
            'context_manager_agent': 'idle'
        }
        self.analysis_progress = 0.0
    
    def update_agent_status(self, agent_name: str, status: str):
        """Update the status of a specific agent."""
        self.agent_status[agent_name] = status
    
    def update_progress(self, progress: float):
        """Update overall analysis progress."""
        self.analysis_progress = min(progress, 1.0)
    
    def build_function_usage_map(self, all_files: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Build a map of function names to files where they're used."""
        usage_map = defaultdict(list)
        
        for file_data in all_files:
            filename = file_data['filename']
            
            # Track functions defined in this file
            for func in file_data.get('functions', []):
                func_name = func['name']
                usage_map[func_name].append({
                    'file': filename,
                    'type': 'defined',
                    'line': func.get('line_number')
                })
            
            # Track imports that might indicate function usage
            imports = file_data.get('imports', [])
            for import_name in imports:
                # This is a simplified approach - in a real implementation,
                # you'd analyze actual function calls in the code
                usage_map[import_name].append({
                    'file': filename,
                    'type': 'imported',
                    'line': None
                })
        
        return dict(usage_map)
    
    def find_cross_references(self, all_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find cross-references between functions across files."""
        cross_refs = []
        function_map = self.build_function_usage_map(all_files)
        
        for func_name, usages in function_map.items():
            if len(usages) > 1:
                files_used_in = [usage['file'] for usage in usages]
                cross_refs.append({
                    'function': func_name,
                    'used_in': files_used_in,
                    'usage_types': [usage['type'] for usage in usages]
                })
        
        return cross_refs
    
    def analyze_file_dependencies(self, all_files: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
        """Analyze dependencies between files based on imports."""
        dependencies = defaultdict(set)
        
        for file_data in all_files:
            filename = file_data['filename']
            imports = file_data.get('imports', [])
            
            for import_name in imports:
                # Try to find which file this import refers to
                for other_file in all_files:
                    other_filename = other_file['filename']
                    if other_filename != filename:
                        # Check if the import might refer to this file
                        if self._import_matches_file(import_name, other_filename):
                            dependencies[filename].add(other_filename)
        
        return dict(dependencies)
    
    def _import_matches_file(self, import_name: str, filename: str) -> bool:
        """Check if an import statement might refer to a specific file."""
        # Remove file extension for comparison
        base_filename = filename.split('.')[0]
        
        # Handle different import patterns
        import_parts = import_name.split('/')
        last_part = import_parts[-1].split('.')[0]  # Remove extension if present
        
        return base_filename.lower() == last_part.lower()
    
    def generate_project_summary(self, all_files: List[Dict[str, Any]], libraries: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive project summary."""
        total_files = len(all_files)
        total_functions = sum(len(file_data.get('functions', [])) for file_data in all_files)
        
        # Count file types
        file_types = defaultdict(int)
        for file_data in all_files:
            file_type = file_data.get('file_type', 'unknown')
            file_types[file_type] += 1
        
        # Count libraries by category
        library_categories = defaultdict(int)
        for lib in libraries:
            lib_name = lib['name'].lower()
            if any(frontend_lib in lib_name for frontend_lib in ['react', 'vue', 'angular']):
                library_categories['frontend'] += 1
            elif any(backend_lib in lib_name for backend_lib in ['express', 'flask', 'fastapi']):
                library_categories['backend'] += 1
            else:
                library_categories['utility'] += 1
        
        # Generate summary
        summary_parts = [f"Project contains {total_files} files with {total_functions} functions"]
        
        if file_types:
            type_summary = ", ".join([f"{count} {file_type}" for file_type, count in file_types.items()])
            summary_parts.append(f"File types: {type_summary}")
        
        if library_categories:
            lib_summary = ", ".join([f"{count} {category}" for category, count in library_categories.items()])
            summary_parts.append(f"Libraries: {lib_summary}")
        
        return ". ".join(summary_parts) + "."
    
    def track_analysis_context(self, file_path: str, analysis_result: Dict[str, Any]):
        """Track analysis context for a specific file."""
        self.context_memory[file_path] = {
            'analysis_time': time.time(),
            'functions_count': len(analysis_result.get('functions', [])),
            'libraries_count': len(analysis_result.get('external_libraries', [])),
            'summary': analysis_result.get('summary', '')
        }
    
    def get_analysis_context(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get stored analysis context for a file."""
        return self.context_memory.get(file_path)
    
    def coordinate_agents(self, analysis_stage: str) -> Dict[str, str]:
        """Coordinate agent activities based on analysis stage."""
        if analysis_stage == "parsing":
            return {
                'internal_doc_agent': 'idle',
                'library_doc_agent': 'idle',
                'context_manager_agent': 'active'
            }
        elif analysis_stage == "internal_docs":
            return {
                'internal_doc_agent': 'active',
                'library_doc_agent': 'idle',
                'context_manager_agent': 'active'
            }
        elif analysis_stage == "library_docs":
            return {
                'internal_doc_agent': 'completed',
                'library_doc_agent': 'active',
                'context_manager_agent': 'active'
            }
        elif analysis_stage == "finalizing":
            return {
                'internal_doc_agent': 'completed',
                'library_doc_agent': 'completed',
                'context_manager_agent': 'active'
            }
        else:
            return {
                'internal_doc_agent': 'idle',
                'library_doc_agent': 'idle',
                'context_manager_agent': 'idle'
            }
    
    def get_analysis_statistics(self, all_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive analysis statistics."""
        stats = {
            'total_files': len(all_files),
            'total_functions': 0,
            'total_libraries': 0,
            'file_types': defaultdict(int),
            'average_functions_per_file': 0,
            'most_common_libraries': [],
            'cross_references_count': 0
        }
        
        # Calculate basic stats
        for file_data in all_files:
            stats['total_functions'] += len(file_data.get('functions', []))
            file_type = file_data.get('file_type', 'unknown')
            stats['file_types'][file_type] += 1
        
        # Calculate averages
        if stats['total_files'] > 0:
            stats['average_functions_per_file'] = stats['total_functions'] / stats['total_files']
        
        # Count libraries
        all_libraries = set()
        for file_data in all_files:
            for lib in file_data.get('external_libraries', []):
                all_libraries.add(lib['name'])
        stats['total_libraries'] = len(all_libraries)
        
        # Count cross-references
        cross_refs = self.find_cross_references(all_files)
        stats['cross_references_count'] = len(cross_refs)
        
        return stats
    
    def export_context(self) -> Dict[str, Any]:
        """Export current context for debugging or persistence."""
        return {
            'context_memory': self.context_memory,
            'agent_status': self.agent_status,
            'analysis_progress': self.analysis_progress,
            'function_usage_map': dict(self.function_usage_map),
            'file_dependencies': {k: list(v) for k, v in self.file_dependencies.items()}
        }
    
    def clear_context(self):
        """Clear all stored context."""
        self.context_memory.clear()
        self.function_usage_map.clear()
        self.file_dependencies.clear()
        self.analysis_progress = 0.0
        for agent in self.agent_status:
            self.agent_status[agent] = 'idle' 