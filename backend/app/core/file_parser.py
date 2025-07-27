import ast
import re
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
import zipfile
import tempfile
import shutil

class FileParser:
    """Handles parsing of code files and extraction of structural information."""
    
    def __init__(self):
        self.supported_extensions = {
            '.js': 'javascript',
            '.jsx': 'react',
            '.ts': 'typescript',
            '.tsx': 'react',
            '.py': 'python',
            '.pyx': 'python'
        }
    
    def extract_zip(self, zip_path: str, extract_dir: str) -> List[str]:
        """Extract uploaded zip file and return list of code files."""
        code_files = []
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_code_file(file_path):
                    code_files.append(file_path)
        
        return code_files
    
    def _is_code_file(self, file_path: str) -> bool:
        """Check if file is a supported code file."""
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_extensions
    
    def get_file_type(self, file_path: str) -> str:
        """Get the programming language type of the file."""
        ext = Path(file_path).suffix.lower()
        return self.supported_extensions.get(ext, 'unknown')
    
    def parse_python_file(self, file_path: str) -> Dict[str, Any]:
        """Parse Python file using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line_number': node.lineno,
                        'parameters': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node) or ""
                    })
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line_number': node.lineno,
                        'docstring': ast.get_docstring(node) or ""
                    })
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'line_count': len(content.split('\n'))
            }
        except Exception as e:
            return {
                'functions': [],
                'classes': [],
                'imports': [],
                'line_count': 0,
                'error': str(e)
            }
    
    def parse_javascript_file(self, file_path: str) -> Dict[str, Any]:
        """Parse JavaScript/React file using regex patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            functions = []
            imports = []
            
            # Extract function declarations
            function_pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
            arrow_function_pattern = r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
            method_pattern = r'(\w+)\s*\([^)]*\)\s*{'
            
            # Find regular functions
            for match in re.finditer(function_pattern, content):
                functions.append({
                    'name': match.group(1),
                    'parameters': [p.strip() for p in match.group(2).split(',') if p.strip()],
                    'type': 'function'
                })
            
            # Find arrow functions
            for match in re.finditer(arrow_function_pattern, content):
                functions.append({
                    'name': match.group(1),
                    'parameters': [],
                    'type': 'arrow_function'
                })
            
            # Find method-like patterns
            for match in re.finditer(method_pattern, content):
                functions.append({
                    'name': match.group(1),
                    'parameters': [],
                    'type': 'method'
                })
            
            # Extract imports
            import_patterns = [
                r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
                r'require\s*\(\s*[\'"]([^\'"]+)[\'"]',
                r'import\s+[\'"]([^\'"]+)[\'"]'
            ]
            
            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    imports.append(match.group(1))
            
            return {
                'functions': functions,
                'imports': list(set(imports)),
                'line_count': len(content.split('\n'))
            }
        except Exception as e:
            return {
                'functions': [],
                'imports': [],
                'line_count': 0,
                'error': str(e)
            }
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse file based on its type."""
        file_type = self.get_file_type(file_path)
        
        if file_type == 'python':
            return self.parse_python_file(file_path)
        elif file_type in ['javascript', 'react', 'typescript']:
            return self.parse_javascript_file(file_path)
        else:
            return {
                'functions': [],
                'imports': [],
                'line_count': 0,
                'error': f'Unsupported file type: {file_type}'
            }
    
    def get_file_summary(self, file_path: str, parsed_data: Dict[str, Any]) -> str:
        """Generate a brief summary of the file."""
        file_type = self.get_file_type(file_path)
        filename = Path(file_path).name
        
        summary_parts = [f"{filename} ({file_type})"]
        
        if parsed_data.get('functions'):
            summary_parts.append(f"Contains {len(parsed_data['functions'])} functions")
        
        if parsed_data.get('classes'):
            summary_parts.append(f"Contains {len(parsed_data['classes'])} classes")
        
        if parsed_data.get('imports'):
            summary_parts.append(f"Imports {len(parsed_data['imports'])} modules")
        
        if parsed_data.get('line_count'):
            summary_parts.append(f"{parsed_data['line_count']} lines of code")
        
        return " - ".join(summary_parts) 