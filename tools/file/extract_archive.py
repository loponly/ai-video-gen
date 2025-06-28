"""Archive extraction functionality"""
import os
import zipfile
import tarfile
from typing import Dict, Any

def extract_archive(archive_path: str, destination_path: str) -> Dict[str, Any]:
    """Extract archive contents to destination."""
    try:
        if not os.path.exists(archive_path):
            return {"status": "error", "message": "Archive not found", "destination_path": None}
        
        os.makedirs(destination_path, exist_ok=True)
        
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(destination_path)
        elif archive_path.endswith(('.tar.gz', '.tgz')):
            with tarfile.open(archive_path, 'r:gz') as tarf:
                tarf.extractall(destination_path)
        
        return {
            "status": "success",
            "message": f"Extracted archive to {destination_path}",
            "destination_path": destination_path,
            "extracted_files": len(os.listdir(destination_path))
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "destination_path": None}
