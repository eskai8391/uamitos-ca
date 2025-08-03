import os
import logging
from typing import Optional


class ProfileImageService:
    """Service for managing user profile images"""
    
    def __init__(self, base_path="assets/profile_images"):
        """
        Initialize profile image service
        
        :param base_path: Base directory for profile images
        """
        self._logger = logging.getLogger(__name__)
        self._base_path = base_path
        
        # Create directory if it doesn't exist
        os.makedirs(self._base_path, exist_ok=True)
    
    def get_image_path(self, user_id: str, role: Optional[str] = None) -> str:
        """
        Get the profile image path for a user
        
        :param user_id: User identifier (uuid or username)
        :param role: Optional user role for role-specific default images
        :return: Path to the user's profile image or default image
        """
        # Sanitize user_id to use as filename
        safe_id = user_id.replace(" ", "_").lower()
        
        # Check for specific image formats
        for ext in ['.png', '.jpg', '.jpeg']:
            specific_path = os.path.join(self._base_path, f"{safe_id}{ext}")
            if os.path.exists(specific_path):
                return specific_path
        
        # Return role-specific default if role is provided
        if role:
            role_default = os.path.join(self._base_path, f"default_{role.lower()}.png")
            if os.path.exists(role_default):
                return role_default
        
        # Return general default image
        default_path = os.path.join(self._base_path, "default.png")
        
        # If even the default doesn't exist, return empty string
        if not os.path.exists(default_path):
            self._logger.warning(f"Default profile image not found at {default_path}")
            return ""
        
        return default_path
    
    def save_image(self, user_id: str, image_path: str) -> bool:
        """
        Save a profile image for a user
        
        :param user_id: User identifier
        :param image_path: Path to the image file to save
        :return: True if successful, False otherwise
        """
        try:
            from PySide6.QtGui import QImage
            
            # Sanitize user_id
            safe_id = user_id.replace(" ", "_").lower()
            
            # Determine file extension
            _, ext = os.path.splitext(image_path)
            if not ext:
                ext = ".png"  # Default to PNG
            
            # Create target path
            target_path = os.path.join(self._base_path, f"{safe_id}{ext}")
            
            # Load and save the image
            image = QImage(image_path)
            if image.isNull():
                self._logger.error(f"Failed to load image from {image_path}")
                return False
            
            # Save image as PNG
            success = image.save(target_path)
            if not success:
                self._logger.error(f"Failed to save image to {target_path}")
                return False
                
            return True
            
        except Exception as e:
            self._logger.error(f"Error saving profile image: {e}")
            return False