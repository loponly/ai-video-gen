"""
File copying functionality
"""

import os
import shutil
from typing import Dict, Any, List


def copy_files(
    source_paths: List[str],
    destination_path: str,
    preserve_structure: bool = True,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Copy files from source locations to destination directory.
    
    Use this tool when you need to duplicate files for backup, organize content
    into different directories, or prepare files for processing workflows.
    Supports both individual files and batch operations.
    
    Args:
        source_paths: List of absolute paths to files or directories to copy.
                     All paths should exist and be accessible.
        destination_path: Absolute path to destination directory where files will be copied.
                         Directory will be created if it doesn't exist.
        preserve_structure: Whether to maintain directory structure when copying.
                          If False, all files are copied to destination root. Defaults to True.
        overwrite: Whether to overwrite existing files in destination.
                  If False, existing files are skipped. Defaults to False.
    
    Returns:
        A dictionary containing the copy operation result:
        - status: 'success' if all files copied, 'partial' if some failed, 'error' if all failed
        - message: Descriptive message about the operation result
        - destination_path: Path to destination directory
        - files_copied: Number of files successfully copied
        - files_skipped: Number of files skipped (due to overwrite=False)
        - files_failed: Number of files that failed to copy
        - copied_files: List of successfully copied file paths
        - failed_files: List of files that failed to copy with error messages
        
        Example success: {'status': 'success', 'message': 'Copied 5 files successfully',
                         'destination_path': '/path/to/dest', 'files_copied': 5, 'files_skipped': 0,
                         'files_failed': 0, 'copied_files': [...], 'failed_files': []}
        Example error: {'status': 'error', 'message': 'Destination path is invalid',
                       'destination_path': destination_path}
    """
    try:
        # Validate inputs
        if not source_paths:
            return {
                "status": "error",
                "message": "No source paths provided for copying",
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
        
        copied_files = []
        skipped_files = []
        failed_files = []
        
        for source_path in source_paths:
            try:
                if not os.path.exists(source_path):
                    failed_files.append({
                        "path": source_path,
                        "error": "Source file/directory not found"
                    })
                    continue
                
                if os.path.isfile(source_path):
                    # Copy individual file
                    filename = os.path.basename(source_path)
                    dest_file_path = os.path.join(destination_path, filename)
                    
                    # Check if file already exists
                    if os.path.exists(dest_file_path) and not overwrite:
                        skipped_files.append(dest_file_path)
                        continue
                    
                    shutil.copy2(source_path, dest_file_path)
                    copied_files.append(dest_file_path)
                
                elif os.path.isdir(source_path):
                    # Copy directory
                    dir_name = os.path.basename(source_path)
                    dest_dir_path = os.path.join(destination_path, dir_name)
                    
                    if preserve_structure:
                        if os.path.exists(dest_dir_path) and not overwrite:
                            skipped_files.append(dest_dir_path)
                            continue
                        
                        if os.path.exists(dest_dir_path) and overwrite:
                            shutil.rmtree(dest_dir_path)
                        
                        shutil.copytree(source_path, dest_dir_path)
                        copied_files.append(dest_dir_path)
                    else:
                        # Copy all files from directory to destination root
                        for root, dirs, files in os.walk(source_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                dest_file_path = os.path.join(destination_path, file)
                                
                                if os.path.exists(dest_file_path) and not overwrite:
                                    skipped_files.append(dest_file_path)
                                    continue
                                
                                shutil.copy2(file_path, dest_file_path)
                                copied_files.append(dest_file_path)
                
            except Exception as e:
                failed_files.append({
                    "path": source_path,
                    "error": str(e)
                })
        
        # Determine overall status
        total_files = len(copied_files) + len(skipped_files) + len(failed_files)
        
        if len(failed_files) == total_files and total_files > 0:
            status = "error"
            message = f"Failed to copy all {len(failed_files)} files"
        elif len(failed_files) > 0:
            status = "partial"
            message = f"Copied {len(copied_files)} files, {len(failed_files)} failed, {len(skipped_files)} skipped"
        else:
            status = "success"
            message = f"Successfully copied {len(copied_files)} files"
            if len(skipped_files) > 0:
                message += f", {len(skipped_files)} skipped"
        
        return {
            "status": status,
            "message": message,
            "destination_path": destination_path,
            "files_copied": len(copied_files),
            "files_skipped": len(skipped_files),
            "files_failed": len(failed_files),
            "copied_files": copied_files,
            "skipped_files": skipped_files,
            "failed_files": failed_files
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"File copy operation failed: {str(e)}",
            "destination_path": destination_path
        }
