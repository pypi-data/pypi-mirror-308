import random
import time
import sys
import pyfiglet

def glow_text(text: str, colors: list, pulse_intensity: int) -> str:
    """Apply a dynamic glowing effect with pulsing intensity to text."""
    glowing_text = ""
    intensity_colors = colors[:pulse_intensity]  # Limit colors to simulate fading effect
    for char in text:
        if char.strip():  # Only apply color to non-space characters
            glowing_text += random.choice(intensity_colors) + char
        else:
            glowing_text += char  # Preserve spaces
    glowing_text += "\033[0m"  # Reset color at the end
    return glowing_text

def anaiza_text_effect(text: str, delay: float = 0.1, iterations: int = 20):
    """Print text with a smooth animated glow effect using ASCII art."""
    base_colors = [
        "\033[38;5;46m",  # Neon Green
        "\033[38;5;51m",  # Neon Cyan
        "\033[38;5;226m", # Neon Yellow
        "\033[38;5;201m", # Neon Pink
        "\033[38;5;208m"  # Neon Orange
    ]
    
    # Generate large ASCII text
    ascii_art = pyfiglet.figlet_format(text)

    pulse = [1, 2, 3, 4, 5, 4, 3, 2]  # Simulates pulsing brightness

    for i in range(iterations):
        # Modulate the colors to simulate pulsing brightness
        animated_text = glow_text(ascii_art, base_colors, pulse[i % len(pulse)])
        
        # Print in-place with no abrupt clearing
        sys.stdout.write("\033[H\033[J")  # Clear the terminal (smooth)
        sys.stdout.write(animated_text)
        sys.stdout.flush()
        time.sleep(delay)

    print("\033[0m")  # Reset color to default
