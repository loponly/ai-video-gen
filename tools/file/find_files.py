"""File search functionality"""
import os
import fnmatch
from typing import Dict, Any, List

def find_files(search_directory: str, pattern: str = "*", file_type: str = "all") -> Dict[str, Any]:
    """Search for files matching pattern in directory tree."""
    try:
        if not os.path.exists(search_directory):
            return {"status": "error", "message": "Search directory not found", "search_directory": search_directory}
        
        found_files = []
        
        for root, dirs, files in os.walk(search_directory):
            items = files if file_type == "file" else (dirs if file_type == "directory" else files + dirs)
            
            for item in items:
                if fnmatch.fnmatch(item, pattern):
                    item_path = os.path.join(root, item)
                    item_info = {
                        "name": item,
                        "path": item_path,
                        "type": "directory" if os.path.isdir(item_path) else "file",
                        "relative_path": os.path.relpath(item_path, search_directory)
                    }
                    found_files.append(item_info)
        
        return {
            "status": "success",
            "message": f"Found {len(found_files)} items matching '{pattern}'",
            "search_directory": search_directory,
            "pattern": pattern,
            "found_files": found_files,
            "total_found": len(found_files)
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "search_directory": search_directory}
