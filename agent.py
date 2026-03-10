"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Main Agent Controller                  ║
║      Powered by Kimi K2.5 via NVIDIA API         ║
╚══════════════════════════════════════════════════╝
"""

import json
import re
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
        self.system_prompt = """You are DELTON AI — an elite AI video montage director and editor.
You think and plan like a professional filmmaker with 20+ years of After Effects and Premiere Pro experience.

YOUR ROLE: Analyze user requests and generate DETAILED JSON montage plans that a rendering engine can execute.

AVAILABLE TRANSITIONS: fade, crossfade, zoom_in, zoom_out, whip_pan_left, whip_pan_right, whip_pan_up, whip_pan_down, glitch, rgb_split, light_leak, luma_fade, spin, slice_horizontal, slice_vertical, film_burn, dissolve, wipe_left, wipe_right, wipe_up, wipe_down, circle_reveal, diamond_reveal, pixelate, blur_transition, flash_white, flash_black

AVAILABLE COLOR GRADES: cinematic_teal_orange, warm_golden, cool_blue, dark_moody, vintage_film, neon_cyberpunk, clean_bright, bw_dramatic, pastel_soft, luxury_dark_gold

AVAILABLE AD STYLES: apple_clean, nike_bold, luxury_elegance, tech_modern, social_viral, cinematic_story

AVAILABLE ICONS (Lucide): zap, rocket, shield, lock, star, award, crown, headphones, message_circle, globe, dollar_sign, clock, settings, bar_chart, trending_up, cloud, download, play, video, camera, image, music, heart, check_circle, arrow_right, user, users, smartphone, monitor, brain, sparkles, film, scissors, palette, volume_2, layers, target, eye, sun, moon, send

AVAILABLE SOUND EFFECTS: whoosh, impact, riser, pop, click, shimmer, bass_drop, reverse_cymbal, notification, sweep

SPEED EFFECTS: normal (1.0), slow_motion (0.3-0.5), fast (1.5-3.0), speed_ramp (variable), reverse, freeze_frame

VFX OPTIONS: particles_dust, particles_sparks, particles_bokeh, particles_snow, particles_rain, light_rays, lens_flare, screen_shake, split_screen_2, split_screen_3, split_screen_4, vignette, film_grain, blur_background, glow, chromatic_aberration

TEXT ANIMATIONS: fade_in, slide_up, slide_down, slide_left, slide_right, scale_up, scale_down, bounce, typewriter, glitch_text, blur_in, rotate_in, flip_in, wave, kinetic_pop

RESPONSE FORMAT — You MUST respond with valid JSON in this exact structure:

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
                    "counter_start": "int or null",
                    "counter_end": "int or null"
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
        "grain_intensity": 0.05,
        "letterbox": false,
        "letterbox_ratio": 2.35
    },
    "export": {
        "format": "mp4",
        "codec": "libx264",
        "bitrate": "8000k",
        "audio": true
    }
}

IMPORTANT RULES:
1. ALWAYS respond with ONLY valid JSON — no markdown, no explanations outside JSON
2. Create at least 5 scenes for any video
3. Every scene MUST have at least one element
4. Use diverse transitions — don't repeat the same one
5. Color choices must match the mood
6. For premium ads, think Apple/Nike/Samsung quality
7. Timing must be precise and add up correctly
8. Position uses percentages (0-100) for x and y
9. Size is a scale factor (1.0 = default, 2.0 = double)
10. Include sound effects for major transitions and reveals"""

        self.conversation_history = [
            {"role": "system", "content": self.system_prompt}
        ]

    def activate_premium_mode(self):
        """Activate Premium Ad Agent mode."""
        self.mode = "premium_ad"
        premium_context = """
PREMIUM AD MODE ACTIVATED. You are now creating After Effects-quality advertisements.
Apply these premium principles:
- Every animation uses ease-in-out (smooth)
- Overshoot/bounce on text entrances
- Stagger animations (elements appear sequentially, not all at once)
- Use anticipation → action → follow-through
- Maximum 3 colors per composition
- 60-30-10 color rule
- Glassmorphism and gradient mesh for modern feel
- Depth of field blur on backgrounds
- Subtle particle overlays
- Premium sound design on every transition
- Think: Apple ads, Nike ads, Samsung ads level quality
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

        # Add user message
        self.conversation_history.append(
            {"role": "user", "content": user_request}
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
                if chunk.choices[0].delta.content is not None:
                    response_text += chunk.choices[0].delta.content

            # Save to history
            self.conversation_history.append(
                {"role": "assistant", "content": response_text}
            )

            # Parse JSON from response
            montage_plan = self._parse_json_response(response_text)
            self.current_project = montage_plan
            return montage_plan

        except Exception as e:
            print(f"[DELTON AI] Error communicating with Kimi K2.5: {e}")
            return self._generate_fallback_plan(user_request)

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
        # Try direct parse first
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON in the response
        json_patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'(\{.*\})',
        ]

        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue

        # If nothing works, try cleaning the response
        cleaned = response_text.strip()
        if cleaned.startswith('{'):
            # Find the last closing brace
            brace_count = 0
            end_idx = 0
            for i, char in enumerate(cleaned):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            try:
                return json.loads(cleaned[:end_idx])
            except json.JSONDecodeError:
                pass

        print("[DELTON AI] Warning: Could not parse AI response as JSON. Using fallback.")
        return self._generate_fallback_plan("default montage")

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