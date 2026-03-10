"""
╔══════════════════════════════════════════════════╗
║  Skill 10: Premium Ad Creation                   ║
╚══════════════════════════════════════════════════╝
"""

from config import AD_STYLES


class PremiumAdCreator:
    """
    Enhances plans with premium ad characteristics:
    Apple / Nike / Samsung quality design principles.
    """

    STAGGER_DELAY = 0.12   # seconds between element entrances
    OVERSHOOT = 1.08       # scale overshoot factor for bounce animations

    def enhance_plan(self, plan: dict) -> dict:
        """Add premium polish to a plan in-place and return it."""
        ad_style = plan.get("ad_style")
        style_config = AD_STYLES.get(ad_style, {})

        for scene in plan.get("scenes", []):
            self._stagger_elements(scene)
            self._upgrade_transitions(scene, ad_style)
            self._apply_vignette(scene)

        return plan

    def _stagger_elements(self, scene: dict):
        """Give each element a sequential delay so they don't all appear at once."""
        for i, element in enumerate(scene.get("elements", [])):
            existing_delay = element.get("animation_in_delay", 0.0)
            element["animation_in_delay"] = existing_delay + i * self.STAGGER_DELAY

            # Upgrade simple fade_in to bounce for headings
            if element.get("animation_in") == "fade_in" and element.get("type") == "text":
                element["animation_in"] = "scale_up"

    def _upgrade_transitions(self, scene: dict, ad_style: str):
        """Replace generic transitions with premium ones per ad style."""
        upgrades = {
            "apple_clean":      ("luma_fade",    "luma_fade"),
            "nike_bold":        ("flash_black",  "rgb_split"),
            "luxury_elegance":  ("light_leak",   "light_leak"),
            "tech_modern":      ("glitch",       "rgb_split"),
            "social_viral":     ("zoom_in",      "zoom_out"),
            "cinematic_story":  ("crossfade",    "crossfade"),
        }
        trans_in, trans_out = upgrades.get(ad_style, ("crossfade", "crossfade"))
        if not scene.get("transition_in"):
            scene["transition_in"] = trans_in
        if not scene.get("transition_out"):
            scene["transition_out"] = trans_out

    def _apply_vignette(self, scene: dict):
        """Ensure premium scenes always have a vignette VFX."""
        vfx = scene.setdefault("vfx", [])
        if "vignette" not in vfx:
            vfx.insert(0, "vignette")

    def get_color_palette(self, ad_style: str) -> dict:
        """Return the bg/text/accent colors for a given ad style."""
        style = AD_STYLES.get(ad_style, {})
        return {
            "bg":     style.get("bg_color",      (10, 10, 10)),
            "text":   style.get("text_color",    (255, 255, 255)),
            "accent": style.get("accent_color",  (100, 100, 255)),
        }
