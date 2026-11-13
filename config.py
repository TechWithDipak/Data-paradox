"""
Configuration and styling constants for RetailCo Churn Analysis System.
Enhanced multi-colored, professional, high-contrast palette.
"""

APP_TITLE = "RetailCo – Customer Churn Analysis System"
APP_SUBTITLE = "MECE Issue Tree Investigation & Strategic Root Cause Validation"
ACADEMIC_META = "SRMIST • 21IPE341T: Mastering the Data Paradox with AI & ML • Case Study Part B"

# Primary Brand & Accent Palette
COLORS = {
    "primary": "#1E1B4B",       # Deep Indigo
    "secondary": "#2563EB",     # Electric Royal Blue
    "accent_cyan": "#06B6D4",   # Bright Cyan
    "accent_purple": "#8B5CF6", # Vivid Violet
    "accent_pink": "#EC4899",   # Vibrant Rose Pink
    "success": "#10B981",       # Emerald Green
    "warning": "#F59E0B",       # Radiant Amber
    "danger": "#EF4444",        # Crimson Red
    "neutral_dark": "#1F2937",  # Charcoal Dark
    "neutral_light": "#F8FAFC", # Clean Light Canvas
    "card_bg": "#FFFFFF",       # Pure White Card
    "border": "#E2E8F0"         # Slate Border
}

# Dedicated City / Location Colors
CITY_COLORS = {
    "Hyderabad": "#EF4444",   # Vivid Crimson (Critical Hotspot)
    "Chennai": "#F97316",     # Warm Amber Orange (Secondary Hotspot)
    "Bangalore": "#06B6D4",   # Electric Cyan (Tech Center)
    "Delhi": "#8B5CF6",       # Vibrant Royal Violet (North Hub)
    "Mumbai": "#10B981"       # Fresh Emerald Green (Top Retained)
}

# Dedicated Loyalty Tier Colors
TIER_COLORS = {
    "Gold": "#F59E0B",        # Radiant Amber Gold
    "Silver": "#64748B",      # Sleek Slate Silver
    "Bronze": "#EA580C"       # Burnished Copper Bronze
}

# Dedicated Gender Colors
GENDER_COLORS = {
    "M": "#2563EB",           # Royal Cobalt Blue
    "F": "#EC4899"            # Vibrant Magenta Pink
}

# Dedicated Age Cohort Colors
AGE_COLORS = {
    "18-25": "#06B6D4",       # Teal / Cyan
    "26-35": "#3B82F6",       # Blue
    "36-45": "#8B5CF6",       # Violet
    "46+": "#EC4899"          # Rose
}

# Dedicated AI Recommendation Product Categories
CATEGORY_COLORS = {
    "Sarees": "#EC4899",      # Vivid Pink
    "Kurtas": "#8B5CF6",      # Purple
    "Jeans": "#2563EB",       # Royal Blue
    "T-Shirts": "#06B6D4",    # Cyan
    "Shoes": "#F59E0B",       # Amber
    "Watches": "#10B981",     # Emerald
    "Bags": "#F97316"         # Bright Orange
}

# Dedicated Marketing Channel Colors
CHANNEL_COLORS = {
    "Instagram": "#E1306C",   # Brand Magenta / Instagram Rose
    "Facebook": "#1877F2",    # Brand Royal Blue
    "App Push": "#10B981",    # Emerald Green
    "SMS": "#F59E0B",         # Amber Orange
    "Email": "#8B5CF6"        # Deep Violet
}

# Validation Status Styling (MECE Tree)
STATUS_CONFIG = {
    "Supported": {
        "badge_color": "#DCFCE7",
        "text_color": "#15803D",
        "border_color": "#86EFAC",
        "icon": ""
    },
    "Partially Supported": {
        "badge_color": "#FEF3C7",
        "text_color": "#B45309",
        "border_color": "#FCD34D",
        "icon": ""
    },
    "Not Testable": {
        "badge_color": "#F1F5F9",
        "text_color": "#475569",
        "border_color": "#CBD5E1",
        "icon": ""
    }
}
