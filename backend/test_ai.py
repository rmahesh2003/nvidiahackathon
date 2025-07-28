#!/usr/bin/env python3
"""
Test script for DocuSynth AI integration.
This script tests the AI capabilities without running the full server.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.agents.internal_doc_agent import InternalDocAgent
from app.config import Config

def test_ai_integration():
    """Test the Nemotron Super 49B integration with sample code."""
    
    print("🧠 Testing DocuSynth AI with Nemotron Super 49B")
    print("=" * 60)
    
    # Initialize the agent
    print("📦 Initializing InternalDocAgent with Nemotron Super 49B...")
    agent = InternalDocAgent()
    
    # Test data
    test_functions = [
        {
            'name': 'handleSearch',
            'parameters': ['query', 'filters'],
            'context': 'React component function'
        },
        {
            'name': 'getUserData',
            'parameters': ['userId'],
            'context': 'API utility function'
        },
        {
            'name': 'validateInput',
            'parameters': ['input', 'rules'],
            'context': 'Form validation function'
        }
    ]
    
    print("\n🔍 Testing function documentation generation...")
    for i, func in enumerate(test_functions, 1):
        print(f"\n--- Test {i}: {func['name']} ---")
        
        # Generate documentation
        doc = agent._generate_function_documentation(func, 'javascript')
        print(f"Generated: {doc}")
    
    # Test file summary
    print("\n📄 Testing file summary generation...")
    test_file_data = {
        'functions': ['handleSearch', 'getUserData', 'validateInput'],
        'imports': ['react', 'axios', 'lodash'],
        'line_count': 150
    }
    
    summary = agent._generate_file_summary('SearchComponent.js', test_file_data, 'javascript')
    print(f"File Summary: {summary}")
    
    print("\n✅ Nemotron Super 49B Integration Test Complete!")
    print("\nConfiguration:")
    config = Config.get_model_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print("\n🚀 Ready for Brev deployment with GPU acceleration!")

if __name__ == "__main__":
    test_ai_integration() 