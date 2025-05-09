import streamlit as st
import matplotlib.pyplot as plt

def plot_sfd_bmd(x_coords, shear, bending_moment, positions):
    # Use a valid Matplotlib style
    plt.style.use("ggplot")

    # Create the figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={"height_ratios": [1, 1]})

    # Plot the Shear Force Diagram (SFD)
    ax1.plot(x_coords, shear, color="blue", linewidth=2)
    ax1.fill_between(x_coords, shear, 0, color="blue", alpha=0.2)
    ax1.axhline(0, color="black", linewidth=1, linestyle="--")
    ax1.set_ylabel("Shear Force (kN)", fontsize=12)
    ax1.tick_params(axis="both", which="major", labelsize=10)
    
    # Set the x-axis limits based on the beam length
    ax1.set_xlim([min(x_coords), max(x_coords)])

    # Annotate the zero shear position (same as max bending moment position)
    max_bending_idx = bending_moment.index(max(bending_moment, key=abs))
    max_bending_x = x_coords[max_bending_idx]

    # Annotate zero shear at max bending moment position
    ax1.annotate(
        f"x={max_bending_x:.2f}",  # Annotating the x value
        (max_bending_x, 0),  # Zero shear position
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=12,
        arrowprops=dict(facecolor="blue", arrowstyle="->", lw=0.5)
    )

    # Plot the Bending Moment Diagram (BMD)
    ax2.plot(x_coords, bending_moment, color="green", linewidth=2)
    ax2.fill_between(x_coords, bending_moment, 0, color="green", alpha=0.2)
    ax2.axhline(0, color="black", linewidth=1, linestyle="--")
    ax2.set_xlabel("Beam Length (m)", fontsize=12)
    ax2.set_ylabel("Bending Moment (kNm)", fontsize=12)
    ax2.tick_params(axis="both", which="major", labelsize=10)

    # Set the x-axis limits based on the beam length
    ax2.set_xlim([min(x_coords), max(x_coords)])

    # Annotate maximum and minimum bending moments
    min_bending_idx = bending_moment.index(min(bending_moment, key=abs))

    ax2.annotate(
        f"Max M\nx={x_coords[max_bending_idx]:.2f}\nM={bending_moment[max_bending_idx]:.2f}",
        (x_coords[max_bending_idx], bending_moment[max_bending_idx]),
        textcoords="offset points",
        xytext=(10, -20),
        ha="center",
        fontsize=12,
        arrowprops=dict(facecolor="green", arrowstyle="->", lw=0.5)
    )

    # ax2.annotate(
    #     f"Min M\nx={x_coords[min_bending_idx]:.2f}\nM={bending_moment[min_bending_idx]:.2f}",
    #     (x_coords[min_bending_idx], bending_moment[min_bending_idx]),
    #     textcoords="offset points",
    #     xytext=(10, 20),
    #     ha="center",
    #     fontsize=10,
    #     arrowprops=dict(facecolor="green", arrowstyle="->", lw=0.5)
    # )

    # Annotate SF and BM at specified positions and draw vertical lines
    for pos in positions:
        # Find the closest index for the given position in x_coords
        closest_idx = min(range(len(x_coords)), key=lambda i: abs(x_coords[i] - pos))
        
        # Annotate Shear Force at the given position
        ax1.annotate(
            f"{shear[closest_idx]:.2f}",  # SF value
            (x_coords[closest_idx], shear[closest_idx]),  # Position on the graph
            textcoords="offset points",
            xytext=(10, 5),
            ha="center",
            fontsize=12,
            color="brown"
        )

        # Annotate Bending Moment at the given position
        ax2.annotate(
            f"{bending_moment[closest_idx]:.2f}",  # BM value
            (x_coords[closest_idx], bending_moment[closest_idx]),  # Position on the graph
            textcoords="offset points",
            xytext=(10, 5),
            ha="center",
            fontsize=12,
            color="brown"
        )

        # Draw light vertical lines at the specified positions
        ax1.axvline(x=x_coords[closest_idx], color="blue", linestyle="--", linewidth=0.5)
        ax2.axvline(x=x_coords[closest_idx], color="green", linestyle="--", linewidth=0.5)
        # Draw at max bm and zero sf
        ax1.axvline(x=x_coords[max_bending_idx], color="blue", linestyle="--", linewidth=0.5)
        ax2.axvline(x=x_coords[max_bending_idx], color="green", linestyle="--", linewidth=0.5)

        # Add "Generated by Torch Tech" at the bottom right corner
        fig.text(0.95, 0.0, 'Generated by Md. Asadur Rahman', ha='center', va='center', fontsize=10, color='black', alpha=0.6)

    # Adjust layout
    plt.tight_layout()

    # Display the diagram in Streamlit
    st.pyplot(fig)

    # Avoid overlapping plots in the Streamlit app
    plt.close(fig)

    
