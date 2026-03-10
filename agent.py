"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Main Agent Controller                  ║
║      Powered by Kimi K2.5 via NVIDIA API         ║
╚══════════════════════════════════════════════════╝
"""

import json
import re
import random
import time as _time
from openai import OpenAI
from config import (
    NVIDIA_BASE_URL, NVIDIA_API_KEY, NVIDIA_MODEL,
    AI_TEMPERATURE, AI_TOP_P, AI_MAX_TOKENS,
    COLOR_GRADES, TRANSITIONS, AD_STYLES,
    DEFAULT_RESOLUTION, DEFAULT_FPS
)


class DeltonAgent:
    """
    DELTON AI Agent — The brain that plans and directs video montages.
    Uses Kimi K2.5 model via NVIDIA API endpoint.
    """

    def __init__(self):
        self.client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY
        )
        self.model = NVIDIA_MODEL
        self.conversation_history = []
        self.current_project = None
        self.mode = "standard"  # standard or premium_ad

        # Initialize system prompt
        self._init_system_prompt()

    def _init_system_prompt(self):
        """Initialize the master system prompt for DELTON AI."""
        self.system_prompt = """You are DELTON AI — an elite motion-design director and After Effects master with 20+ years crafting world-class ads for Apple, Nike, Samsung, and top Facebook/Instagram campaigns.

YOUR ROLE: Receive a creative brief and output a UNIQUE, PREMIUM, production-ready JSON montage plan every single time. Each plan must be visually distinct from anything previously generated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREMIUM MOTION DESIGN PRINCIPLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• EASING: All animations use ease-in-out. No linear motion ever.
• STAGGER: Elements appear sequentially — never all at once. Add 0.10–0.18s delay between each element.
• BREATHING ROOM: Give text space. Use large font sizes (2.5–5.0) and generous vertical spacing.
• 3-COLOR RULE: Max 3 colors per scene. Pick a dominant, secondary, and accent.
• 60-30-10 RULE: 60% background, 30% main element color, 10% accent.
• MICRO-ANIMATIONS: Icons subtly pulse or rotate. Text has slight scale-up on hold.
• HOLD FRAMES: Important messages stay visible for at least 1.5s before exit animation.
• SMOOTH EXITS: Exit animation_out_delay must give content time to breathe before leaving.
• SOUND DESIGN: Every transition has a matching sound. Every text reveal has a subtle pop/shimmer.
• PACING: Hook in first 2s. Build tension. Release at climax. Calm CTA close.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STYLE REFERENCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Apple: Pure white/black bg, San Francisco-style type, slow zoom, whisper-quiet sound, luma_fade transitions, one bold product claim per scene.
• Facebook/Instagram Ads: Hook within 2s, bold color, high contrast, fast-paced (8–15 scenes), zoom_in/whip_pan, social_viral style, portrait format preferred.
• Nike: Dark bg, high contrast, fast cuts, impact sounds, glitch/flash_black transitions, kinetic typography.
• Luxury/Premium: Black gold palette, elegant font, light_leak transitions, slow builds, orchestral feel, film_grain on.
• Tech SaaS: Deep blue/cyan, glassmorphism, blur_transition, counter elements showing stats, particles_bokeh.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AVAILABLE OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSITIONS: fade, crossfade, zoom_in, zoom_out, whip_pan_left, whip_pan_right, whip_pan_up, whip_pan_down, glitch, rgb_split, light_leak, luma_fade, spin, slice_horizontal, slice_vertical, film_burn, dissolve, wipe_left, wipe_right, wipe_up, wipe_down, circle_reveal, diamond_reveal, pixelate, blur_transition, flash_white, flash_black

COLOR GRADES: cinematic_teal_orange, warm_golden, cool_blue, dark_moody, vintage_film, neon_cyberpunk, clean_bright, bw_dramatic, pastel_soft, luxury_dark_gold

AD STYLES: apple_clean, nike_bold, luxury_elegance, tech_modern, social_viral, cinematic_story

ICONS: zap, rocket, shield, lock, star, award, crown, headphones, message_circle, globe, dollar_sign, clock, settings, bar_chart, trending_up, cloud, download, play, video, camera, image, music, heart, check_circle, arrow_right, user, users, smartphone, monitor, brain, sparkles, film, scissors, palette, volume_2, layers, target, eye, sun, moon, send

SOUND EFFECTS: whoosh, impact, riser, pop, click, shimmer, bass_drop, reverse_cymbal, notification, sweep

SPEED EFFECTS: normal (1.0), slow_motion (0.3–0.5), fast (1.5–3.0), speed_ramp, reverse, freeze_frame

VFX: particles_dust, particles_sparks, particles_bokeh, particles_snow, particles_rain, light_rays, lens_flare, screen_shake, split_screen_2, split_screen_3, split_screen_4, vignette, film_grain, blur_background, glow, chromatic_aberration

TEXT ANIMATIONS: fade_in, slide_up, slide_down, slide_left, slide_right, scale_up, scale_down, bounce, typewriter, glitch_text, blur_in, rotate_in, flip_in, wave, kinetic_pop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT OUTPUT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Respond with ONLY valid JSON — zero markdown, zero explanation outside the JSON.
2. Minimum 6 scenes. Premium ads: 8–12 scenes.
3. Every scene has 2–5 elements with staggered delays.
4. NEVER use the same transition twice in a row. Vary them across scenes.
5. NEVER generate the same plan twice — use the style, product, and mood to make it unique.
6. Timings must be exact and cumulative (start_time of scene N = end_time of scene N-1).
7. Positions: percentages 0–100 for x and y. Center = [50, 50].
8. Size: scale factor. 1.0 = default. Headings: 2.5–5.0. Body: 1.0–1.8.
9. animation_out must be a valid exit animation (e.g. scale_down, fade_in, slide_down).
10. animation_out_delay must be: scene duration - 0.3s (leave room for exit).
11. Total bitrate for premium: use "12000k". For social: "8000k".
12. For Facebook/Instagram ads: use portrait format [1080, 1920] and fps: 30.
13. For Apple/Luxury ads: use landscape [1920, 1080], fps: 30, letterbox: true.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED JSON STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{
    "project_name": "string",
    "description": "string",
    "format": "landscape|portrait|square",
    "resolution": [width, height],
    "fps": 30,
    "total_duration": float_seconds,
    "color_grade": "grade_name",
    "ad_style": "style_name or null",
    "music": {
        "style": "string",
        "bpm": int,
        "mood": "string"
    },
    "scenes": [
        {
            "scene_id": 1,
            "name": "string",
            "start_time": 0.0,
            "end_time": 3.0,
            "duration": 3.0,
            "type": "hook|intro|content|build|climax|outro|cta",
            "background": {
                "type": "solid|gradient|image|video",
                "color": [r, g, b] or null,
                "gradient_start": [r, g, b] or null,
                "gradient_end": [r, g, b] or null,
                "gradient_direction": "horizontal|vertical|diagonal|radial"
            },
            "elements": [
                {
                    "type": "text|icon|shape|image|counter|progress_bar",
                    "content": "string",
                    "position": [x_percent, y_percent],
                    "size": float_scale,
                    "color": [r, g, b],
                    "font": "font_name or null",
                    "animation_in": "animation_name",
                    "animation_out": "animation_name",
                    "animation_in_delay": float_seconds,
                    "animation_in_duration": float_seconds,
                    "animation_out_delay": float_seconds,
                    "icon_name": "icon_name or null",
                    "counter_start": null,
                    "counter_end": null
                }
            ],
            "transition_in": "transition_name or null",
            "transition_in_duration": 0.5,
            "transition_out": "transition_name or null",
            "transition_out_duration": 0.5,
            "speed_effect": "normal|slow_motion|fast|speed_ramp",
            "speed_value": 1.0,
            "vfx": ["effect1", "effect2"],
            "sound_effects": [
                {
                    "type": "effect_name",
                    "time": float_seconds_from_scene_start
                }
            ]
        }
    ],
    "global_effects": {
        "vignette": true,
        "film_grain": false,
        "grain_intensity": 0.04,
        "letterbox": false,
        "letterbox_ratio": 2.35
    },
    "export": {
        "format": "mp4",
        "codec": "libx264",
        "bitrate": "12000k",
        "audio": true
    }
}"""

        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def activate_premium_mode(self):
        """Activate Premium Ad Agent mode."""
        self.mode = "premium_ad"
        premium_context = """
╔══════════════════════════════════════════════════╗
║          PREMIUM AD DIRECTOR MODE                ║
╚══════════════════════════════════════════════════╝

You are now operating as a world-class motion design director.
Every plan you generate must feel like a $500,000 broadcast commercial.

MANDATORY PREMIUM RULES:
━━━━━━━━━━━━━━━━━━━━━━━━
① FORMAT
   • Portrait [1080×1920] for Facebook/Instagram/TikTok ads
   • Landscape [1920×1080] for YouTube/TV/Apple style
   • Always use fps: 30, bitrate: "12000k"

② SCENE STRUCTURE (minimum 8 scenes)
   • Scene 1 — HOOK (0–2s): Bold single statement. Grab attention immediately.
   • Scene 2 — PROBLEM / TENSION (2–5s): Establish what the viewer is missing.
   • Scene 3–5 — FEATURES (5–12s): One key benefit per scene. Icon + text pairing.
   • Scene 6–7 — PROOF / SOCIAL (12–18s): Counter elements, stats, or testimonial copy.
   • Scene 8 — CLIMAX (18–21s): Brand moment. Big logo or product name. Lens flare.
   • Scene 9 — CTA (21–25s): Single clear call-to-action. Minimal. Centered.

③ ANIMATION QUALITY
   • Entrance durations: 0.4–0.7s (never faster, never slower)
   • Always stagger elements: 0.12s delay between each element in a scene
   • Use kinetic_pop or scale_up for headings — never plain fade_in for hero text
   • Exit (animation_out_delay) = scene duration − 0.4s

④ COLOR & AESTHETICS
   • Maximum 3 colors. 60-30-10 rule strictly enforced.
   • Background must be intentional: black, white, deep navy, or a rich gradient
   • Accent color must pop against the background (high contrast)
   • Use glow VFX on accent-colored icons
   • Apply vignette on every scene

⑤ TRANSITIONS (vary every single scene)
   • Apple style: luma_fade, crossfade, zoom_in (slow, 0.6s)
   • Nike/Social: flash_black, rgb_split, whip_pan_right (fast, 0.25–0.35s)
   • Luxury: light_leak, film_burn, dissolve (elegant, 0.5s)
   • Never use the same transition twice in a row

⑥ SOUND DESIGN
   • Every transition: whoosh or impact
   • Every text reveal: pop or shimmer
   • Climax scene: bass_drop + riser combo
   • CTA scene: notification or soft shimmer

⑦ GLOBAL EFFECTS
   • vignette: true always
   • film_grain: true for luxury/cinematic, false for clean/tech
   • grain_intensity: 0.03–0.06 (subtle)
   • letterbox: true for Apple/cinematic styles (ratio 2.35)

Generate a plan that a senior Art Director at BBDO would approve on first pass.
"""
        self.conversation_history.append(
            {"role": "system", "content": premium_context}
        )

    def deactivate_premium_mode(self):
        """Return to standard mode."""
        self.mode = "standard"

    def generate_montage_plan(self, user_request: str) -> dict:
        """
        Send user request to Kimi K2.5 and get a montage plan.

        Args:
            user_request: What the user wants to create

        Returns:
            dict: Structured montage plan
        """
        # Check for premium mode trigger
        if "premium ad" in user_request.lower() or "premium mode" in user_request.lower():
            self.activate_premium_mode()

        # ── Reset history for every new generation so the AI never echoes
        # a previous plan. The refinement path (refine_plan) appends to the
        # existing history intentionally.
        self._init_system_prompt()
        if self.mode == "premium_ad":
            self.activate_premium_mode()

        # ── Uniqueness seed: timestamp + random adjective so the AI is
        # forced to think fresh on every call.
        _seed = f"{int(_time.time())}-{random.randint(1000, 9999)}"
        _vibes = random.choice([
            "bold and unexpected", "sleek and minimalist", "high-energy and kinetic",
            "dark and cinematic", "bright and optimistic", "neon and futuristic",
            "warm and emotional", "cold and corporate", "organic and natural",
            "maximalist and vibrant", "editorial and luxury", "raw and documentary",
        ])
        enriched_request = (
            f"{user_request}\n\n"
            f"[CREATIVE SEED: {_seed} | VISUAL VIBE: {_vibes}]\n"
            f"This must be a completely unique plan — do NOT reuse colors, scene order, "
            f"or transitions from any previous response. Surprise me.\n\n"
            f"CRITICAL: Your entire response must be a single valid JSON object. "
            f"No markdown fences, no explanation text, no preamble, no postamble. "
            f"Start your response with {{ and end it with }}. Nothing else."
        )

        # Add user message
        self.conversation_history.append(
            {"role": "user", "content": enriched_request}
        )

        try:
            # Call NVIDIA API with Kimi K2.5
            response_text = ""
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=AI_TEMPERATURE,
                top_p=AI_TOP_P,
                max_tokens=AI_MAX_TOKENS,
                stream=True
            )

            for chunk in completion:
                # Guard: some terminal chunks have empty choices list
                if not chunk.choices:
                    continue
                delta_content = chunk.choices[0].delta.content
                if delta_content is not None:
                    response_text += delta_content

        except Exception as e:
            print(f"[DELTON AI] Error communicating with Kimi K2.5: {e}")
            return self._generate_fallback_plan(user_request)

        # Save to history (useful if the user refines right after)
        self.conversation_history.append(
            {"role": "assistant", "content": response_text}
        )

        # Parse JSON from response (errors here should NOT trigger the fallback silently)
        montage_plan = self._parse_json_response(response_text)
        self.current_project = montage_plan
        return montage_plan

    def refine_plan(self, feedback: str) -> dict:
        """
        Refine the current montage plan based on user feedback.

        Args:
            feedback: User's feedback or modification request

        Returns:
            dict: Updated montage plan
        """
        refinement_prompt = f"""
The user wants to modify the current montage plan.
Their feedback: {feedback}

Please regenerate the COMPLETE updated JSON montage plan with the requested changes.
Keep everything else the same unless the change affects it.
Respond with ONLY valid JSON.
"""
        return self.generate_montage_plan(refinement_prompt)

    def _parse_json_response(self, response_text: str) -> dict:
        """Extract and parse JSON from AI response."""
        if not response_text or not response_text.strip():
            print("[DELTON AI] Warning: Empty response from AI.")
            return self._generate_fallback_plan("default montage")

        # 1. Direct parse — model returned pure JSON
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass

        # 2. Strip markdown fences (handles ```json...``` and ```...```)
        fence_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if fence_match:
            try:
                return json.loads(fence_match.group(1))
            except json.JSONDecodeError:
                pass

        # 3. Find the first '{' anywhere in the response and balance braces.
        #    This handles any preamble text the model adds before the JSON.
        first_brace = response_text.find('{')
        if first_brace != -1:
            brace_count = 0
            end_idx = first_brace
            for i in range(first_brace, len(response_text)):
                c = response_text[i]
                if c == '{':
                    brace_count += 1
                elif c == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            candidate = response_text[first_brace:end_idx]
            try:
                return json.loads(candidate)
            except json.JSONDecodeError:
                # JSON found but malformed — try json5-style repair: strip trailing commas
                repaired = re.sub(r',\s*([}\]])', r'\1', candidate)
                try:
                    return json.loads(repaired)
                except json.JSONDecodeError:
                    pass

        # 4. Nothing worked — save raw response for inspection
        self._debug_save_response(response_text)
        print("[DELTON AI] Warning: Could not parse AI response as JSON.")
        print("[DELTON AI] Raw response saved to output/debug_last_response.txt — check it to see what the model returned.")
        return self._generate_fallback_plan("default montage")

    def _debug_save_response(self, text: str):
        """Save raw AI response to a debug file for inspection."""
        import os
        os.makedirs("output", exist_ok=True)
        try:
            with open("output/debug_last_response.txt", "w", encoding="utf-8") as f:
                f.write(text)
        except Exception:
            pass

    def _generate_fallback_plan(self, request: str) -> dict:
        """Generate a basic fallback montage plan if AI fails."""
        return {
            "project_name": "DELTON_Montage",
            "description": f"Montage based on: {request}",
            "format": "landscape",
            "resolution": [1920, 1080],
            "fps": 30,
            "total_duration": 15.0,
            "color_grade": "cinematic_teal_orange",
            "ad_style": None,
            "music": {
                "style": "cinematic",
                "bpm": 120,
                "mood": "energetic"
            },
            "scenes": [
                {
                    "scene_id": 1,
                    "name": "Hook",
                    "start_time": 0.0,
                    "end_time": 3.0,
                    "duration": 3.0,
                    "type": "hook",
                    "background": {
                        "type": "gradient",
                        "color": None,
                        "gradient_start": [20, 20, 40],
                        "gradient_end": [40, 40, 80],
                        "gradient_direction": "vertical"
                    },
                    "elements": [
                        {
                            "type": "text",
                            "content": "DELTON AI",
                            "position": [50, 40],
                            "size": 3.0,
                            "color": [255, 255, 255],
                            "font": "heading",
                            "animation_in": "scale_up",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.2,
                            "animation_in_duration": 0.8,
                            "animation_out_delay": 2.5,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "text",
                            "content": "From Vision to Video",
                            "position": [50, 55],
                            "size": 1.5,
                            "color": [0, 200, 255],
                            "font": "body",
                            "animation_in": "slide_up",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.8,
                            "animation_in_duration": 0.6,
                            "animation_out_delay": 2.5,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        }
                    ],
                    "transition_in": None,
                    "transition_in_duration": 0.0,
                    "transition_out": "zoom_in",
                    "transition_out_duration": 0.5,
                    "speed_effect": "normal",
                    "speed_value": 1.0,
                    "vfx": ["particles_bokeh", "vignette"],
                    "sound_effects": [
                        {"type": "impact", "time": 0.2},
                        {"type": "shimmer", "time": 0.8}
                    ]
                },
                {
                    "scene_id": 2,
                    "name": "Content",
                    "start_time": 3.0,
                    "end_time": 8.0,
                    "duration": 5.0,
                    "type": "content",
                    "background": {
                        "type": "gradient",
                        "color": None,
                        "gradient_start": [15, 15, 35],
                        "gradient_end": [30, 30, 60],
                        "gradient_direction": "diagonal"
                    },
                    "elements": [
                        {
                            "type": "text",
                            "content": "Create Amazing Videos",
                            "position": [50, 30],
                            "size": 2.5,
                            "color": [255, 255, 255],
                            "font": "heading",
                            "animation_in": "slide_left",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.3,
                            "animation_in_duration": 0.7,
                            "animation_out_delay": 4.0,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "icon",
                            "content": "",
                            "position": [25, 60],
                            "size": 2.0,
                            "color": [0, 200, 255],
                            "font": None,
                            "animation_in": "bounce",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.8,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 4.0,
                            "icon_name": "film",
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "icon",
                            "content": "",
                            "position": [50, 60],
                            "size": 2.0,
                            "color": [255, 100, 100],
                            "font": None,
                            "animation_in": "bounce",
                            "animation_out": "fade_in",
                            "animation_in_delay": 1.2,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 4.0,
                            "icon_name": "sparkles",
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "icon",
                            "content": "",
                            "position": [75, 60],
                            "size": 2.0,
                            "color": [100, 255, 100],
                            "font": None,
                            "animation_in": "bounce",
                            "animation_out": "fade_in",
                            "animation_in_delay": 1.6,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 4.0,
                            "icon_name": "rocket",
                            "counter_start": None,
                            "counter_end": None
                        }
                    ],
                    "transition_in": "zoom_in",
                    "transition_in_duration": 0.5,
                    "transition_out": "whip_pan_right",
                    "transition_out_duration": 0.4,
                    "speed_effect": "normal",
                    "speed_value": 1.0,
                    "vfx": ["particles_dust", "vignette"],
                    "sound_effects": [
                        {"type": "whoosh", "time": 0.0},
                        {"type": "pop", "time": 0.8},
                        {"type": "pop", "time": 1.2},
                        {"type": "pop", "time": 1.6}
                    ]
                },
                {
                    "scene_id": 3,
                    "name": "Features",
                    "start_time": 8.0,
                    "end_time": 12.0,
                    "duration": 4.0,
                    "type": "build",
                    "background": {
                        "type": "solid",
                        "color": [10, 10, 25],
                        "gradient_start": None,
                        "gradient_end": None,
                        "gradient_direction": None
                    },
                    "elements": [
                        {
                            "type": "text",
                            "content": "Powered by AI",
                            "position": [50, 25],
                            "size": 2.0,
                            "color": [255, 215, 0],
                            "font": "heading",
                            "animation_in": "typewriter",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.2,
                            "animation_in_duration": 1.0,
                            "animation_out_delay": 3.5,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "icon",
                            "content": "",
                            "position": [50, 50],
                            "size": 4.0,
                            "color": [0, 245, 255],
                            "font": None,
                            "animation_in": "scale_up",
                            "animation_out": "fade_in",
                            "animation_in_delay": 1.0,
                            "animation_in_duration": 0.8,
                            "animation_out_delay": 3.5,
                            "icon_name": "brain",
                            "counter_start": None,
                            "counter_end": None
                        },
                        {
                            "type": "text",
                            "content": "Kimi K2.5 × NVIDIA",
                            "position": [50, 75],
                            "size": 1.2,
                            "color": [150, 150, 150],
                            "font": "accent",
                            "animation_in": "fade_in",
                            "animation_out": "fade_in",
                            "animation_in_delay": 1.5,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 3.5,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        }
                    ],
                    "transition_in": "whip_pan_right",
                    "transition_in_duration": 0.4,
                    "transition_out": "glitch",
                    "transition_out_duration": 0.3,
                    "speed_effect": "normal",
                    "speed_value": 1.0,
                    "vfx": ["glow", "particles_sparks"],
                    "sound_effects": [
                        {"type": "whoosh", "time": 0.0},
                        {"type": "riser", "time": 0.5},
                        {"type": "impact", "time": 1.0}
                    ]
                },
                {
                    "scene_id": 4,
                    "name": "Climax",
                    "start_time": 12.0,
                    "end_time": 14.0,
                    "duration": 2.0,
                    "type": "climax",
                    "background": {
                        "type": "gradient",
                        "color": None,
                        "gradient_start": [0, 50, 100],
                        "gradient_end": [100, 0, 50],
                        "gradient_direction": "diagonal"
                    },
                    "elements": [
                        {
                            "type": "text",
                            "content": "DELTON AI",
                            "position": [50, 45],
                            "size": 4.0,
                            "color": [255, 255, 255],
                            "font": "heading",
                            "animation_in": "kinetic_pop",
                            "animation_out": "scale_up",
                            "animation_in_delay": 0.1,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 1.5,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        }
                    ],
                    "transition_in": "glitch",
                    "transition_in_duration": 0.3,
                    "transition_out": "flash_white",
                    "transition_out_duration": 0.3,
                    "speed_effect": "normal",
                    "speed_value": 1.0,
                    "vfx": ["lens_flare", "particles_sparks", "screen_shake"],
                    "sound_effects": [
                        {"type": "bass_drop", "time": 0.0},
                        {"type": "impact", "time": 0.1}
                    ]
                },
                {
                    "scene_id": 5,
                    "name": "Outro CTA",
                    "start_time": 14.0,
                    "end_time": 15.0,
                    "duration": 1.0,
                    "type": "outro",
                    "background": {
                        "type": "solid",
                        "color": [0, 0, 0],
                        "gradient_start": None,
                        "gradient_end": None,
                        "gradient_direction": None
                    },
                    "elements": [
                        {
                            "type": "text",
                            "content": "Start Creating Now",
                            "position": [50, 50],
                            "size": 1.8,
                            "color": [0, 200, 255],
                            "font": "subheading",
                            "animation_in": "fade_in",
                            "animation_out": "fade_in",
                            "animation_in_delay": 0.2,
                            "animation_in_duration": 0.5,
                            "animation_out_delay": 0.8,
                            "icon_name": None,
                            "counter_start": None,
                            "counter_end": None
                        }
                    ],
                    "transition_in": "flash_white",
                    "transition_in_duration": 0.3,
                    "transition_out": "fade",
                    "transition_out_duration": 0.5,
                    "speed_effect": "normal",
                    "speed_value": 1.0,
                    "vfx": ["vignette"],
                    "sound_effects": [
                        {"type": "shimmer", "time": 0.2}
                    ]
                }
            ],
            "global_effects": {
                "vignette": True,
                "film_grain": False,
                "grain_intensity": 0.03,
                "letterbox": False,
                "letterbox_ratio": 2.35
            },
            "export": {
                "format": "mp4",
                "codec": "libx264",
                "bitrate": "8000k",
                "audio": True
            }
        }

    def get_project_summary(self) -> str:
        """Get a human-readable summary of the current project."""
        if not self.current_project:
            return "No project loaded."

        p = self.current_project
        summary = f"""
╔══════════════════════════════════════════════════╗
║          DELTON AI — PROJECT SUMMARY             ║
╠══════════════════════════════════════════════════╣
║  Project:    {p.get('project_name', 'Untitled'):<35}║
║  Format:     {p.get('format', 'landscape'):<35}║
║  Resolution: {str(p.get('resolution', [1920,1080])):<35}║
║  Duration:   {str(p.get('total_duration', 0)) + 's':<35}║
║  FPS:        {str(p.get('fps', 30)):<35}║
║  Color:      {p.get('color_grade', 'none'):<35}║
║  Scenes:     {str(len(p.get('scenes', []))):<35}║
║  Mode:       {self.mode:<35}║
╚══════════════════════════════════════════════════╝
"""
        # Scene list
        for scene in p.get('scenes', []):
            summary += f"\n  [{scene.get('start_time', 0):.1f}s - {scene.get('end_time', 0):.1f}s] "
            summary += f"{scene.get('name', 'Scene')} ({scene.get('type', 'content')})"
            summary += f" | Transition: {scene.get('transition_out', 'none')}"
            summary += f" | Elements: {len(scene.get('elements', []))}"
            summary += f" | VFX: {', '.join(scene.get('vfx', []))}"

        return summary

    def reset(self):
        """Reset the agent to initial state."""
        self.current_project = None
        self.mode = "standard"
        self._init_system_prompt()