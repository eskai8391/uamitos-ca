from typing import Dict, Any, List, Optional
from PySide6.QtWidgets import QWidget, QLayout

from presentation.ui.builders.layouts.base_layout_builder import BaseLayoutBuilder


class LayoutDirector:
    """
    Director class that coordinates the layout building process.
    The Director defines the order in which to execute the building steps.
    """

    @staticmethod
    def construct_basic_layout(
        builder: BaseLayoutBuilder, 
        config: Dict[str, Any]
    ) -> QLayout:
        """
        Constructs a layout with basic configuration
        
        :param builder: The layout builder to use
        :param config: Configuration dictionary with layout properties
        :return: The constructed layout
        """
        if 'margin' in config:
            builder.set_margin(config['margin'])
            
        if 'spacing' in config:
            builder.set_spacing(config['spacing'])
            
        if 'alignment' in config:
            builder.set_alignment(config['alignment'])
            
        if 'fixed_size' in config:
            width, height = config['fixed_size']
            builder.set_fixed_size(width, height)
            
        if 'style_sheet' in config:
            css = config.get('style_sheet')
            builder.set_style_sheet(css=css)
            
        if 'style_sheet_path' in config:
            path = config.get('style_sheet_path')
            builder.set_style_sheet(route=path)
            
        if 'class_name' in config:
            builder.set_class(config['class_name'])
        
        # Add widgets if provided
        if 'widgets' in config:
            for widget in config['widgets']:
                builder.add_widget(widget)
                
        return builder.build()
    
    @staticmethod
    def construct_from_preset(
        builder: BaseLayoutBuilder, 
        preset_name: str
    ) -> QLayout:
        """
        Constructs a layout using a predefined preset
        
        :param builder: The layout builder to use
        :param preset_name: Name of the preset to apply
        :return: The constructed layout
        """
        presets = {
            'form_container': {
                'margin': 20,
                'spacing': 10,
                'class_name': 'form-container'
            },
            'content_section': {
                'margin': 15,
                'spacing': 8,
                'class_name': 'content-section'
            },
            'header_section': {
                'margin': 10,
                'spacing': 5,
                'alignment': 0x0084,  # Qt.AlignmentFlag.AlignCenter
                'class_name': 'header-section'
            }
        }
        
        if preset_name not in presets:
            raise ValueError(f"Unknown preset: {preset_name}")
        
        return LayoutDirector.construct_basic_layout(builder, presets[preset_name])
        
    @staticmethod
    def add_widgets_to_layout(
        builder: BaseLayoutBuilder, 
        widgets: List[QWidget]
    ) -> BaseLayoutBuilder:
        """
        Adds multiple widgets to a layout builder
        
        :param builder: The layout builder to modify
        :param widgets: List of widgets to add
        :return: The modified builder (for method chaining)
        """
        for widget in widgets:
            builder.add_widget(widget)
        return builder