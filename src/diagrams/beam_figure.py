import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def draw_beam(beam_length, supports, point_loads, distributed_loads, moments):
    
    fig, ax = plt.subplots(figsize=(12, 4))
    # ax.plot([0, beam_length], [0,0], 'b-', lw=2)
    ax.plot([0, beam_length], [1,1], 'b-', lw=2)
    ax.plot([0, beam_length], [-1,-1], 'b-', lw=2)

    ax.set_xlim(-beam_length * 0.03, beam_length * 1.03)
    ax.set_ylim(-16, 12)
    ax.get_yaxis().set_visible(False) # Hide y-axis
    ax.get_xaxis().set_visible(False)
    ax.axis('off')

    ax.fill_between(
        [0, beam_length], 
        [1, 1], 
        [-1, -1], 
        color='blue', 
        alpha=0.7  # Adjust transparency for visual effect
    )

    # support
    # Load icons for each support type
    fixed_left_icon_path = 'src/icons/fixed_support_left.png'
    fixed_right_icon_path = 'src/icons/fixed_support_right.png'
    hinge_icon_path = 'src/icons/hinge_support.png'
    roller_icon_path = 'src/icons/roller_support.png'

    # Load the images using the correct path
    hinge_icon = mpimg.imread(hinge_icon_path)
    fixed_icon_left = mpimg.imread(fixed_left_icon_path)
    fixed_icon_right = mpimg.imread(fixed_right_icon_path)
    roller_icon = mpimg.imread(roller_icon_path)

    for support_type, position in supports:
        if support_type == "Fixed":
            # Use the fixed support icon
            if position == beam_length:
                imagebox = OffsetImage(fixed_icon_right, zoom=0.5)
            else:
                imagebox = OffsetImage(fixed_icon_left, zoom=0.5)
            ab = AnnotationBbox(imagebox, (position, 0), frameon=False)
            ax.add_artist(ab)
        elif support_type == "Hinge":
            # Use the hinge support icon
            imagebox = OffsetImage(hinge_icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (position, -1.8), frameon=False)
            ax.add_artist(ab)
        elif support_type == "Roller":
            # Use the roller support icon
            imagebox = OffsetImage(roller_icon, zoom=0.3)
            ab = AnnotationBbox(imagebox, (position, -1.8), frameon=False)
            ax.add_artist(ab)

    ##Point Load
    max_magnitude = max((abs(mag) for _, mag in point_loads), default=0) # Find the maximum magnitude
    # st.write(max_magnitude)
    # Loop through point loads to draw arrows with adjusted positions and directions
    for position, magnitude in point_loads:
        if max_magnitude == 0:
            continue
        # Calculate arrow length based on magnitude, scaled to fit within the y-limits
        direction = 1 if magnitude > 0 else (-1 if magnitude < 0 else 0)  # Downward if positive, upward if negative

        if direction == 0:
            continue

        # Determine the starting y-coordinate based on load direction and beam thickness
        start_y = -2.2 * direction if magnitude > 0 else -2.2 * direction

        # Draw the arrow with the adjusted y-coordinate and length based on the load's sign and magnitude
        ax.arrow(
            position,              # x-coordinate of arrow's starting point
            start_y,               # y-coordinate of arrow's starting point
            0,                     # No horizontal movement, vertical arrow
            direction * .01,  # Adjust length by direction and scaled magnitude
            head_width=0.2,        # Width of the arrow head
            head_length=1,       # Length of the arrow head
            fc='red',              # Fill color of arrow
            ec='red'               # Edge color of arrow
        )
        # Calculate the line length proportionally based on the max magnitude
        line_length = direction * max(0.3, (abs(magnitude) / max_magnitude) * 8)
        # st.write(line_length)

        # Draw the red line from the arrowhead
        ax.plot([position, position], [start_y, -line_length], 'r-', lw=1.5)
        
        point_loads_text = -line_length - 1 if magnitude > 0 else -line_length + 0.05
        ax.text(position, point_loads_text, f'{abs(magnitude)} kN', color='red', ha='center')

    ## Distributed Load
    max_dist_magnitude = max((abs(mag) for _, _, mag1, mag2 in distributed_loads for mag in [mag1, mag2]), default=0)
    # st.write(max_dist_magnitude)

    for start_pos, end_pos, start_mag, end_mag in distributed_loads:
        if max_dist_magnitude == 0:
            continue

        # Calculate directions based on magnitude signs
        start_direction = 1 if start_mag > 0 else (-1 if start_mag < 0 else 0)
        end_direction = 1 if end_mag > 0 else (-1 if end_mag < 0 else 0)

        # Determine starting y-coordinates
        start_y = -2.2 * start_direction if start_direction != 0 else 0
        end_y = -2.2 * end_direction if end_direction != 0 else 0

        # Calculate line lengths proportionally based on max magnitude
        start_line_length = start_direction * max(0.3, (abs(start_mag) / max_dist_magnitude) * 8) if start_direction != 0 else 0
        end_line_length = end_direction * max(0.3, (abs(end_mag) / max_dist_magnitude) * 8) if end_direction != 0 else 0

        # Draw arrows at the start and end positions if direction is non-zero
        if start_direction != 0:
            ax.arrow(
                start_pos,
                start_y,
                0,
                start_direction * 0.01,
                head_width=0.2,
                head_length=1,
                fc='green',
                ec='green'
            )
        if end_direction != 0:
            ax.arrow(
                end_pos,
                end_y,
                0,
                end_direction * 0.01,
                head_width=0.2,
                head_length=1,
                fc='green',
                ec='green'
            )

        # Draw the green lines from the arrowheads or connect the fill directly to y=0
        ax.plot([start_pos, start_pos], [start_y, -start_line_length], 'g-', lw=1.5)
        ax.plot([end_pos, end_pos], [end_y, -end_line_length], 'g-', lw=1.5)

        # Connect the ends of the arrows and fill the area between
        x_coords = [start_pos, start_pos, end_pos, end_pos]
        y_coords = [-start_line_length if start_direction != 0 else 0, -1 if start_direction >0 else 1, -1 if end_direction>0 else 1, -end_line_length if end_direction != 0 else 0]
        ax.fill(x_coords, y_coords, color='green', alpha=0.3)

        # Label distributed load magnitudes at the start and end positions if direction is non-zero
        if start_direction != 0:
            start_pos_text = -start_line_length - 1 if start_mag > 0 else -start_line_length + 0.03
            ax.text(
                start_pos,
                start_pos_text,
                f'{abs(start_mag)} kN/m',
                color='green',
                ha='center'
            )
        if end_direction != 0:
            end_pos_text = -end_line_length - 1 if end_mag > 0 else -end_line_length + 0.03
            ax.text(
                end_pos,
                end_pos_text,
                f'{abs(end_mag)} kN/m',
                color='green',
                ha='center'
            )

    ## Moment
    clockwise_moment_icon_path = 'src/icons/moment_clockwise.png'
    anticlockwise_moment_icon_path = 'src/icons/moment_anticlockwise.png'

    clockwise_moment_icon = mpimg.imread(clockwise_moment_icon_path)
    anticlockwise_moment_icon = mpimg.imread(anticlockwise_moment_icon_path)

    for moment_position, moment_magnitude in moments:
        if moment_magnitude > 0:
            imagebox = OffsetImage(clockwise_moment_icon, zoom=0.13)
            ab = AnnotationBbox(imagebox, (moment_position, 0.0), frameon=False)
            ax.add_artist(ab)

            ax.text(moment_position, 4, f'{abs(moment_magnitude)} kNm', color='black', ha='center')

        elif moment_magnitude < 0:
            imagebox = OffsetImage(anticlockwise_moment_icon, zoom=0.13)
            ab = AnnotationBbox(imagebox, (moment_position, 0), frameon=False)
            ax.add_artist(ab)

            ax.text(moment_position, 4, f'{abs(moment_magnitude)} kNm', color='black', ha='center')

    # Positions
    positions = []
    # Add positions from supports
    positions.extend([support[1] for support in supports])
    # Add positions from point loads
    positions.extend([load[0] for load in point_loads])
    # Add start and end positions from distributed loads
    positions.extend([dist_load[0] for dist_load in distributed_loads])  # Start positions
    positions.extend([dist_load[1] for dist_load in distributed_loads])  # End positions
    # Add positions from moments
    positions.extend([moment[0] for moment in moments])
    # Add 0.0 and beam_length
    positions.append(0.0)
    positions.append(beam_length)

    # Remove duplicates and sort
    positions = sorted(set(positions))
    # st.write(positions)

    # dimension
    ax.plot([0, beam_length], [-12, -12], '-k', lw=1)
    dim_text_pos = 0
    for i in range (len(positions)-1):
        ax.plot([positions[i], positions[i]], [-12.5, -10], '-k', lw=1)
        dim_text = positions[i+1] - positions[i]
        formatted_dim_text = f"{dim_text:.2f}".rstrip('0').rstrip('.')
        dim_text_pos = positions[i]
        dim_text_pos += dim_text/2
        ax.text(
            dim_text_pos, 
            -11.5,
            f'{formatted_dim_text} m',
            color='black',
            ha='center'
        )
    # end dim
    ax.plot([beam_length, beam_length], [-12.5, -10], '-k', lw=1)


    st.pyplot(fig)
    plt.show()

    return positions