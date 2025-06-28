"""File compression functionality"""
import os
import zipfile
import tarfile
from typing import Dict, Any, List

def compress_files(file_paths: List[str], archive_path: str, format_type: str = "zip") -> Dict[str, Any]:
    """Compress files into archive."""
    try:
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        
        if format_type == "zip":
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in file_paths:
                    if os.path.exists(file_path):
                        if os.path.isfile(file_path):
                            zipf.write(file_path, os.path.basename(file_path))
                        elif os.path.isdir(file_path):
                            for root, dirs, files in os.walk(file_path):
                                for file in files:
                                    full_path = os.path.join(root, file)
                                    arc_path = os.path.relpath(full_path, os.path.dirname(file_path))
                                    zipf.write(full_path, arc_path)
        
        return {
            "status": "success",
            "message": f"Created {format_type} archive with {len(file_paths)} items",
            "archive_path": archive_path,
            "archive_size": os.path.getsize(archive_path)
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "archive_path": None}
