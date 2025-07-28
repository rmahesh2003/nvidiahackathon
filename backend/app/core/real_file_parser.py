import zipfile
import os
import re
from typing import List, Dict, Any
import ast

class RealFileParser:
    """Real file parser that extracts and parses uploaded files"""
    
    def __init__(self):
        self.supported_extensions = ['.js', '.jsx', '.ts', '.tsx', '.py', '.pyx']
        self.extracted_files = {}
    
    def extract_zip(self, zip_file_path: str) -> Dict[str, str]:
        """Extract and parse files from a zip archive"""
        extracted_files = {}
        
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                for file_info in zip_ref.filelist:
                    filename = file_info.filename
                    
                    # Skip directories and unsupported files
                    if file_info.is_dir() or not self._is_supported_file(filename):
                        continue
                    
                    # Read file content
                    content = zip_ref.read(filename).decode('utf-8', errors='ignore')
                    extracted_files[filename] = content
                    
        except Exception as e:
            print(f"Error extracting zip file: {e}")
            return {}
        
        self.extracted_files = extracted_files
        return extracted_files
    
    def _is_supported_file(self, filename: str) -> bool:
        """Check if file is supported for analysis"""
        return any(filename.endswith(ext) for ext in self.supported_extensions)
    
    def parse_javascript_file(self, filename: str, content: str) -> Dict[str, Any]:
        """Parse JavaScript/React file"""
        functions = self._extract_js_functions(content)
        imports = self._extract_js_imports(content)
        
        return {
            "filename": filename,
            "type": "javascript",
            "functions": functions,
            "imports": imports,
            "content": content
        }
    
    def parse_python_file(self, filename: str, content: str) -> Dict[str, Any]:
        """Parse Python file"""
        functions = self._extract_python_functions(content)
        imports = self._extract_python_imports(content)
        
        return {
            "filename": filename,
            "type": "python",
            "functions": functions,
            "imports": imports,
            "content": content
        }
    
    def _extract_js_functions(self, content: str) -> List[Dict[str, str]]:
        """Extract functions from JavaScript/React code"""
        functions = []
        
        # Patterns for different function declarations
        patterns = [
            # Function declarations
            r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            # Arrow functions
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{[^}]*\}',
            # Method definitions
            r'(\w+)\s*:\s*\([^)]*\)\s*=>\s*\{[^}]*\}',
            # Function expressions
            r'(\w+)\s*:\s*function\s*\([^)]*\)\s*\{[^}]*\}'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                function_name = match.group(1)
                function_code = match.group(0)
                
                # Extract function signature
                signature = self._extract_function_signature(function_code)
                
                functions.append({
                    "name": function_name,
                    "signature": signature,
                    "code": function_code.strip()
                })
        
        return functions
    
    def _extract_python_functions(self, content: str) -> List[Dict[str, str]]:
        """Extract functions from Python code"""
        functions = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_name = node.name
                    function_code = ast.unparse(node)
                    
                    # Extract function signature
                    signature = f"def {function_name}({', '.join(arg.arg for arg in node.args.args)})"
                    
                    functions.append({
                        "name": function_name,
                        "signature": signature,
                        "code": function_code.strip()
                    })
                    
        except SyntaxError as e:
            print(f"Error parsing Python file: {e}")
        
        return functions
    
    def _extract_js_imports(self, content: str) -> List[str]:
        """Extract import statements from JavaScript/React code"""
        imports = []
        
        # Patterns for import statements
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'import\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                import_path = match.group(1)
                imports.append(import_path)
        
        return imports
    
    def _extract_python_imports(self, content: str) -> List[str]:
        """Extract import statements from Python code"""
        imports = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
                        
        except SyntaxError as e:
            print(f"Error parsing Python imports: {e}")
        
        return imports
    
    def _extract_function_signature(self, function_code: str) -> str:
        """Extract function signature from function code"""
        # Find the opening parenthesis
        start = function_code.find('(')
        if start == -1:
            return function_code
        
        # Find the closing parenthesis
        paren_count = 0
        end = start
        
        for i, char in enumerate(function_code[start:], start):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
                if paren_count == 0:
                    end = i + 1
                    break
        
        return function_code[:end]
    
    def parse_all_files(self, extracted_files: Dict[str, str]) -> List[Dict[str, Any]]:
        """Parse all extracted files"""
        parsed_files = []
        
        for filename, content in extracted_files.items():
            if filename.endswith(('.js', '.jsx', '.ts', '.tsx')):
                parsed_file = self.parse_javascript_file(filename, content)
            elif filename.endswith(('.py', '.pyx')):
                parsed_file = self.parse_python_file(filename, content)
            else:
                continue
            
            parsed_files.append(parsed_file)
        
        return parsed_files 