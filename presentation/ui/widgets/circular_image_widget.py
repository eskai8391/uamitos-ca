from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QPainter, QPainterPath, QBrush, QColor, QFont
from PySide6.QtWidgets import QLabel
import os


def get_initials(name):
    """
    Extract initials from a name
    
    :param name: Full name to extract initials from
    :return: String with up to 2 initials
    """
    if not name:
        return ""
        
    parts = name.split()
    initials = ""
    
    for part in parts[:2]:  # Take first two parts of the name
        if part:
            initials += part[0].upper()
            
    return initials


class CircularImageWidget(QLabel):
    """
    A widget that displays a circular image from a file path or QPixmap.
    Falls back to displaying initials if no image is provided.
    """
    
    def __init__(self, size=64, placeholder_bg_color="#8ecaef", placeholder_text="", parent=None):
        """
        Initialize circular image widget
        
        :param size: Size of the widget in pixels (width = height)
        :param placeholder_bg_color: Background color for placeholder when no image is available
        :param placeholder_text: Text to show in placeholder (typically initials)
        :param parent: Parent widget
        """
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._pixmap = None
        self._placeholder_bg_color = placeholder_bg_color
        self._placeholder_text = placeholder_text
        self._size = size
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # No need for mouse tracking
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    
    def setImage(self, image_path):
        """
        Set image from a file path
        
        :param image_path: Path to the image file
        """
        if not image_path or not os.path.exists(image_path):
            self._pixmap = None
            self.update()
            return
            
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.setPixmap(pixmap)
    
    def setPixmap(self, pixmap):
        """
        Set a QPixmap directly
        
        :param pixmap: QPixmap to display
        """
        self._pixmap = pixmap
        self.update()
    
    def setPlaceholderText(self, text):
        """
        Set the placeholder text (initials)
        
        :param text: Text to display when no image is available
        """
        self._placeholder_text = text
        self.update()
    
    def setPlaceholderColor(self, color):
        """
        Set the background color for the placeholder
        
        :param color: Color string like "#RRGGBB" or a QColor
        """
        self._placeholder_bg_color = color
        self.update()
    
    def paintEvent(self, event):
        """Override paint event to draw circular image or placeholder"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create circular clipping path
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        
        # Apply clipping path
        painter.setClipPath(path)
        
        if self._pixmap and not self._pixmap.isNull():
            # Scale the pixmap to fit the widget
            scaled_pixmap = self._pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                Qt.TransformationMode.SmoothTransformation
            )
            
            # Center the pixmap
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            
            # Draw pixmap
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            # Draw placeholder with background color and text
            painter.setBrush(QBrush(QColor(self._placeholder_bg_color)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(0, 0, self.width(), self.height())
            
            if self._placeholder_text:
                painter.setPen(Qt.GlobalColor.white)
                
                # Set font size based on widget size
                font = painter.font()
                font_size = max(8, self._size // 3)
                font.setPixelSize(font_size)
                font.setBold(True)
                painter.setFont(font)
                
                # Draw text centered
                painter.drawText(
                    self.rect(), 
                    Qt.AlignmentFlag.AlignCenter, 
                    self._placeholder_text
                )
        
        # Draw circle outline for better visual appearance
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QColor(0, 0, 0, 30))  # Semi-transparent black
        painter.drawEllipse(0, 0, self.width() - 1, self.height() - 1)