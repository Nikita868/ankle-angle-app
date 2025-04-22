import math
import random
import streamlit as st
import matplotlib.pyplot as plt

# Function to generate standard random walking-related coordinates
def generate_coordinates():
    LEX = round(random.uniform(0.1, 0.2), 3)
    LEY = round(random.uniform(0.43, 0.46), 3)
    LMX = round(random.uniform(0.0, 0.1), 3)
    LMY = round(random.uniform(0.2, 0.3), 3)
    CX = round(random.uniform(-0.15, -0.05), 3)
    CY = round(random.uniform(0.18, 0.26), 3)
    MTX = round(random.uniform(0.0, 0.05), 3)
    MTY = round(random.uniform(0.0, 0.01), 3)
    return LEX, LEY, LMX, LMY, CX, CY, MTX, MTY

# Function to generate dorsiflexed condition (positive ankle angle)
def generate_dorsiflexed_coordinates(LEX, LEY, LMX, LMY):
    CX = round(random.uniform(-0.15, -0.05), 3)
    CY = round(LMY - 0.05, 3)  # about 5 cm lower than Lateral Malleolus
    MTX = round(CX + random.uniform(0.14, 0.17), 3)  # Toes forward
    MTY = round(CY + random.uniform(0.02, 0.04), 3)  # Toes slightly higher than heel
    return CX, CY, MTX, MTY

# Function to calculate absolute angles with quadrant corrections
def calculate_absolute_angle(proximal_x, proximal_y, distal_x, distal_y):
    delta_x = proximal_x - distal_x
    delta_y = proximal_y - distal_y
    angle_rad = math.atan2(delta_y, delta_x)
    angle_deg = math.degrees(angle_rad)

    # Apply quadrant correction
    if delta_x > 0 and delta_y >= 0:  # Quadrant 1
        pass
    elif delta_x < 0 and delta_y > 0:  # Quadrant 2 
        angle_deg += 0
    elif delta_x < 0 and delta_y < 0:  # Quadrant 3
        angle_deg += 180
    elif delta_x > 0 and delta_y < 0:  # Quadrant 4
        angle_deg += 360

    return round(angle_deg, 1)

# Initialize session state
if 'LEX' not in st.session_state:
    st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY, st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY = generate_coordinates()
    st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
    st.session_state.foot_angle = calculate_absolute_angle(st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY)
    st.session_state.ankle_angle = round(st.session_state.foot_angle - st.session_state.leg_angle - 90, 1)
    st.session_state.show_how = False

st.title("Leg Angle, Foot Angle, and Ankle Relative Angle Practice App")

# Problem Statement
st.subheader("Problem Statement")
st.markdown("""
The data below are (x,y) position coordinates of a person's lower leg and foot during walking.
Use the data to estimate:
- Absolute angle of the leg segment
- Absolute angle of the foot segment
- Relative ankle angle

Report all answers in degrees to one decimal place.
""")

# Display Coordinates
st.subheader("Provided Coordinates")
st.table({
    "Anatomical Location": ["Lateral Epicondyle", "Lateral Malleolus", "Calcaneus", "5th MTP (toes)"],
    "X Position (m)": [st.session_state.LEX, st.session_state.LMX, st.session_state.CX, st.session_state.MTX],
    "Y Position (m)": [st.session_state.LEY, st.session_state.LMY, st.session_state.CY, st.session_state.MTY]
})

# Student input
student_leg_angle = st.number_input("Your estimated absolute leg angle (degrees):", step=0.1, key='leg')
student_foot_angle = st.number_input("Your estimated absolute foot angle (degrees):", step=0.1, key='foot')
student_ankle_angle = st.number_input("Your estimated relative ankle angle (degrees):", step=0.1, key='ankle')

# Buttons
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("Check Leg Angle"):
        if abs(student_leg_angle - st.session_state.leg_angle) <= 0.1:
            st.success(f"✅ Correct! The absolute leg angle is {st.session_state.leg_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute leg angle is {st.session_state.leg_angle:.1f}°.")

with col2:
    if st.button("Check Foot Angle"):
        if abs(student_foot_angle - st.session_state.foot_angle) <= 0.1:
            st.success(f"✅ Correct! The absolute foot angle is {st.session_state.foot_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct absolute foot angle is {st.session_state.foot_angle:.1f}°.")

with col3:
    if st.button("Check Ankle Angle"):
        if abs(student_ankle_angle - st.session_state.ankle_angle) <= 0.1:
            st.success(f"✅ Correct! The relative ankle angle is {st.session_state.ankle_angle:.1f}°.")
        else:
            st.error(f"❌ Incorrect. The correct relative ankle angle is {st.session_state.ankle_angle:.1f}°.")

with col4:
    if st.button("Show How to Calculate"):
        st.session_state.show_how = True

with col5:
    if st.button("🔄 Try Another Problem"):
        st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY, st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY = generate_coordinates()
        st.session_state.leg_angle = calculate_absolute_angle(st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
        st.session_state.foot_angle = calculate_absolute_angle(st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY)
        st.session_state.ankle_angle = round(st.session_state.foot_angle - st.session_state.leg_angle - 90, 1)
        st.session_state.show_how = False
        st.rerun()

with col6:
    if st.button("🔄 Try When Ankle is Dorsiflexed"):
        # Keep leg the same but modify foot for dorsiflexed condition
        st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY = generate_dorsiflexed_coordinates(
            st.session_state.LEX, st.session_state.LEY, st.session_state.LMX, st.session_state.LMY)
        st.session_state.foot_angle = calculate_absolute_angle(st.session_state.CX, st.session_state.CY, st.session_state.MTX, st.session_state.MTY)
        st.session_state.ankle_angle = round(st.session_state.foot_angle - st.session_state.leg_angle - 90, 1)
        st.session_state.show_how = False
        st.rerun()

# Explanation and Plot
if st.session_state.show_how:
    st.subheader("📚 How to Calculate:")

    st.markdown("**Absolute Leg Angle:**")
    st.latex(r"\Delta x = LEX - LMX")
    st.latex(r"\Delta y = LEY - LMY")
    st.latex(r"\text{Leg Angle} = \text{atan2}(\Delta y, \Delta x)")
    st.markdown("Apply quadrant correction rules as before.")

    st.markdown("**Absolute Foot Angle:**")
    st.latex(r"\Delta x = CX - MTX")
    st.latex(r"\Delta y = CY - MTY")
    st.latex(r"\text{Foot Angle} = \text{atan2}(\Delta y, \Delta x)")
    st.markdown("Apply same quadrant correction rules.")

    st.markdown("**Relative Ankle Angle:**")
    st.latex(r"\text{Ankle Angle} = \text{Foot Angle} - \text{Leg Angle} - 90")

    st.subheader("📈 Segment Plot")
    fig, ax = plt.subplots(figsize=(1, 4))  # 4:1 aspect ratio
    ax.plot([st.session_state.LEX, st.session_state.LMX], [st.session_state.LEY, st.session_state.LMY], 'bo-', label='Leg (LEX → LMX)')
    ax.plot([st.session_state.CX, st.session_state.MTX], [st.session_state.CY, st.session_state.MTY], 'go-', label='Foot (CX → MTX)')
    ax.text(st.session_state.LEX, st.session_state.LEY, 'LEX', fontsize=9, ha='right')
    ax.text(st.session_state.LMX, st.session_state.LMY, 'LMX', fontsize=9, ha='left')
    ax.text(st.session_state.CX, st.session_state.CY, 'CX', fontsize=9, ha='right')
    ax.text(st.session_state.MTX, st.session_state.MTY, 'MTX', fontsize=9, ha='left')
    ax.set_xlabel('X Position (m)')
    ax.set_ylabel('Y Position (m)')
    ax.set_title('Leg and Foot Segments')
    ax.set_aspect(4)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
