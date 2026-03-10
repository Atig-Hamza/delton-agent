"""
╔══════════════════════════════════════════════════╗
║              D E L T O N   A I                   ║
║         Rich Terminal User Interface             ║
╚══════════════════════════════════════════════════╝
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.layout import Layout
from rich.markdown import Markdown
from rich import box
import time


console = Console()


def show_banner():
    """Display the DELTON AI startup banner."""
    banner = """
[bold cyan]
    ██████╗ ███████╗██╗  ████████╗ ██████╗ ███╗   ██╗     █████╗ ██╗
    ██╔══██╗██╔════╝██║  ╚══██╔══╝██╔═══██╗████╗  ██║    ██╔══██╗██║
    ██║  ██║█████╗  ██║     ██║   ██║   ██║██╔██╗ ██║    ███████║██║
    ██║  ██║██╔══╝  ██║     ██║   ██║   ██║██║╚██╗██║    ██╔══██║██║
    ██████╔╝███████╗███████╗██║   ╚██████╔╝██║ ╚████║    ██║  ██║██║
    ╚═════╝ ╚══════╝╚══════╝╚═╝    ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝
[/bold cyan]
[dim]    Powered by Kimi K2.5 | NVIDIA API Endpoint[/dim]
[bold white]    "From Vision to Video — AI That Thinks Like a Filmmaker"[/bold white]
    """
    console.print(banner)


def show_welcome():
    """Display welcome message."""
    welcome = Panel(
        """[bold white]🎬 DELTON AI is online and ready.[/bold white]

[cyan]I'm your AI montage director. Tell me your vision,
and I'll craft it into a cinematic masterpiece.[/cyan]

[bold yellow]💡 Quick Commands:[/bold yellow]
  [green]• Describe your video idea in detail[/green]
  [green]• Type 'PREMIUM AD MODE' for advertisement creation[/green]
  [green]• Type 'refine' to modify the last plan[/green]
  [green]• Type 'render' to generate the video[/green]
  [green]• Type 'preview' to see the plan summary[/green]
  [green]• Type 'reset' to start fresh[/green]
  [green]• Type 'help' for all commands[/green]
  [green]• Type 'exit' to quit[/green]

[bold yellow]📐 Format Options:[/bold yellow]
  [dim]landscape (16:9) | portrait (9:16) | square (1:1) | ultrawide (21:9)[/dim]

[bold yellow]🎨 Style Options:[/bold yellow]
  [dim]cinematic | luxury | tech | viral | minimal | dramatic[/dim]""",
        title="[bold cyan]Welcome to DELTON AI[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE_EDGE,
        padding=(1, 2)
    )
    console.print(welcome)


def show_help():
    """Display help information."""
    table = Table(
        title="DELTON AI — Commands",
        box=box.ROUNDED,
        border_style="cyan"
    )
    table.add_column("Command", style="bold green", width=20)
    table.add_column("Description", style="white")

    commands = [
        ("Any text", "Describe your video — AI will create a montage plan"),
        ("PREMIUM AD MODE", "Activate premium advertisement creation mode"),
        ("render", "Render the current montage plan to video"),
        ("preview", "Show summary of current montage plan"),
        ("refine + text", "Modify the current plan (e.g., 'refine make it faster')"),
        ("reset", "Clear current project and start fresh"),
        ("formats", "Show available video formats"),
        ("styles", "Show available color grades and ad styles"),
        ("transitions", "Show available transitions"),
        ("effects", "Show available visual effects"),
        ("icons", "Show available icons"),
        ("help", "Show this help screen"),
        ("exit / quit", "Exit DELTON AI"),
    ]

    for cmd, desc in commands:
        table.add_row(cmd, desc)

    console.print(table)


def show_formats():
    """Display available formats."""
    table = Table(title="Available Formats", box=box.ROUNDED, border_style="cyan")
    table.add_column("Format", style="bold green")
    table.add_column("Resolution", style="white")
    table.add_column("Use Case", style="dim")

    formats = [
        ("landscape", "1920×1080", "YouTube, Website, TV"),
        ("portrait", "1080×1920", "TikTok, Reels, Shorts"),
        ("square", "1080×1080", "Instagram Feed"),
        ("ultrawide", "2560×1080", "Cinematic"),
        ("4k_landscape", "3840×2160", "4K YouTube, Cinema"),
        ("4k_portrait", "2160×3840", "4K Vertical"),
    ]

    for fmt, res, use in formats:
        table.add_row(fmt, res, use)

    console.print(table)


def show_styles():
    """Display available styles."""
    table = Table(title="Color Grades & Ad Styles", box=box.ROUNDED, border_style="cyan")
    table.add_column("Style", style="bold green")
    table.add_column("Type", style="yellow")
    table.add_column("Mood", style="dim")

    styles = [
        ("cinematic_teal_orange", "Color Grade", "Blockbuster cinematic"),
        ("warm_golden", "Color Grade", "Sunset, nostalgic"),
        ("cool_blue", "Color Grade", "Corporate, tech"),
        ("dark_moody", "Color Grade", "Thriller, luxury"),
        ("vintage_film", "Color Grade", "Retro, film"),
        ("neon_cyberpunk", "Color Grade", "Futuristic, vibrant"),
        ("clean_bright", "Color Grade", "Commercial, product"),
        ("bw_dramatic", "Color Grade", "Dramatic B&W"),
        ("pastel_soft", "Color Grade", "Lifestyle, fashion"),
        ("luxury_dark_gold", "Color Grade", "Luxury brand"),
        ("apple_clean", "Ad Style", "Clean, minimal, white"),
        ("nike_bold", "Ad Style", "Dark, bold, energetic"),
        ("luxury_elegance", "Ad Style", "Black & gold, premium"),
        ("tech_modern", "Ad Style", "Dark blue, futuristic"),
        ("social_viral", "Ad Style", "Bright, catchy, trending"),
        ("cinematic_story", "Ad Style", "Widescreen, dramatic"),
    ]

    for style, stype, mood in styles:
        table.add_row(style, stype, mood)

    console.print(table)


def show_transitions():
    """Display available transitions."""
    from config import TRANSITIONS
    table = Table(title="Available Transitions", box=box.ROUNDED, border_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Transition", style="bold green")

    for i, trans in enumerate(TRANSITIONS, 1):
        table.add_row(str(i), trans)

    console.print(table)


def show_effects():
    """Display available VFX."""
    effects = [
        ("particles_dust", "Floating dust particles"),
        ("particles_sparks", "Spark/fire particles"),
        ("particles_bokeh", "Bokeh light circles"),
        ("particles_snow", "Snow falling"),
        ("particles_rain", "Rain drops"),
        ("vignette", "Dark edges, focus center"),
        ("film_grain", "Vintage film texture"),
        ("glow", "Bloom/glow on bright areas"),
        ("chromatic_aberration", "RGB color split"),
        ("lens_flare", "Anamorphic lens flare"),
        ("screen_shake", "Camera shake effect"),
        ("light_rays", "Volumetric light rays"),
    ]

    table = Table(title="Available Visual Effects", box=box.ROUNDED, border_style="cyan")
    table.add_column("Effect", style="bold green")
    table.add_column("Description", style="white")

    for eff, desc in effects:
        table.add_row(eff, desc)

    console.print(table)


def show_icons():
    """Display available icons."""
    from config import ICON_LIBRARIES
    icons = ICON_LIBRARIES.get("lucide", {}).get("icons", {})

    table = Table(title="Available Icons (Lucide)", box=box.ROUNDED, border_style="cyan")
    table.add_column("Icon Name", style="bold green", width=20)
    table.add_column("Icon Name", style="bold green", width=20)
    table.add_column("Icon Name", style="bold green", width=20)

    icon_list = list(icons.keys())
    for i in range(0, len(icon_list), 3):
        row = [icon_list[i] if i < len(icon_list) else ""]
        row.append(icon_list[i+1] if i+1 < len(icon_list) else "")
        row.append(icon_list[i+2] if i+2 < len(icon_list) else "")
        table.add_row(*row)

    console.print(table)


def show_plan_summary(plan: dict):
    """Display a montage plan summary."""
    if not plan:
        console.print("[yellow]No plan loaded.[/yellow]")
        return

    # Header
    console.print(Panel(
        f"""[bold white]Project:[/bold white] {plan.get('project_name', 'Untitled')}
[bold white]Description:[/bold white] {plan.get('description', 'N/A')}
[bold white]Format:[/bold white] {plan.get('format', 'landscape')} | [bold white]Resolution:[/bold white] {plan.get('resolution', [1920,1080])}
[bold white]Duration:[/bold white] {plan.get('total_duration', 0)}s | [bold white]FPS:[/bold white] {plan.get('fps', 30)}
[bold white]Color Grade:[/bold white] {plan.get('color_grade', 'none')}
[bold white]Ad Style:[/bold white] {plan.get('ad_style', 'none')}
[bold white]Music:[/bold white] {plan.get('music', {}).get('style', 'N/A')} @ {plan.get('music', {}).get('bpm', 'N/A')} BPM""",
        title="[bold cyan]📋 Montage Plan[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED
    ))

    # Scenes
    scenes = plan.get('scenes', [])
    table = Table(
        title=f"Scenes ({len(scenes)} total)",
        box=box.ROUNDED,
        border_style="green"
    )
    table.add_column("#", style="bold", width=3)
    table.add_column("Name", style="white", width=15)
    table.add_column("Time", style="cyan", width=12)
    table.add_column("Type", style="yellow", width=10)
    table.add_column("Elements", style="green", width=8)
    table.add_column("Transition", style="magenta", width=18)
    table.add_column("VFX", style="dim", width=25)

    for scene in scenes:
        table.add_row(
            str(scene.get('scene_id', '?')),
            scene.get('name', 'Scene'),
            f"{scene.get('start_time', 0):.1f}s-{scene.get('end_time', 0):.1f}s",
            scene.get('type', 'content'),
            str(len(scene.get('elements', []))),
            scene.get('transition_out', 'none'),
            ', '.join(scene.get('vfx', [])[:3])
        )

    console.print(table)

    # Elements detail
    for scene in scenes:
        elements = scene.get('elements', [])
        if elements:
            elem_table = Table(
                title=f"Scene {scene.get('scene_id', '?')}: {scene.get('name', '')} — Elements",
                box=box.SIMPLE,
                border_style="dim"
            )
            elem_table.add_column("Type", style="yellow", width=10)
            elem_table.add_column("Content", style="white", width=25)
            elem_table.add_column("Position", style="dim", width=12)
            elem_table.add_column("Animation", style="green", width=15)

            for elem in elements:
                content = elem.get('content', '') or elem.get('icon_name', '')
                pos = f"({elem.get('position', [50,50])[0]}, {elem.get('position', [50,50])[1]})"
                elem_table.add_row(
                    elem.get('type', '?'),
                    content[:25],
                    pos,
                    elem.get('animation_in', 'none')
                )

            console.print(elem_table)


def show_rendering_progress(total_scenes: int):
    """Show rendering progress bar."""
    return Progress(
        TextColumn("[bold cyan]🎬 Rendering"),
        BarColumn(bar_width=40, style="cyan", complete_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console
    )


def show_error(message: str):
    """Display an error message."""
    console.print(Panel(
        f"[bold red]❌ Error:[/bold red] {message}",
        border_style="red",
        box=box.ROUNDED
    ))


def show_success(message: str):
    """Display a success message."""
    console.print(Panel(
        f"[bold green]✅ {message}[/bold green]",
        border_style="green",
        box=box.ROUNDED
    ))


def show_info(message: str):
    """Display an info message."""
    console.print(f"[cyan]ℹ️  {message}[/cyan]")


def show_thinking():
    """Show thinking animation."""
    console.print("[bold cyan]🧠 DELTON AI is thinking...[/bold cyan]")


def get_input() -> str:
    """Get user input with styled prompt."""
    try:
        return console.input("\n[bold green]🎬 DELTON AI >[/bold green] ").strip()
    except (EOFError, KeyboardInterrupt):
        return "exit"