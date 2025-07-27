from typing import List, Dict, Any, Optional
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re

class MockNeMoLLM(LLM):
    """Mock NeMo LLM for hackathon demo - replace with actual NeMo integration"""
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Mock LLM response for code documentation generation."""
        
        # Simple rule-based responses for demo
        if "function" in prompt.lower() and "document" in prompt.lower():
            return self._generate_function_doc(prompt)
        elif "summary" in prompt.lower():
            return self._generate_file_summary(prompt)
        else:
            return "This function performs the specified operation."
    
    def _generate_function_doc(self, prompt: str) -> str:
        """Generate function documentation based on function name and context."""
        # Extract function name from prompt
        func_match = re.search(r'function\s+(\w+)', prompt)
        if func_match:
            func_name = func_match.group(1)
            
            # Simple rule-based documentation
            if "handle" in func_name.lower():
                return f"Handles user interaction for {func_name.replace('handle', '').lower()}"
            elif "get" in func_name.lower():
                return f"Retrieves {func_name.replace('get', '').lower()} data"
            elif "set" in func_name.lower():
                return f"Sets {func_name.replace('set', '').lower()} value"
            elif "validate" in func_name.lower():
                return f"Validates {func_name.replace('validate', '').lower()} input"
            else:
                return f"Executes {func_name} operation"
        
        return "Performs the specified function operation."
    
    def _generate_file_summary(self, prompt: str) -> str:
        """Generate file summary based on content analysis."""
        if "react" in prompt.lower() or "jsx" in prompt.lower():
            return "React component that renders user interface elements"
        elif "python" in prompt.lower():
            return "Python module containing utility functions and classes"
        elif "javascript" in prompt.lower():
            return "JavaScript module with interactive functionality"
        else:
            return "Code file with various functions and utilities"
    
    @property
    def _llm_type(self) -> str:
        return "mock_nemo"

class InternalDocAgent:
    """Agent responsible for analyzing code structure and generating internal documentation."""
    
    def __init__(self):
        self.llm = MockNeMoLLM()
        self.function_doc_prompt = PromptTemplate(
            input_variables=["function_name", "parameters", "context"],
            template="""
            Analyze this function and generate clear documentation:
            
            Function: {function_name}
            Parameters: {parameters}
            Context: {context}
            
            Generate a concise description of what this function does:
            """
        )
        
        self.file_summary_prompt = PromptTemplate(
            input_variables=["filename", "functions", "imports", "file_type"],
            template="""
            Analyze this code file and provide a summary:
            
            File: {filename}
            Type: {file_type}
            Functions: {functions}
            Imports: {imports}
            
            Provide a brief summary of this file's purpose:
            """
        )
    
    def analyze_file(self, file_path: str, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single file and generate documentation."""
        filename = file_path.split('/')[-1]
        file_type = self._get_file_type(filename)
        
        # Generate file summary
        file_summary = self._generate_file_summary(filename, parsed_data, file_type)
        
        # Generate function documentation
        functions = []
        for func in parsed_data.get('functions', []):
            func_doc = self._generate_function_documentation(func, file_type)
            functions.append({
                'name': func['name'],
                'doc': func_doc,
                'parameters': func.get('parameters', []),
                'returns': self._infer_return_type(func, file_type),
                'line_number': func.get('line_number')
            })
        
        return {
            'filename': filename,
            'summary': file_summary,
            'functions': functions,
            'file_type': file_type,
            'line_count': parsed_data.get('line_count', 0)
        }
    
    def _get_file_type(self, filename: str) -> str:
        """Determine file type based on extension."""
        if filename.endswith('.py'):
            return 'python'
        elif filename.endswith(('.js', '.jsx')):
            return 'javascript'
        elif filename.endswith(('.ts', '.tsx')):
            return 'typescript'
        else:
            return 'unknown'
    
    def _generate_file_summary(self, filename: str, parsed_data: Dict[str, Any], file_type: str) -> str:
        """Generate a summary of the file's purpose."""
        functions = [f['name'] for f in parsed_data.get('functions', [])]
        imports = parsed_data.get('imports', [])
        
        chain = LLMChain(llm=self.llm, prompt=self.file_summary_prompt)
        
        result = chain.run({
            'filename': filename,
            'functions': ', '.join(functions),
            'imports': ', '.join(imports),
            'file_type': file_type
        })
        
        return result.strip()
    
    def _generate_function_documentation(self, func: Dict[str, Any], file_type: str) -> str:
        """Generate documentation for a specific function."""
        func_name = func['name']
        parameters = func.get('parameters', [])
        
        # Create context based on function name and parameters
        context = f"Function in {file_type} file"
        if parameters:
            context += f" with parameters: {', '.join(parameters)}"
        
        chain = LLMChain(llm=self.llm, prompt=self.function_doc_prompt)
        
        result = chain.run({
            'function_name': func_name,
            'parameters': ', '.join(parameters),
            'context': context
        })
        
        return result.strip()
    
    def _infer_return_type(self, func: Dict[str, Any], file_type: str) -> Optional[str]:
        """Infer the return type of a function based on naming patterns."""
        func_name = func['name'].lower()
        
        if file_type == 'python':
            if func_name.startswith('get_'):
                return 'Any'
            elif func_name.startswith('is_'):
                return 'bool'
            elif func_name.startswith('has_'):
                return 'bool'
            else:
                return 'Any'
        else:  # JavaScript/TypeScript
            if func_name.startsWith('get'):
                return 'any'
            elif func_name.startsWith('is'):
                return 'boolean'
            elif func_name.startsWith('has'):
                return 'boolean'
            else:
                return 'any'
    
    def find_cross_references(self, all_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find cross-references between functions across files."""
        cross_refs = []
        
        # Create a map of function names to files
        function_map = {}
        for file_data in all_files:
            filename = file_data['filename']
            for func in file_data['functions']:
                func_name = func['name']
                if func_name not in function_map:
                    function_map[func_name] = []
                function_map[func_name].append(filename)
        
        # Find functions used in multiple files
        for func_name, files in function_map.items():
            if len(files) > 1:
                cross_refs.append({
                    'function': func_name,
                    'used_in': files
                })
        
        return cross_refs 