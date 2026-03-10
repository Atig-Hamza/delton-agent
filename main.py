"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║           Main Application Entry Point           ║
║                                                  ║
║   AI Video Montage Tool                          ║
║   Powered by Kimi K2.5 via NVIDIA API            ║
║                                                  ║
║   "From Vision to Video"                         ║
╚══════════════════════════════════════════════════╝
"""

import sys
import os
import time
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import DeltonAgent
from engine.renderer import DeltonRenderer
from ui.terminal_ui import (
    console, show_banner, show_welcome, show_help,
    show_formats, show_styles, show_transitions,
    show_effects, show_icons, show_plan_summary,
    show_error, show_success, show_info,
    show_thinking, get_input
)


class DeltonApp:
    """Main DELTON AI Application."""

    def __init__(self):
        self.agent = DeltonAgent()
        self.renderer = DeltonRenderer()
        self.current_plan = None
        self.running = True

    def start(self):
        """Start the DELTON AI application."""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Show startup
        show_banner()
        time.sleep(0.5)
        show_welcome()

        # Main loop
        while self.running:
            try:
                user_input = get_input()

                if not user_input:
                    continue

                self._handle_command(user_input)

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
            except Exception as e:
                show_error(f"Unexpected error: {str(e)}")

    def _handle_command(self, user_input: str):
        """Process user commands and requests."""
        cmd = user_input.lower().strip()

        # ─── Exit Commands ───
        if cmd in ("exit", "quit", "q", "bye"):
            self._exit()
            return

        # ─── Help Commands ───
        if cmd == "help":
            show_help()
            return

        # ─── Format Commands ───
        if cmd == "formats":
            show_formats()
            return

        # ─── Style Commands ───
        if cmd == "styles":
            show_styles()
            return

        # ─── Transition Commands ───
        if cmd == "transitions":
            show_transitions()
            return

        # ─── Effects Commands ───
        if cmd == "effects":
            show_effects()
            return

        # ─── Icons Commands ───
        if cmd == "icons":
            show_icons()
            return

        # ─── Preview Commands ───
        if cmd in ("preview", "plan", "show", "summary"):
            if self.current_plan:
                show_plan_summary(self.current_plan)
            else:
                show_info("No montage plan created yet. Describe your video to get started!")
            return

        # ─── Reset Commands ───
        if cmd == "reset":
            self.agent.reset()
            self.current_plan = None
            show_success("Project reset. Ready for a new creation!")
            return

        # ─── Render Commands ───
        if cmd in ("render", "create", "generate", "build", "export"):
            self._render_video()
            return

        # ─── Save Plan Commands ───
        if cmd in ("save", "save plan"):
            self._save_plan()
            return

        # ─── Load Plan Commands ───
        if cmd.startswith("load "):
            filepath = cmd[5:].strip()
            self._load_plan(filepath)
            return

        # ─── Refine Commands ───
        if cmd.startswith("refine"):
            feedback = user_input[6:].strip()
            if not feedback:
                feedback = get_input()
            if feedback and self.current_plan:
                self._refine_plan(feedback)
            else:
                show_info("No plan to refine. Create one first!")
            return

        # ─── Premium Mode Commands ───
        if cmd in ("premium", "premium mode", "premium ad mode", "ad mode"):
            self.agent.activate_premium_mode()
            show_success("Premium Ad Agent ACTIVATED! 🏆 Creating After Effects-quality content.")
            show_info("Now describe your advertisement...")
            return

        # ─── Standard Mode Commands ───
        if cmd in ("standard", "standard mode", "normal mode"):
            self.agent.deactivate_premium_mode()
            show_success("Switched to Standard Mode.")
            return

        # ─── Default: Create Montage Plan ───
        self._create_plan(user_input)

    def _create_plan(self, user_request: str):
        """Create a new montage plan from user request."""
        show_thinking()

        console.print("[dim]   Connecting to Kimi K2.5 via NVIDIA API...[/dim]")
        start_time = time.time()

        # Generate plan via AI
        plan = self.agent.generate_montage_plan(user_request)

        elapsed = time.time() - start_time
        console.print(f"[dim]   AI response received in {elapsed:.1f}s[/dim]")

        if plan:
            self.current_plan = plan
            show_success(f"Montage plan created: \"{plan.get('project_name', 'Untitled')}\"")
            show_plan_summary(plan)

            console.print("\n[bold yellow]What would you like to do?[/bold yellow]")
            console.print("  [green]• Type 'render' to generate the video[/green]")
            console.print("  [green]• Type 'refine' + feedback to modify[/green]")
            console.print("  [green]• Type 'save' to save the plan[/green]")
            console.print("  [green]• Or describe a new video[/green]")
        else:
            show_error("Failed to generate montage plan. Try again with more detail.")

    def _refine_plan(self, feedback: str):
        """Refine the current plan."""
        show_thinking()
        console.print(f"[dim]   Refining plan with feedback: \"{feedback}\"[/dim]")

        plan = self.agent.refine_plan(feedback)

        if plan:
            self.current_plan = plan
            show_success("Plan refined successfully!")
            show_plan_summary(plan)
        else:
            show_error("Failed to refine plan.")

    def _render_video(self):
        """Render the current plan to video."""
        if not self.current_plan:
            show_error("No montage plan to render! Create one first by describing your video.")
            return

        console.print("\n[bold cyan]═══════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]  🎬 DELTON AI — VIDEO RENDERING      [/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════[/bold cyan]\n")

        # Confirm
        console.print(f"[white]Project: {self.current_plan.get('project_name', 'Untitled')}[/white]")
        console.print(f"[white]Duration: {self.current_plan.get('total_duration', 0)}s[/white]")
        console.print(f"[white]Resolution: {self.current_plan.get('resolution', [1920,1080])}[/white]")
        console.print(f"[white]Scenes: {len(self.current_plan.get('scenes', []))}[/white]")

        confirm = console.input("\n[yellow]Start rendering? (y/n): [/yellow]").strip().lower()
        if confirm not in ('y', 'yes', ''):
            show_info("Rendering cancelled.")
            return

        try:
            # Load plan into renderer
            self.renderer.load_plan(self.current_plan)

            # Render
            start_time = time.time()
            output_path = self.renderer.render()
            elapsed = time.time() - start_time

            if output_path and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                show_success(f"Video rendered successfully!")
                console.print(f"\n[bold white]   📁 Output: {output_path}[/bold white]")
                console.print(f"[bold white]   📊 Size: {file_size:.1f} MB[/bold white]")
                console.print(f"[bold white]   ⏱️  Time: {elapsed:.1f}s[/bold white]")
            else:
                show_error("Rendering failed — no output file created.")

        except Exception as e:
            show_error(f"Rendering error: {str(e)}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")

    def _save_plan(self):
        """Save the current plan to JSON."""
        if not self.current_plan:
            show_error("No plan to save!")
            return

        project_name = self.current_plan.get('project_name', 'delton_plan')
        safe_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in project_name)
        filepath = os.path.join("output", f"{safe_name}.json")

        os.makedirs("output", exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.current_plan, f, indent=2, ensure_ascii=False)

        show_success(f"Plan saved to: {filepath}")

    def _load_plan(self, filepath: str):
        """Load a plan from JSON file."""
        if not os.path.exists(filepath):
            show_error(f"File not found: {filepath}")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.current_plan = json.load(f)
            show_success(f"Plan loaded from: {filepath}")
            show_plan_summary(self.current_plan)
        except Exception as e:
            show_error(f"Failed to load plan: {str(e)}")

    def _exit(self):
        """Exit the application."""
        console.print("\n[bold cyan]🎬 DELTON AI signing off.[/bold cyan]")
        console.print("[dim]   Thank you for creating with us. See you next time![/dim]\n")
        self.running = False


# ═══════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════

def main():
    """Main entry point."""
    app = DeltonApp()
    app.start()


if __name__ == "__main__":
    main()