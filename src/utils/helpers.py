from datetime import datetime
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional


# Configure logging
logger = logging.getLogger(__name__)


def validate_environment_variables() -> bool:
    """Validate that all required environment variables are set"""
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_DEPLOYMENT_NAME",  # Added your deployment name
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT",
        "PINECONE_INDEX",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info("All required environment variables are present")
    return True


def format_user_profile(profile_dict: Dict[str, Any]) -> str:
    """Format user profile dictionary into a readable string"""
    return f"""
    Career Interests: {profile_dict.get('interests', 'Not specified')}
    Current Skills: {profile_dict.get('skills', 'Not specified')}
    Experience Level: {profile_dict.get('experience', 'Not specified')}
    Career Goals: {profile_dict.get('goals', 'Not specified')}
    """


def validate_user_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean user profile data"""
    validated_profile = {
        "interests": str(profile.get("interests", "")).strip(),
        "skills": str(profile.get("skills", "")).strip(),
        "experience": str(profile.get("experience", "")).strip(),
        "goals": str(profile.get("goals", "")).strip(),
    }

    # Validate experience level
    valid_experience_levels = [
        "Student",
        "Entry-level",
        "Mid-level",
        "Senior",
        "Executive",
    ]
    if validated_profile["experience"] not in valid_experience_levels:
        logger.warning(f"Invalid experience level: {validated_profile['experience']}")
        validated_profile["experience"] = "Student"  # Default value

    return validated_profile


def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to specified length, adding ellipsis if needed"""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""

    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove control characters
    text = "".join(char for char in text if ord(char) >= 32 or ord(char) in [9, 10, 13])

    return text.strip()


def format_timestamp(timestamp: Optional[float] = None) -> str:
    """Format timestamp to readable string"""
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def calculate_response_time(start_time: float) -> float:
    """Calculate response time in seconds"""
    return datetime.now().timestamp() - start_time


def get_azure_deployment_info() -> Dict[str, str]:
    """Get Azure deployment information for logging"""
    return {
        "deployment_name": os.getenv("AZURE_DEPLOYMENT_NAME", "Not set"),
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "Not set"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "Not set"),
    }
