"""
File writing tool for saving content to files
"""

import os
from typing import Any, Dict


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """
    Write content to a file.
    
    Args:
        file_path (str): Path where to save the file
        content (str): Content to write to the file
        encoding (str): File encoding (default: utf-8)
        
    Returns:
        Dict[str, Any]: Result containing success status, file path, and message
    """
    try:
        # Create directory if it doesn't exist
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        # Write content to file
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
            
        # Get file size for confirmation
        file_size = os.path.getsize(file_path)
        
        return {
            'success': True,
            'file_path': file_path,
            'file_size': file_size,
            'message': f'Successfully wrote {len(content)} characters to {file_path} (size: {file_size} bytes)'
        }
        
    except Exception as e:
        return {
            'success': False,
            'file_path': file_path,
            'error': str(e),
            'message': f'Failed to write file {file_path}: {str(e)}'
        }
