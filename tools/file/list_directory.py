"""Directory listing functionality"""
import os
from typing import Dict, Any

def list_directory(directory_path: str, include_hidden: bool = False) -> Dict[str, Any]:
    """List directory contents with file information."""
    try:
        if not os.path.exists(directory_path):
            return {"status": "error", "message": "Directory not found", "directory_path": directory_path}
        
        items = []
        for item in os.listdir(directory_path):
            if not include_hidden and item.startswith('.'):
                continue
            
            item_path = os.path.join(directory_path, item)
            item_info = {
                "name": item,
                "path": item_path,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
            }
            items.append(item_info)
        
        return {
            "status": "success",
            "message": f"Listed {len(items)} items in directory",
            "directory_path": directory_path,
            "items": items,
            "total_items": len(items)
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "directory_path": directory_path}
