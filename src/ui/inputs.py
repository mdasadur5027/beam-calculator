import streamlit as st

def input_beam_length(default_value):
    st.write("#### Beam Length Input")
    return st.number_input(
        'Enter the beam length (m):',
        min_value=1.0,
        value=default_value,
        step=1.0
    )


def input_supports(beam_length, saved_supports):
    st.write('#### Define Supports')
    support_types = ["Fixed", "Hinge", "Roller"]
    num_supports = st.number_input('Number of Supports', min_value=1, max_value=2, value=len(saved_supports) or 1)
    supports = []
    for i in range(int(num_supports)):
        col1, col2 = st.columns(2)
        with col1:
            support_type = st.selectbox(
                f"Support {i+1} type:",
                support_types,
                index=support_types.index(saved_supports[i][0]) if i < len(saved_supports) else 0,
                key=f"support_type_{i}"
            )
        with col2:
            position = st.number_input(
                f'Position of support {i+1} (m from left):',
                min_value=0.0,
                max_value=beam_length,
                value=saved_supports[i][1] if i < len(saved_supports) else 0.0,
                step=1.0,
                key=f"support_pos_{i}"
            )
        supports.append((support_type, position))
    return supports


def input_loads(beam_length, saved_point_loads, saved_distributed_loads):
    st.write("#### Define Point Loads")
    
    # Point Loads
    num_point_loads = st.number_input(
        'Number of Point Loads',
        min_value=0,
        max_value=15,
        value=len(saved_point_loads) or 0
    )
    point_loads = []
    for i in range(int(num_point_loads)):
        col1, col2, col3 = st.columns([3, 3, 1])
        with col1:
            position = st.number_input(
                f"Point Load {i+1} position (m from left):",
                min_value=0.0,
                max_value=beam_length,
                value=saved_point_loads[i][0] if i < len(saved_point_loads) else 0.0,
                step=1.0,
                key=f"point_load_pos_{i}"
            )
        with col2:
            magnitude = st.number_input(
                f"Point Load {i+1} magnitude (kN):",
                value=saved_point_loads[i][1] if i < len(saved_point_loads) else 0.0,
                step=0.5,
                key=f"point_load_mag_{i}"
            )
        # with col3:
        #     upward_arrow = st.button("⬆️", key=f"upward_arrow_{i}")
        #     downward_arrow = st.button("⬇️", key=f"downward_arrow_{i}")
        #     if upward_arrow:
        #         magnitude = abs(magnitude)
        #     elif downward_arrow:
        #         magnitude = -abs(magnitude)
        point_loads.append((position, magnitude))

    # Distributed Loads
    st.write("#### Define Distributed Loads")
    num_distributed_loads = st.number_input(
        "Number of Distributed Loads",
        min_value=0,
        max_value=3,
        value=len(saved_distributed_loads) or 0
    )
    distributed_loads = []
    for i in range(int(num_distributed_loads)):
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            start_pos = st.number_input(
                f"Distributed Load {i+1} starting position (m from left):",
                min_value=0.0,
                max_value=beam_length,
                value=saved_distributed_loads[i][0] if i < len(saved_distributed_loads) else 0.0,
                step=1.0,
                key=f"dist_load_start_{i}"
            )
            start_mag = st.number_input(
                f"Distributed Load {i+1} start magnitude (kN/m):",
                value=saved_distributed_loads[i][2] if i < len(saved_distributed_loads) else 0.0,
                step=0.5,
                key=f"dist_load_start_mag_{i}"
            )
        with col2:
            end_pos = st.number_input(
                f"Distributed Load {i+1} ending position (m from left):",
                min_value=0.0,
                max_value=beam_length,
                value=saved_distributed_loads[i][1] if i < len(saved_distributed_loads) else 0.0,
                step=1.0,
                key=f"dist_load_end_{i}"
            )
            end_mag = st.number_input(
                f"Distributed Load {i+1} end magnitude (kN/m):",
                value=saved_distributed_loads[i][3] if i < len(saved_distributed_loads) else start_mag,
                step=0.5,
                key=f"dist_load_end_mag_{i}"
            )
        distributed_loads.append((start_pos, end_pos, start_mag, end_mag))

    return point_loads, distributed_loads

def input_moments(beam_length, saved_moments):
    st.write("#### Define Moments")
    num_moments = st.number_input(
        "Number of Moments:", 
        min_value=0, 
        max_value=3, 
        value=len(saved_moments) or 0
    )
    moments = []
    for i in range(int(num_moments)):
        col1, col2 = st.columns(2)
        with col1:
            moment_position = st.number_input(
                f"Moment {i+1} position (m from left):", 
                min_value=0.0, 
                max_value=beam_length, 
                value=saved_moments[i][0] if i < len(saved_moments) else 0.0,
                step=1.0,
                key=f"moment_pos_{i}"
            )
        with col2:
            moment_magnitude = st.number_input(
                f"Moment {i+1} magnitude (kNm):", 
                value=saved_moments[i][1] if i < len(saved_moments) else 0.0,
                step=1.0,
                key=f"moment_mag_{i}"
            )
        moments.append((moment_position, moment_magnitude))
    return moments
