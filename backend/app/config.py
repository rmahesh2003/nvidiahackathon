import os
from typing import Optional

class Config:
    """Configuration management for DocuSynth AI."""
    
    # AI Model Configuration
    NEMOTRON_MODEL_NAME: str = os.getenv("NEMOTRON_MODEL_NAME", "nvidia/nemotron-3-49b-super")
    NEMOTRON_DEVICE: str = os.getenv("NEMOTRON_DEVICE", "cuda" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu")
    NEMOTRON_MAX_LENGTH: int = int(os.getenv("NEMOTRON_MAX_LENGTH", "150"))
    NEMOTRON_TEMPERATURE: float = float(os.getenv("NEMOTRON_TEMPERATURE", "0.7"))
    NEMOTRON_API_ENDPOINT: str = os.getenv("NEMOTRON_API_ENDPOINT", "")
    
    # Fallback Configuration
    ENABLE_FALLBACK: bool = os.getenv("ENABLE_FALLBACK", "true").lower() == "true"
    ENHANCED_RULE_BASED: bool = os.getenv("ENHANCED_RULE_BASED", "true").lower() == "true"
    
    # Performance Configuration
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "1"))
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "true").lower() == "true"
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def get_model_config(cls) -> dict:
        """Get AI model configuration."""
        return {
            "model_name": cls.NEMOTRON_MODEL_NAME,
            "device": cls.NEMOTRON_DEVICE,
            "max_length": cls.NEMOTRON_MAX_LENGTH,
            "temperature": cls.NEMOTRON_TEMPERATURE,
            "api_endpoint": cls.NEMOTRON_API_ENDPOINT,
            "enable_fallback": cls.ENABLE_FALLBACK,
            "enhanced_rule_based": cls.ENHANCED_RULE_BASED
        }
    
    @classmethod
    def get_performance_config(cls) -> dict:
        """Get performance configuration."""
        return {
            "batch_size": cls.BATCH_SIZE,
            "cache_enabled": cls.CACHE_ENABLED
        } 