from typing import Dict, Any, Optional, Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from presentation.ui.builders.widgets.base_widget_builder import BaseWidgetBuilder


class WidgetDirector:
    """
    Director class that coordinates the widget building process.
    The Director defines the order in which to execute the building steps.
    """

    @staticmethod
    def construct_basic_widget(builder: BaseWidgetBuilder, config: Dict[str, Any]) -> QWidget:
        """
        Constructs a widget with basic configuration
        
        :param builder: The widget builder to use
        :param config: Configuration dictionary with widget properties
        :return: The constructed widget
        """
        if 'geometry' in config:
            x, y, width, height = config['geometry']
            builder.set_geometry(x, y, width, height)
            
        if 'fixed_size' in config:
            width, height = config['fixed_size']
            builder.set_fixed_size(width, height)
            
        if 'object_name' in config:
            builder.set_object_name(config['object_name'])
            
        if 'style_sheet' in config:
            builder.set_style_sheet(config['style_sheet'])
            
        # Font configuration
        if 'font_size' in config:
            builder.set_font_size(config['font_size'])
            
        if 'font_bold' in config:
            builder.set_font_bold(config['font_bold'])
            
        if 'font_family' in config:
            builder.set_font_family(config['font_family'])
            
        # Alignment
        if 'alignment' in config:
            builder.set_alignment(config['alignment'])
        
        # Size policy
        if 'size_policy' in config:
            horizontal, vertical = config['size_policy']
            builder.set_size_policy(horizontal, vertical)
            
        return builder.build()
    
    @staticmethod
    def construct_from_preset(builder: BaseWidgetBuilder, preset_name: str) -> QWidget:
        """
        Constructs a widget using a predefined preset
        
        :param builder: The widget builder to use
        :param preset_name: Name of the preset to apply
        :return: The constructed widget
        """
        presets = {
            'header': {
                'font_size': 16,
                'font_bold': True,
                'alignment': Qt.AlignmentFlag.AlignCenter
            },
            'form_input': {
                'font_size': 12,
                'fixed_size': (200, 30),
            },
            'action_button': {
                'font_size': 16,
                'font_bold': True,
                'fixed_size': (200, 60),
            }
        }
        
        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}")
        
        return WidgetDirector.construct_basic_widget(builder, presets[preset_name])
        
    @staticmethod
    def apply_widget_callback(
        widget: QWidget, 
        event_type: str, 
        callback: Callable[[], None]
    ) -> QWidget:
        """
        Applies a callback to a widget's event
        
        :param widget: The widget to apply the callback to
        :param event_type: The event type to connect ('clicked', 'textChanged', etc.)
        :param callback: The callback function to connect
        :return: The widget with applied callback
        """
        if hasattr(widget, event_type):
            signal = getattr(widget, event_type)
            if hasattr(signal, 'connect'):
                signal.connect(callback)
            
        return widget