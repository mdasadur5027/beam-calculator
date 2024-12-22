import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from src.calculations.reactionsCalc import calculate_reactions
from src.calculations.shearForceCalc import shear_force
from src.calculations.bendingMomentCalc import bending_moment
from src.ui.inputs import input_beam_length, input_supports, input_loads, input_moments
from src.diagrams.beam_figure import draw_beam
from src.diagrams.sfd_bmd import plot_sfd_bmd


st.set_page_config(layout="wide")  #Set layout to wide for side-by-side display
st.title("Beam SFD and BMD Calculator")

#  Container for input on the left side and output on the right side
col1, col2 = st.columns([2, 3.6])

with col1:
    # Initialize session state variables
    if "beam_length" not in st.session_state:
        st.session_state.beam_length = 10.0
    if "supports" not in st.session_state:
        st.session_state.supports = []
    if "point_loads" not in st.session_state:
        st.session_state.point_loads = []
    if "distributed_loads" not in st.session_state:
        st.session_state.distributed_loads = []
    if "moments" not in st.session_state:
        st.session_state.moments = []

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Length"
    if "last_active_tab" not in st.session_state:
        st.session_state.last_active_tab = "Length"

    # Define a function to switch tabs
    def set_active_tab(tab_name):
        st.session_state.last_active_tab = st.session_state.active_tab
        st.session_state.active_tab = tab_name

    
    # Display tab buttons
    # Display tab buttons with equal width
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;  /* Make buttons take full width of their container */
        }
        .stColumn {
            width: 25%; /* Ensure the columns take equal width */
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1_h1, col1_h2, col1_h3, col1_h4 = st.columns(4)

    with col1_h1:
        st.button("Length", on_click=set_active_tab, args=("Length",))
    with col1_h2:
        if st.button("Supports"):
            set_active_tab("Support")

    with col1_h3:
        if st.button("Loads"):
            set_active_tab("Load")

    with col1_h4:
        if st.button("Moments"):
            set_active_tab("Moment")

    # Track changes only if the active tab has changed
    if st.session_state.active_tab != st.session_state.last_active_tab:
        if st.session_state.last_active_tab == "Length":
            st.session_state.beam_length = st.session_state.get("temp_beam_length", st.session_state.beam_length)
        elif st.session_state.last_active_tab == "Support":
            st.session_state.supports = st.session_state.get("temp_supports", st.session_state.supports)
        elif st.session_state.last_active_tab == "Load":
            st.session_state.point_loads = st.session_state.get("temp_point_loads", st.session_state.point_loads)
            st.session_state.distributed_loads = st.session_state.get("temp_distributed_loads", st.session_state.distributed_loads)
        elif st.session_state.last_active_tab == "Moment":
            st.session_state.moments = st.session_state.get("temp_moments", st.session_state.moments)

    

    # Render tab-specific inputs
    if st.session_state.active_tab == "Length":
        st.session_state.temp_beam_length = input_beam_length(
            default_value=st.session_state.beam_length
        )
    elif st.session_state.active_tab == "Support":
        st.session_state.temp_supports = input_supports(
            beam_length=st.session_state.beam_length,
            saved_supports=st.session_state.supports
        )
    elif st.session_state.active_tab == "Load":
        st.session_state.temp_point_loads, st.session_state.temp_distributed_loads = input_loads(
            beam_length=st.session_state.beam_length,
            saved_point_loads=st.session_state.point_loads,
            saved_distributed_loads = st.session_state.distributed_loads
        )


    elif st.session_state.active_tab == "Moment":
        st.session_state.temp_moments = input_moments(
            beam_length=st.session_state.beam_length,
            saved_moments=st.session_state.moments
        )
    st.divider()
    # st.write(st.session_state)

    # Display Inputs
    if st.button("Calculate", on_click=set_active_tab, args=("calculate",)):
        set_active_tab("Calculate")
        # st.write("Performing calculations based on the input data...")

            
    st.write("#### Input Summary")
    if st.session_state.beam_length:
        st.write(f"**Beam Length**: {st.session_state.beam_length} m")
    
    if st.session_state.supports:
        st.write("**Supports**:")
        for support in st.session_state.supports:
            st.write(f"- {support[0]} support at {support[1]} m")
    
    if st.session_state.point_loads:
        st.write("**Point Loads**:")
        for load in st.session_state.point_loads:
            direction = "Upward" if load[1] > 0 else "Downward"
            st.write(f"- Load at {load[0]} m with magnitude {abs(load[1])} kN ({direction})")
    
    if st.session_state.distributed_loads:
        st.write("**Distributed Loads**:")
        for dist_load in st.session_state.distributed_loads:
            st.write(f"- From {dist_load[0]} m to {dist_load[1]} m with magnitudes {dist_load[2]} kN/m to {dist_load[3]} kN/m")

    if st.session_state.moments:
        st.write("**Moments**:")
        for moment in st.session_state.moments:
            st.write(f"- Moment at {moment[0]} m with magnitude {moment[1]} kNm")


with col2:
    col2a, col2b = st.columns(2)
    with col2a:
        # Calculate reactions
        reactions = calculate_reactions(st.session_state.supports, st.session_state.point_loads, st.session_state.distributed_loads, st.session_state.moments, st.session_state.beam_length)
    with col2b:
        resolution = st.number_input("Resolution (higher = more precision)", min_value=10, max_value=1000, value=100, step=10)
        
    num_supports = len(st.session_state.supports)
    # st.write(num_supports)
    if num_supports == 1:
        support_reactions = [reactions[0]]
        support_moments = [reactions[1]]
    else:
        support_reactions = reactions
        support_moments = []
    # st.write(reaction_supports)

    st.divider()

    # Draw Beam
    positions = draw_beam(st.session_state.beam_length, st.session_state.supports, st.session_state.point_loads, st.session_state.distributed_loads, st.session_state.moments)

    # SF
    x_coords, shear = shear_force(support_reactions, st.session_state.point_loads, st.session_state.distributed_loads, st.session_state.beam_length, resolution)
    # BM
    x_coords, bending_moment = bending_moment(st.session_state.supports, support_reactions, support_moments, st.session_state.point_loads, st.session_state.distributed_loads, st.session_state.moments, st.session_state.beam_length, resolution)
    # SFD & BMD
    plot_sfd_bmd(x_coords, shear, bending_moment, positions)