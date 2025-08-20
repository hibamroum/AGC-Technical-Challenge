from typing import Optional

# Focused on women’s safety in public spaces (not generic culture)
SAFETY_KEYWORDS = {
    "safety", "public", "street", "harass", "harassment", "catcall", "stalk", "stalking",
    "bus", "metro", "taxi", "rideshare", "self-defense", "crowded", "night", "lighting",
    "route", "panic", "report", "police", "hotline", "bystander", "assault", "followed",
    "escort", "commute", "station", "platform", "parking", "alley",
}

BLOCK_MSG = (
    "This assistant only answers questions about **women’s safety in public spaces**. "
    "Please rephrase toward harassment, transit, reporting, bystander tips, night routes, etc."
)

def enforce_public_safety_only(user_message: str) -> Optional[str]:
    text = (user_message or "").lower()
    if not any(k in text for k in SAFETY_KEYWORDS):
        return BLOCK_MSG
    return None

def sanitize(text: str, max_len: int = 4000) -> str:
    """Basic input sanitation and defensive length cap."""
    return (text or "").strip()[:max_len]
