#!/usr/bin/env python3
"""
Simple test script to verify basic functionality without AI model.
This will work locally and help us debug the core system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.file_parser import FileParser
from app.agents.internal_doc_agent import InternalDocAgent

def test_basic_functionality():
    """Test basic functionality without AI model."""
    print("🧪 Testing Basic DocuSynth Functionality")
    print("=" * 50)
    
    # Test file parser
    print("📁 Testing File Parser...")
    parser = FileParser()
    
    # Create a simple test file
    test_code = '''
def calculate_sum(a, b):
    """Add two numbers together."""
    return a + b

def multiply_numbers(x, y):
    """Multiply two numbers."""
    result = x * y
    return result

class Calculator:
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"Added {a} + {b} = {result}")
        return result
'''
    
    # Create a temporary file for testing
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    # Parse the test code
    parsed_data = parser.parse_python_file(temp_file)
    
    # Clean up
    os.unlink(temp_file)
    print(f"✅ Parsed {len(parsed_data.get('functions', []))} functions")
    print(f"✅ Found {len(parsed_data.get('imports', []))} imports")
    
    # Test agent initialization (without AI)
    print("\n🤖 Testing Agent Initialization...")
    try:
        agent = InternalDocAgent()
        print("✅ Agent initialized successfully")
        
        # Test fallback documentation generation
        print("\n📝 Testing Fallback Documentation...")
        func = {'name': 'calculate_sum', 'parameters': ['a', 'b']}
        doc = agent._generate_function_documentation(func, 'python')
        print(f"✅ Generated documentation: {doc[:100]}...")
        
        # Test file summary
        summary = agent._generate_file_summary('test.py', parsed_data, 'python')
        print(f"✅ Generated summary: {summary[:100]}...")
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False
    
    print("\n🎉 Basic functionality test completed successfully!")
    print("🚀 Ready to deploy to Brev with GPU acceleration!")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n✅ All basic tests passed! The project is ready for Brev deployment.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.") 