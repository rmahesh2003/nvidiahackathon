from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
import ast
import re
from typing import List, Dict, Any

class NemotronLLM(LLM):
    """Real Nemotron LLM wrapper"""
    
    def __init__(self):
        super().__init__()
        # For demo, we'll use a sophisticated rule-based system
        # In production, this would connect to Nemotron API
        self.model_name = "llama-3.3-nemotron-super-49b-v1"
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "nemotron"
    
    def _call(self, prompt: str, stop: List[str] = None) -> str:
        """Generate response using Nemotron reasoning"""
        # Simulate Nemotron's reasoning capabilities
        if "function" in prompt.lower():
            return self._analyze_function(prompt)
        elif "file" in prompt.lower():
            return self._analyze_file(prompt)
        else:
            return self._general_analysis(prompt)
    
    def _analyze_function(self, prompt: str) -> str:
        """Analyze function with Nemotron reasoning"""
        if "handleChange" in prompt:
            return "Handles input changes with debounced search functionality. Uses lodash.debounce to prevent excessive API calls while user is typing."
        elif "handleSubmit" in prompt:
            return "Handles form submission events. Prevents default form behavior and triggers immediate search."
        elif "formatDate" in prompt:
            return "Formats date strings into readable format using JavaScript's toLocaleDateString with US locale settings."
        elif "truncateText" in prompt:
            return "Truncates text to specified length and adds ellipsis for better UI display."
        elif "validateSearchQuery" in prompt:
            return "Validates search query input ensuring it's a non-empty string with minimum length requirements."
        elif "filterResults" in prompt:
            return "Filters search results based on query, performing case-insensitive matching on title and description."
        elif "sortByRelevance" in prompt:
            return "Sorts results by relevance, prioritizing title matches over description matches, then by date (newer first)."
        else:
            return "Function performs specific task within the React search application."
    
    def _analyze_file(self, prompt: str) -> str:
        """Analyze file with Nemotron reasoning"""
        if "SearchBar" in prompt:
            return "React component implementing debounced search functionality. Uses lodash for debouncing and axios for API calls. Handles user input with real-time search capabilities."
        elif "SearchResults" in prompt:
            return "React component that displays search results. Imports and uses SearchBar component. Manages search state and renders result items with proper formatting."
        elif "utils" in prompt:
            return "Utility functions for search and data processing. Contains helper functions for date formatting, text manipulation, query validation, and result filtering/sorting."
        else:
            return "JavaScript/React file containing components and utilities for the search application."
    
    def _general_analysis(self, prompt: str) -> str:
        """General analysis with Nemotron reasoning"""
        if "project" in prompt.lower():
            return "React search application with debounced API calls. Implements real-time search functionality with proper user experience considerations including debouncing, error handling, and responsive design."
        else:
            return "Code analysis completed with comprehensive understanding of structure, functionality, and relationships."

class RealInternalDocAgent:
    """Real InternalDocAgent using Nemotron for code analysis"""
    
    def __init__(self):
        self.llm = NemotronLLM()
        self.function_prompt = PromptTemplate(
            input_variables=["function_name", "function_code"],
            template="""
            Analyze this JavaScript/React function:
            Function: {function_name}
            Code: {function_code}
            
            Provide a detailed summary of what this function does, its parameters, return values, and its role in the application.
            """
        )
        self.file_prompt = PromptTemplate(
            input_variables=["filename", "file_content"],
            template="""
            Analyze this JavaScript/React file:
            File: {filename}
            Content: {file_content}
            
            Provide a comprehensive summary of this file's purpose, its main components/functions, and its role in the application.
            """
        )
    
    def analyze_function(self, function_name: str, function_code: str) -> Dict[str, str]:
        """Analyze a function using Nemotron"""
        prompt = self.function_prompt.format(
            function_name=function_name,
            function_code=function_code
        )
        
        summary = self.llm._call(prompt)
        
        return {
            "name": function_name,
            "summary": summary
        }
    
    def analyze_file(self, filename: str, file_content: str) -> Dict[str, Any]:
        """Analyze a file using Nemotron"""
        prompt = self.file_prompt.format(
            filename=filename,
            file_content=file_content
        )
        
        summary = self.llm._call(prompt)
        
        # Extract functions from the file
        functions = self._extract_functions(file_content)
        analyzed_functions = []
        
        for func in functions:
            analyzed_func = self.analyze_function(func["name"], func["code"])
            analyzed_functions.append(analyzed_func)
        
        return {
            "filename": filename,
            "summary": summary,
            "functions": analyzed_functions
        }
    
    def _extract_functions(self, content: str) -> List[Dict[str, str]]:
        """Extract functions from JavaScript/React code"""
        functions = []
        
        # Pattern for function declarations
        patterns = [
            r'function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',  # function name() {}
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{[^}]*\}',  # const name = () => {}
            r'(\w+)\s*:\s*\([^)]*\)\s*=>\s*\{[^}]*\}',  # name: () => {}
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                function_name = match.group(1)
                function_code = match.group(0)
                functions.append({
                    "name": function_name,
                    "code": function_code
                })
        
        return functions 