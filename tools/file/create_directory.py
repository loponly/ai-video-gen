"""Directory creation functionality"""
import os
from typing import Dict, Any

def create_directory(directory_path: str, recursive: bool = True) -> Dict[str, Any]:
    """Create directories with optional recursive creation."""
    try:
        if recursive:
            os.makedirs(directory_path, exist_ok=True)
        else:
            os.mkdir(directory_path)
        
        return {
            "status": "success",
            "message": f"Directory created: {directory_path}",
            "directory_path": directory_path,
            "exists": os.path.exists(directory_path)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to create directory: {str(e)}",
            "directory_path": directory_path
        }
