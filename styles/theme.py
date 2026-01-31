# Frame_Ayirici/styles/theme.py
"""
Theme configuration for Frame Extractor application.
Centralized color palette and styling constants.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Colors:
    """Color palette for the application."""
    
    # Primary colors
    primary: str = "#00D1FF"
    primary_hover: str = "#50E3FF"
    primary_pressed: str = "#00A8CC"
    
    # Secondary/Accent colors
    secondary: str = "#50E3C2"
    accent: str = "#B298DC"
    warning: str = "#FFD600"
    error: str = "#FF6B6B"
    success: str = "#4CAF50"
    
    # Background colors
    bg_dark: str = "#1E1B32"
    bg_light: str = "#342F5C"
    bg_card: str = "rgba(255, 255, 255, 0.05)"
    
    # Text colors
    text_primary: str = "#E0E0E0"
    text_secondary: str = "#AAAAAA"
    text_muted: str = "#888888"
    
    # Border colors
    border: str = "rgba(255, 255, 255, 0.1)"
    border_hover: str = "rgba(255, 255, 255, 0.2)"
    
    # Shadow
    shadow: str = "rgba(0, 0, 0, 0.3)"


@dataclass(frozen=True)
class Dimensions:
    """Dimension constants for UI elements."""
    
    # Border radius
    radius_small: int = 8
    radius_medium: int = 12
    radius_large: int = 16
    
    # Spacing
    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 16
    spacing_lg: int = 24
    spacing_xl: int = 32
    
    # Component sizes
    button_height: int = 45
    input_height: int = 40
    card_padding: int = 20


@dataclass(frozen=True)
class Animation:
    """Animation timing constants."""
    
    duration_fast: int = 150
    duration_normal: int = 250
    duration_slow: int = 400
    
    easing_default: str = "Easing.OutCubic"
    easing_bounce: str = "Easing.OutBack"


class Theme:
    """
    Main theme class that provides access to all styling constants.
    
    Usage:
        theme = Theme()
        print(theme.colors.primary)
        print(theme.dimensions.radius_medium)
    """
    
    colors = Colors()
    dimensions = Dimensions()
    animation = Animation()
    
    @classmethod
    def to_qml_properties(cls) -> Dict[str, Any]:
        """
        Export theme as dictionary for QML consumption.
        
        Returns:
            Dictionary containing all theme values
        """
        return {
            'colors': {
                'primary': cls.colors.primary,
                'primaryHover': cls.colors.primary_hover,
                'primaryPressed': cls.colors.primary_pressed,
                'secondary': cls.colors.secondary,
                'accent': cls.colors.accent,
                'warning': cls.colors.warning,
                'error': cls.colors.error,
                'success': cls.colors.success,
                'bgDark': cls.colors.bg_dark,
                'bgLight': cls.colors.bg_light,
                'bgCard': cls.colors.bg_card,
                'textPrimary': cls.colors.text_primary,
                'textSecondary': cls.colors.text_secondary,
                'textMuted': cls.colors.text_muted,
                'border': cls.colors.border,
                'borderHover': cls.colors.border_hover,
            },
            'dimensions': {
                'radiusSmall': cls.dimensions.radius_small,
                'radiusMedium': cls.dimensions.radius_medium,
                'radiusLarge': cls.dimensions.radius_large,
                'spacingSm': cls.dimensions.spacing_sm,
                'spacingMd': cls.dimensions.spacing_md,
                'spacingLg': cls.dimensions.spacing_lg,
                'buttonHeight': cls.dimensions.button_height,
                'inputHeight': cls.dimensions.input_height,
                'cardPadding': cls.dimensions.card_padding,
            },
            'animation': {
                'durationFast': cls.animation.duration_fast,
                'durationNormal': cls.animation.duration_normal,
                'durationSlow': cls.animation.duration_slow,
            }
        }
