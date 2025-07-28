# UI Builder System

This directory contains the implementation of a comprehensive UI builder system following the Builder design pattern.

## Overview

The UI builder system provides a flexible way to construct complex UI components using a fluent interface. It follows several design patterns:

- **Builder Pattern**: For step-by-step construction of UI components
- **Director Pattern**: For coordinating the building process
- **Factory Pattern**: For creating appropriate builders
- **Object Pool Pattern**: For reusing builders to improve performance

## Architecture

The system is organized into the following components:

### Core Components

- `builder_interface.py`: Defines the abstract `Builder` interface that all builders implement
- `utils/`: Utility classes for validation and object pooling
- `directors/`: Classes that orchestrate the building process

### Builders

- `widgets/`: Builders for individual UI widgets (labels, buttons, etc.)
- `layouts/`: Builders for UI layouts (grid, form, box layouts, etc.)

## Usage Examples

### Basic Widget Creation

```python
# Create a label using the builder pattern
label = (
    widget_factory.get("label")
    .set_text("Hello World")
    .set_font_size(16)
    .set_font_bold(True)
    .build()
)
```

### Using Directors

Directors help standardize complex UI construction:

```python
# Create a button with a preset configuration
button_builder = widget_factory.get("button")
button = WidgetDirector.construct_from_preset(button_builder, "action_button")

# Create a layout with custom configuration
layout_builder = layout_factory.get("vbox")
layout = LayoutDirector.construct_basic_layout(layout_builder, {
    "margin": 10,
    "spacing": 5,
    "alignment": Qt.AlignmentFlag.AlignCenter
})
```

### Builder Object Pooling

For performance-critical applications, use the builder pool:

```python
# Get a builder from the pool
button_builder = BuilderPoolRegistry.acquire_builder(ButtonWidgetBuilder)

# Configure the builder
button = button_builder.set_text("Click me").build()

# Release the builder back to the pool when done
BuilderPoolRegistry.release_builder(button_builder)
```

## Validation

All builders include validation to ensure proper usage:

```python
# This will raise a ValidationError if width or height is negative
widget_builder.set_fixed_size(width=-10, height=30)
```

## Adding New Builders

To add a new widget builder:

1. Create a new class that extends `BaseWidgetBuilder`
2. Override the `build()` method to create your widget
3. Add any widget-specific configuration methods

Example:

```python
class ProgressBarWidgetBuilder(BaseWidgetBuilder):
    def __init__(self):
        super().__init__()
        self._widget = QProgressBar()
        self._min_value = 0
        self._max_value = 100
        self._value = 0
    
    def set_range(self, min_value: int, max_value: int) -> Self:
        validate_type(min_value, "min_value", int)
        validate_type(max_value, "max_value", int)
        validate_with_function(
            max_value > min_value,
            "max_value",
            lambda x: x,
            "max_value must be greater than min_value"
        )
        
        self._min_value = min_value
        self._max_value = max_value
        return self
    
    def set_value(self, value: int) -> Self:
        validate_type(value, "value", int)
        self._value = value
        return self
    
    def build(self) -> QProgressBar:
        self._widget.setRange(self._min_value, self._max_value)
        self._widget.setValue(self._value)
        self._apply_common_properties()
        return self._widget
```

## Best Practices

1. Always use the fluent interface for method chaining
2. Use directors for complex component construction
3. Add validation to all methods that accept parameters
4. Standardize attribute protection with single underscore prefix
5. Consider using the object pool for frequently used builders