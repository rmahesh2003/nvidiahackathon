from typing import List, Dict, Any, Optional
from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re
import os
import torch
import requests
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.config import Config

class NemotronSuperLLM(LLM):
    """Nemotron Super 49B LLM for intelligent code documentation generation."""
    
    def __init__(self, model_name: Optional[str] = None, device: Optional[str] = None):
        super().__init__()
        config = Config.get_model_config()
        self.model_name = model_name or "microsoft/DialoGPT-medium"  # Fallback model
        self.device = device or config["device"]
        self.max_length = config["max_length"]
        self.temperature = config["temperature"]
        self.enable_fallback = config["enable_fallback"]
        self.model = None
        self.tokenizer = None
        self.cache = {} if Config.CACHE_ENABLED else None
        self.api_endpoint = config.get("api_endpoint", None)
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Nemotron Super 49B model and tokenizer."""
        try:
            # Try to load Nemotron Super 49B from NVIDIA's model hub
            model_id = "nvidia/nemotron-3-49b-super"
            
            print(f"🚀 Loading Nemotron Super 49B model...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                trust_remote_code=True,
                use_fast=False
            )
            
            # Load model with GPU optimization
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                load_in_8bit=True  # For memory efficiency
            )
            
            # Set pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"✅ Nemotron Super 49B loaded successfully on {self.device}")
            
        except Exception as e:
            print(f"⚠️ Failed to load Nemotron Super 49B: {e}")
            print("🔄 Falling back to enhanced rule-based system")
            self.model = None
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Generate intelligent documentation using Nemotron Super 49B model."""
        
        # Check cache first
        if self.cache is not None and prompt in self.cache:
            return self.cache[prompt]
        
        if self.model is None:
            if self.enable_fallback:
                return self._enhanced_rule_based_response(prompt)
            else:
                raise Exception("Nemotron Super 49B model not available and fallback is disabled")
        
        try:
            # Prepare the prompt for Nemotron
            formatted_prompt = self._format_prompt_for_nemotron(prompt)
            
            # Tokenize the prompt
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048
            ).to(self.device)
            
            # Generate response with Nemotron Super 49B
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.max_length,
                    temperature=self.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,
                    top_p=0.9,
                    top_k=50
                )
            
            # Decode the response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            # Clean up the response
            response = generated_text.strip()
            if stop:
                for stop_seq in stop:
                    if stop_seq in response:
                        response = response.split(stop_seq)[0]
            
            final_response = response if response else self._enhanced_rule_based_response(prompt)
            
            # Cache the result
            if self.cache is not None:
                self.cache[prompt] = final_response
            
            return final_response
            
        except Exception as e:
            print(f"⚠️ Nemotron Super 49B generation failed: {e}")
            fallback_response = self._enhanced_rule_based_response(prompt)
            
            # Cache the fallback result
            if self.cache is not None:
                self.cache[prompt] = fallback_response
            
            return fallback_response
    
    def _format_prompt_for_nemotron(self, prompt: str) -> str:
        """Format prompt specifically for Nemotron Super 49B."""
        # Nemotron Super 49B works well with structured prompts
        system_prompt = """You are an expert code documentation generator. Your task is to analyze code and generate clear, professional documentation that explains what the code does, its purpose, parameters, return values, and any important considerations."""
        
        formatted_prompt = f"""<|system|>
{system_prompt}
<|user|>
{prompt}
<|assistant|>"""
        
        return formatted_prompt
    
    def _enhanced_rule_based_response(self, prompt: str) -> str:
        """Enhanced rule-based system with better patterns and context."""
        
        # Extract function information
        func_match = re.search(r'function\s+(\w+)', prompt)
        file_type_match = re.search(r'(\w+)\s+file', prompt)
        
        if func_match:
            func_name = func_match.group(1)
            file_type = file_type_match.group(1) if file_type_match else "unknown"
            
            # Enhanced function analysis
            if "handle" in func_name.lower():
                action = func_name.replace('handle', '').replace('Handle', '')
                return f"Handles user interaction for {action.lower()} with proper event management and state updates"
            elif "get" in func_name.lower():
                target = func_name.replace('get', '').replace('Get', '')
                return f"Retrieves {target.lower()} data with appropriate error handling and caching"
            elif "set" in func_name.lower():
                target = func_name.replace('set', '').replace('Set', '')
                return f"Updates {target.lower()} value with validation and triggers necessary side effects"
            elif "validate" in func_name.lower():
                target = func_name.replace('validate', '').replace('Validate', '')
                return f"Validates {target.lower()} input with comprehensive error checking and user feedback"
            elif "process" in func_name.lower():
                target = func_name.replace('process', '').replace('Process', '')
                return f"Processes {target.lower()} data with appropriate transformations and error handling"
            elif "render" in func_name.lower():
                return f"Renders UI components with proper state management and lifecycle handling"
            elif "fetch" in func_name.lower():
                return f"Makes API request to retrieve data with proper error handling and loading states"
            elif "update" in func_name.lower():
                target = func_name.replace('update', '').replace('Update', '')
                return f"Updates {target.lower()} with optimistic UI updates and proper error recovery"
            else:
                return f"Executes {func_name} operation with appropriate error handling and state management"
        
        # File summary generation
        if "summary" in prompt.lower():
            if "react" in prompt.lower() or "jsx" in prompt.lower():
                return "React component that provides interactive user interface functionality with proper state management and event handling"
            elif "python" in prompt.lower():
                return "Python module containing utility functions and business logic with comprehensive error handling"
            elif "javascript" in prompt.lower():
                return "JavaScript module with client-side functionality including API integration and user interaction handling"
            else:
                return "Code file with various functions and utilities designed for maintainable and scalable development"
        
        return "This function performs the specified operation with appropriate error handling and state management."
    
    @property
    def _llm_type(self) -> str:
        return "nemotron_super_49b"

class InternalDocAgent:
    """Agent responsible for analyzing code structure and generating internal documentation."""
    
    def __init__(self):
        self.llm = NemotronSuperLLM()
        self.function_doc_prompt = PromptTemplate(
            input_variables=["function_name", "parameters", "context", "file_type"],
            template="""
            You are an expert code documentation generator with deep understanding of software architecture and best practices. Analyze this function and create comprehensive, intelligent documentation.
            
            Function Name: {function_name}
            Parameters: {parameters}
            File Type: {file_type}
            Context: {context}
            
            Generate intelligent documentation that includes:
            - Clear explanation of the function's purpose and behavior
            - Analysis of the function's role in the broader codebase
            - Parameter descriptions with types and constraints
            - Return value explanation and type information
            - Side effects and state changes
            - Error handling and edge cases
            - Performance considerations if relevant
            - Usage examples or patterns
            - Security considerations if applicable
            
            Make the documentation creative, insightful, and helpful for developers. Think beyond basic descriptions to provide architectural context and best practices.
            
            Documentation:
            """
        )
        
        self.file_summary_prompt = PromptTemplate(
            input_variables=["filename", "functions", "imports", "file_type", "line_count"],
            template="""
            You are an expert software architect and code analyst with deep knowledge of design patterns, best practices, and system architecture. Analyze this code file and provide a comprehensive, intelligent summary.
            
            File: {filename}
            Type: {file_type}
            Functions: {functions}
            Imports: {imports}
            Lines of Code: {line_count}
            
            Provide an intelligent analysis that includes:
            - Architectural role and purpose of this file
            - Design patterns and coding patterns used
            - Component relationships and dependencies
            - Code quality assessment and suggestions
            - Performance implications and optimizations
            - Security considerations and best practices
            - Scalability and maintainability factors
            - Integration points with other system components
            - Potential refactoring opportunities
            - Testing strategies and coverage considerations
            
            Think like a senior software architect providing insights that go beyond surface-level descriptions. Consider the broader system context and provide actionable insights.
            
            Analysis:
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
            'file_type': file_type,
            'line_count': parsed_data.get('line_count', 0)
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
            'context': context,
            'file_type': file_type
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