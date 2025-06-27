"""
Path Configuration Module for AI Video Generator

This module provides centralized path management to ensure consistent
directory usage across all agents and tools.
"""

import os
from pathlib import Path
from typing import Union


class PathConfig:
    """Centralized path configuration for the AI Video Generator project."""
    
    # Base project directory (assuming this file is in adk_agents/)
    PROJECT_ROOT = Path(__file__).parent.parent.absolute()
    
    # Standard directories
    DOWNLOADS_DIR = PROJECT_ROOT / "downloads"
    OUTPUTS_DIR = PROJECT_ROOT / "outputs"
    ASSETS_DIR = PROJECT_ROOT / "assets"
    CONTENT_DIR = PROJECT_ROOT / "content"
    CACHE_DIR = PROJECT_ROOT / "cache-models"
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create all required directories if they don't exist."""
        directories = [
            cls.DOWNLOADS_DIR,
            cls.OUTPUTS_DIR,
            cls.ASSETS_DIR,
            cls.CONTENT_DIR,
            cls.CACHE_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    @classmethod
    def get_download_path(cls, filename: str = None) -> str:
        """Get the standardized download path."""
        cls.ensure_directories()
        if filename:
            return str(cls.DOWNLOADS_DIR / filename)
        return str(cls.DOWNLOADS_DIR)
    
    @classmethod
    def get_output_path(cls, filename: str = None) -> str:
        """Get the standardized output path."""
        cls.ensure_directories()
        if filename:
            return str(cls.OUTPUTS_DIR / filename)
        return str(cls.OUTPUTS_DIR)
    
    @classmethod
    def get_assets_path(cls, filename: str = None) -> str:
        """Get the standardized assets path."""
        cls.ensure_directories()
        if filename:
            return str(cls.ASSETS_DIR / filename)
        return str(cls.ASSETS_DIR)
    
    @classmethod
    def get_content_path(cls, filename: str = None) -> str:
        """Get the standardized content path."""
        cls.ensure_directories()
        if filename:
            return str(cls.CONTENT_DIR / filename)
        return str(cls.CONTENT_DIR)
    
    @classmethod
    def normalize_path(cls, path: Union[str, Path]) -> str:
        """Normalize a path relative to project root."""
        path = Path(path)
        if path.is_absolute():
            try:
                # Try to make it relative to project root
                path = path.relative_to(cls.PROJECT_ROOT)
            except ValueError:
                # Path is outside project root, keep as is
                pass
        return str(path)
    
    @classmethod
    def validate_download_path(cls, path: str) -> bool:
        """Validate that a path is within the downloads directory."""
        normalized_path = Path(path).resolve()
        try:
            normalized_path.relative_to(cls.DOWNLOADS_DIR.resolve())
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_output_path(cls, path: str) -> bool:
        """Validate that a path is within the outputs directory."""
        normalized_path = Path(path).resolve()
        try:
            normalized_path.relative_to(cls.OUTPUTS_DIR.resolve())
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_relative_path(cls, absolute_path: Union[str, Path]) -> str:
        """Get relative path from project root."""
        abs_path = Path(absolute_path).resolve()
        try:
            return str(abs_path.relative_to(cls.PROJECT_ROOT))
        except ValueError:
            return str(abs_path)


# Initialize directories on module import
PathConfig.ensure_directories()
