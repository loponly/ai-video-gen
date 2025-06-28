"""File deletion functionality"""
import os
import shutil
from typing import Dict, Any, List

def delete_files(file_paths: List[str], force: bool = False) -> Dict[str, Any]:
    """Delete files and directories safely."""
    try:
        deleted_files = []
        failed_files = []
        
        for path in file_paths:
            try:
                if not os.path.exists(path):
                    failed_files.append({"path": path, "error": "Path not found"})
                    continue
                
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    if force:
                        shutil.rmtree(path)
                    else:
                        os.rmdir(path)  # Only works if empty
                
                deleted_files.append(path)
            except Exception as e:
                failed_files.append({"path": path, "error": str(e)})
        
        status = "success" if not failed_files else ("partial" if deleted_files else "error")
        message = f"Deleted {len(deleted_files)} items"
        if failed_files:
            message += f", {len(failed_files)} failed"
        
        return {
            "status": status,
            "message": message,
            "files_deleted": len(deleted_files),
            "files_failed": len(failed_files),
            "deleted_files": deleted_files,
            "failed_files": failed_files
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
