"""File information functionality"""
import os
import stat
from typing import Dict, Any

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed file information and metadata."""
    try:
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found", "file_path": file_path}
        
        file_stat = os.stat(file_path)
        
        return {
            "status": "success",
            "message": f"Retrieved information for {os.path.basename(file_path)}",
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "size": file_stat.st_size,
            "type": "directory" if os.path.isdir(file_path) else "file",
            "created": file_stat.st_ctime,
            "modified": file_stat.st_mtime,
            "permissions": oct(file_stat.st_mode)[-3:],
            "extension": os.path.splitext(file_path)[1] if os.path.isfile(file_path) else None
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "file_path": file_path}
