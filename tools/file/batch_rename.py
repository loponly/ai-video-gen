"""Batch file renaming functionality"""
import os
from typing import Dict, Any, List

def batch_rename(file_paths: List[str], naming_pattern: str, start_number: int = 1) -> Dict[str, Any]:
    """Rename multiple files using a pattern."""
    try:
        renamed_files = []
        failed_files = []
        
        for i, file_path in enumerate(file_paths):
            try:
                if not os.path.exists(file_path):
                    failed_files.append({"path": file_path, "error": "File not found"})
                    continue
                
                directory = os.path.dirname(file_path)
                extension = os.path.splitext(file_path)[1]
                
                # Generate new name using pattern
                new_name = naming_pattern.format(number=start_number + i, index=i)
                new_path = os.path.join(directory, new_name + extension)
                
                os.rename(file_path, new_path)
                renamed_files.append({"old_path": file_path, "new_path": new_path})
                
            except Exception as e:
                failed_files.append({"path": file_path, "error": str(e)})
        
        status = "success" if not failed_files else ("partial" if renamed_files else "error")
        message = f"Renamed {len(renamed_files)} files"
        if failed_files:
            message += f", {len(failed_files)} failed"
        
        return {
            "status": status,
            "message": message,
            "files_renamed": len(renamed_files),
            "files_failed": len(failed_files),
            "renamed_files": renamed_files,
            "failed_files": failed_files
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
