"""
File moving functionality
"""

import os
import shutil
from typing import Dict, Any, List


def move_files(
    source_paths: List[str],
    destination_path: str,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Move files from source locations to destination directory.
    
    Use this tool when you need to relocate files for organization, clean up
    temporary files, or restructure your file system. This is a destructive
    operation that removes files from their original location.
    
    Args:
        source_paths: List of absolute paths to files or directories to move.
                     All paths should exist and be accessible.
        destination_path: Absolute path to destination directory where files will be moved.
                         Directory will be created if it doesn't exist.
        overwrite: Whether to overwrite existing files in destination.
                  If False, existing files cause the operation to fail. Defaults to False.
    
    Returns:
        A dictionary containing the move operation result:
        - status: 'success' if all files moved, 'partial' if some failed, 'error' if all failed
        - message: Descriptive message about the operation result
        - destination_path: Path to destination directory
        - files_moved: Number of files successfully moved
        - files_failed: Number of files that failed to move
        - moved_files: List of successfully moved file paths (new locations)
        - failed_files: List of files that failed to move with error messages
        
        Example success: {'status': 'success', 'message': 'Moved 3 files successfully',
                         'destination_path': '/path/to/dest', 'files_moved': 3, 'files_failed': 0,
                         'moved_files': [...], 'failed_files': []}
    """
    try:
        if not source_paths:
            return {
                "status": "error",
                "message": "No source paths provided for moving",
                "destination_path": destination_path
            }
        
        # Create destination directory if it doesn't exist
        try:
            os.makedirs(destination_path, exist_ok=True)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create destination directory: {str(e)}",
                "destination_path": destination_path
            }
        
        moved_files = []
        failed_files = []
        
        for source_path in source_paths:
            try:
                if not os.path.exists(source_path):
                    failed_files.append({
                        "path": source_path,
                        "error": "Source file/directory not found"
                    })
                    continue
                
                # Determine destination path
                item_name = os.path.basename(source_path)
                dest_item_path = os.path.join(destination_path, item_name)
                
                # Check if destination already exists
                if os.path.exists(dest_item_path):
                    if not overwrite:
                        failed_files.append({
                            "path": source_path,
                            "error": f"Destination already exists: {dest_item_path}"
                        })
                        continue
                    else:
                        # Remove existing destination
                        if os.path.isdir(dest_item_path):
                            shutil.rmtree(dest_item_path)
                        else:
                            os.remove(dest_item_path)
                
                # Move the file/directory
                shutil.move(source_path, dest_item_path)
                moved_files.append(dest_item_path)
                
            except Exception as e:
                failed_files.append({
                    "path": source_path,
                    "error": str(e)
                })
        
        # Determine overall status
        total_items = len(moved_files) + len(failed_files)
        
        if len(failed_files) == total_items and total_items > 0:
            status = "error"
            message = f"Failed to move all {len(failed_files)} items"
        elif len(failed_files) > 0:
            status = "partial"
            message = f"Moved {len(moved_files)} items, {len(failed_files)} failed"
        else:
            status = "success"
            message = f"Successfully moved {len(moved_files)} items"
        
        return {
            "status": status,
            "message": message,
            "destination_path": destination_path,
            "files_moved": len(moved_files),
            "files_failed": len(failed_files),
            "moved_files": moved_files,
            "failed_files": failed_files
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"File move operation failed: {str(e)}",
            "destination_path": destination_path
        }
