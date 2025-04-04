import asyncio
from vpython import sphere, vector, rate, mag, norm, cross, color, box, label, scene
import random

# Enlarge the canvas
scene.width = 1800  # Set the width of the canvas (default is 1800)
scene.height = 900  # Set the height of the canvas (default is 900)
scene.range = 4  # Increase the visible range of the 3D scene

def rainbow_color(normalized_value):
    """Map a normalized value (0 to 1) to a rainbow color."""
    if normalized_value < 0.25:
        return vector(0, 4 * normalized_value, 1)  # Blue to Cyan
    elif normalized_value < 0.5:
        return vector(0, 1, 1 - 4 * (normalized_value - 0.25))  # Cyan to Green
    elif normalized_value < 0.75:
        return vector(4 * (normalized_value - 0.5), 1, 0)  # Green to Yellow
    else:
        return vector(1, 1 - 4 * (normalized_value - 0.75), 0)  # Yellow to Red

def create_legend():
    """Create a legend for the rainbow color scale."""
    legend_width = 0.1
    legend_height = 1
    legend_pos = vector(-2, 2, 0)  # Position of the legend
    num_segments = 21  # Number of segments in the legend

    for i in range(num_segments):
        normalized_value = i / (num_segments - 1)
        segment_color = rainbow_color(normalized_value)
        box(pos=legend_pos + vector(0, -i * (legend_height / num_segments), 0),
            size=vector(legend_width, legend_height / num_segments, 0.01),
            color=segment_color)

    # Add labels for the legend
    label(pos=legend_pos + vector(-0.2, 0, 0), text="Low Force", height=10, box=False, color=color.white)
    label(pos=legend_pos + vector(-0.2, -legend_height, 0), text="High Force", height=10, box=False, color=color.white)

async def main():
    ###### Define Parameters #####
    G = 1
    M = 1
    R = 1
    rsoft = 0.03
    w = vector(0, 0.05, 0)
    n = 0
    N = 30
    stars = []
    
    create_legend()

    # Create the legend
    create_legend()

    # Create a progress bar
    progress_bar_bg = box(pos=vector(0, -2.5, 0), size=vector(4, 0.1, 0.01), color=color.gray(0.5))
    progress_bar = box(pos=vector(-2, -2.5, 0), size=vector(0.01, 0.1, 0.01), color=color.green)

    # Create a label for the progress percentage
    progress_label = label(pos=vector(0, -2.3, 0), text="0%", height=15, box=False, color=color.white)

    '''Generate a random distribution of stars in a sphere'''
    while n < N:
        rt = R * vector(2 * random.random() - 1, 2 * random.random() - 1, 2 * random.random() - 1)
        stars.append(sphere(pos=rt, radius=R / 30, make_trail=True, retain=100, color=color.white))
        n += 1

    for star in stars:
        star.m = M / N
        star.p = star.m * cross(w, vector(star.pos.x, 0, star.pos.z))
        star.F = vector(0, 0, 0)

    t = 0
    dt = 0.01
    total_time = 100  # Total simulation time

    while t < total_time:
        rate(100)
        max_force = 0  # Track the maximum force for normalization
        for star in stars:
            star.F = vector(0, 0, 0)
        for i in range(len(stars)):
            for j in range(len(stars)):
                if i != j:
                    rji = stars[i].pos - stars[j].pos
                    stars[i].F -= G * stars[i].m * stars[j].m * norm(rji) / (mag(rji)**2 + rsoft**2)
            max_force = max(max_force, mag(stars[i].F))  # Update max force

        for star in stars:
            star.p += star.F * dt
            star.pos += star.p * dt / star.m

            # Normalize the force magnitude to a range [0, 1] for color mapping
            normalized_force = mag(star.F) / max_force if max_force > 0 else 0
            star.color = rainbow_color(normalized_force)  # Apply rainbow color gradient

        # Update the progress bar
        progress_fraction = t / total_time
        progress_bar.size.x = 4 * progress_fraction  # Scale the progress bar width
        progress_bar.pos.x = -2 + 2 * progress_fraction  # Adjust the position of the progress bar

        # Update the progress percentage label
        progress_label.text = f"{int(progress_fraction * 100)}%"  # Update the percentage text

        t += dt

# Run the main function using asyncio
asyncio.run(main())




