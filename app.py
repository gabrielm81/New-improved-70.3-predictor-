import streamlit as st


# Initialize a tab index in session state (default 0 = Swim)
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

# Initialize a tab index in session state (default 0 = Swim)
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0

st.set_page_config(
    page_title="Ironman 70.3 Performance Predictor",
    layout="centered"
)

st.title("🏊‍♂️🚴‍♂️🏃‍♂️ Ironman 70.3 Performance Predictor")

st.write(
    """
    I built this project as I just completed Andrew Ng’s Course on Machine Learning & thought that it would be cool to  combine coding with something I deeply care about:
    Ironman training.

    Answer a few questions to estimate your Ironman 70.3 finish time.
    """
)

# -------------------
# CREATE TABS FOR SWIM, BIKE, RUN
# -------------------
tab_labels = ["🏊 Swim", "🚴 Bike", "🏃 Run"]
tabs = st.tabs(tab_labels)

# -------------------
# SWIM TAB
# -------------------
with tabs[0]:
    if st.session_state.current_tab == 0:
        st.header("🏊 Swim Performance")

    laps = st.slider(
        "How many 25m laps can you swim without stopping?",
        min_value=10,
        max_value=100,
        value=40,
        step=1
    )

    lap_time_sec = st.number_input(
        "Average time per 25m lap (seconds)",
        min_value=10,
        max_value=120,
        value=33,
        step=1
    )

    wet_suit = st.checkbox("I am wearing a Wet suit (reduces time slightly)")

    base_total_sec = 76 * lap_time_sec
    endurance_multiplier = (76 / laps) ** 0.4
    adjusted_total_sec = base_total_sec * endurance_multiplier

    if wet_suit:
        adjusted_total_sec *= 0.95

    swim_minutes = int(adjusted_total_sec // 60)
    swim_seconds = int(adjusted_total_sec % 60)

    st.write(f"**Estimated Swim Split:** ⏱️ {swim_minutes} min {swim_seconds} sec")

    with st.expander("How this calculation works"):
        st.write("""
1. Base pace: average time per 25m lap × 4 = pace per 100m.
2. Endurance factor: how many laps you can swim without stopping compared to 76 laps (1900m).
   - Less than 76 laps → slightly slower total time.
   - More than 76 laps → slightly faster total time.
3. Wet Suit reduces total time by 5%.
""")


    # -------------------
    # PREDICTION INPUT (ONLY SWIM PAGE)
    # -------------------
    st.subheader("📊 Predict Your Total 70.3 Time")

    pred_hours = st.slider("Predicted Total Hours", 0, 10, 6)
    pred_minutes = st.slider("Predicted Minutes", 0, 59, 0)
    pred_seconds = st.slider("Predicted Seconds", 0, 59, 0)

    # Store user predicted total in minutes for later comparison
    user_predicted_total_min = pred_hours * 60 + pred_minutes + pred_seconds / 60

# -------------------
# BIKE TAB
# -------------------
with tabs[1]:
    if st.session_state.current_tab == 1:
        st.header("🚴 Bike Performance")

    ftp = st.slider(
        "What is your FTP (watts)?",
        min_value=150,
        max_value=450,
        value=250,
        step=5
    )
    st.write(f"Your FTP: **{ftp} watts**")

    weight = st.number_input(
        "Your bodyweight (kg)",
        min_value=40.0,
        max_value=120.0,
        value=75.0,
        step=0.5
    )

    wkg = ftp / weight
    st.write(f"**Power-to-weight:** {wkg:.2f} W/kg")

    st.subheader("⛰️ Bike Course Elevation")
    elevation_gain = st.slider(
        "Total bike elevation gain (meters)",
        min_value=0,
        max_value=3000,
        value=800,
        step=50
    )
    st.write(f"Elevation gain: **{elevation_gain} m**")

    st.subheader("🚲 Bike Setup")
    bike_type = st.radio(
        "Bike type",
        ["Road Bike", "Triathlon Bike"],
        horizontal=True
    )
    aero_position = st.checkbox(
        "I can maintain an aero position (TT bars / aero hoods)"
    )

    base_speed_kmh = 30 + (wkg - 3.0) * 4
    if bike_type == "Triathlon Bike":
        base_speed_kmh += 1.5
    if aero_position:
        base_speed_kmh += 1.0

    st.write(f"Estimated average bike speed: **{base_speed_kmh:.1f} km/h**")

    elevation_penalty_minutes = (elevation_gain / 1000) * 5
    bike_distance_km = 90
    bike_time_hours = bike_distance_km / base_speed_kmh
    bike_time_minutes = bike_time_hours * 60 + elevation_penalty_minutes
    bike_hours = int(bike_time_minutes // 60)
    bike_minutes = int(bike_time_minutes % 60)

    st.write(f"**Estimated Bike Split:** ⏱️ {bike_hours}h {bike_minutes}min")
    st.caption("Estimate assumes steady pacing, no major wind, and typical road conditions.")

    with st.expander("⚡ Advanced Rider Metrics (Optional)"):
        st.write("""
        If you know your heart rate for a long ride, enter it below.
        Assumes you ride at **170 HR** for the race and your **max HR > 196**.
        """)

        adv_hr = st.number_input("Average heart rate during long effort (bpm)", min_value=0, max_value=200, value=0, step=1, key="adv_hr")
        adv_hours = st.number_input("Duration of this effort (hours)", min_value=0.0, max_value=5.0, value=0.0, step=0.1, key="adv_hours")
        adv_watts = st.number_input("Average watts for this effort", min_value=0, max_value=1000, value=0, step=1, key="adv_watts")

        if adv_hr > 0 and adv_hours > 0:
            if adv_watts == 0:
                adv_watts = ftp * (adv_hr / 137)
            effective_watts = adv_watts * (170 / adv_hr)
            adv_wkg = effective_watts / weight
            adv_base_speed_kmh = 30 + (adv_wkg - 3.0) * 4
            if bike_type == "Triathlon Bike":
                adv_base_speed_kmh += 1.5
            if aero_position:
                adv_base_speed_kmh += 1.0
            adv_bike_time_hours = bike_distance_km / adv_base_speed_kmh
            adv_bike_time_minutes = adv_bike_time_hours * 60 + elevation_penalty_minutes
            adv_hours_final = int(adv_bike_time_minutes // 60)
            adv_minutes_final = int(adv_bike_time_minutes % 60)
            st.write(f"**Advanced Estimated Bike Split:** ⏱️ {adv_hours_final}h {adv_minutes_final}min")
            st.caption("Assumes race effort at 170 HR and max HR > 196, using your default bike setup and course.")

# -------------------
# RUN TAB
# -------------------
with tabs[2]:
    st.header("🏃 Run Performance")

    st.subheader("Run Inputs")

    five_k_time = st.number_input("Best 5k time (minutes, optional)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    five_k_effort = st.slider("Perceived effort for 5k (1-10)", min_value=1, max_value=10, value=5) if five_k_time > 0 else None

    ten_k_time = st.number_input("Best 10k time (minutes, optional)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)
    ten_k_effort = st.slider("Perceived effort for 10k (1-10)", min_value=1, max_value=10, value=5) if ten_k_time > 0 else None

    hm_time = st.number_input("Best Half Marathon time (minutes, optional)", min_value=0.0, max_value=500.0, value=0.0, step=0.1)
    hm_effort = st.slider("Perceived effort for HM (1-10)", min_value=1, max_value=10, value=5) if hm_time > 0 else None

    elevation_gain_run = st.number_input("Total elevation gain for run (meters)", min_value=0, max_value=1000, value=0, step=10)
    trail_run = st.checkbox("The run course is on trail (slightly slower)")
    carbon_shoes = st.checkbox("I am wearing carbon-plated shoes (slightly faster)")

    # --- Run pace calculation ---
    run_paces = []
    weights = []

    if five_k_time > 0:
        run_paces.append(five_k_time / 5.0)
        weights.append(5.0)
    if ten_k_time > 0:
        run_paces.append(ten_k_time / 10.0)
        weights.append(10.0)
    if hm_time > 0:
        run_paces.append(hm_time / 21.0975)
        weights.append(21.0975)

    if run_paces:
        base_run_pace = sum(p * w for p, w in zip(run_paces, weights)) / sum(weights)

        effort_values = list(filter(None, [five_k_effort, ten_k_effort, hm_effort]))
        avg_effort = sum(effort_values) / len(effort_values)

        effort_multiplier = 1 - ((9 - avg_effort) * 0.03)
        base_run_pace *= effort_multiplier

        if hm_time == 0:
            if ten_k_time > 0:
                extrapolation_multiplier = 1.05
            else:
                extrapolation_multiplier = 1.10
            base_run_pace *= extrapolation_multiplier

        fatigue_multiplier = 1.05
        base_run_pace *= fatigue_multiplier

        if carbon_shoes:
            base_run_pace *= 0.97

        base_run_pace *= (1 + 0.025 * (elevation_gain_run / 100))

        if trail_run:
            base_run_pace *= 1.05

        run_total_time_min = base_run_pace * 21.0975
        run_hours = int(run_total_time_min // 60)
        run_minutes = int(run_total_time_min % 60)

        st.write(f"**Estimated Run Split:** ⏱️ {run_hours}h {run_minutes}min")
    else:
        st.write("Enter at least one run distance/time to estimate your run split.")

    with st.expander("How this calculation works"):
        st.write("""
        Weighted average pace from your available run distances (5k, 10k, HM).
        Perceived effort adjusts the pace:
        - Effort > 9 → slightly slower (pushed harder)
        - Effort < 9 → faster (didn’t push maximally & had more in the tank)

        Carbon-plated shoes reduce pace by ~3%.
        Elevation adds ~2.5% slower per 100 m of gain.
        Trail adds ~5% slower pace.
        Fatigue from the 90 km bike is applied as an additional time penalty (~5% for a half marathon).
        Total run time = adjusted pace × 21.0975 km (half-Ironman distance).
        """)

        import time

            # --- PREDICTION BUTTON & ANIMATION (ONLY RUN PAGE) ---
    st.subheader("📊 See Your Predicted Ironman 70.3 Time")

    if st.button("See Predicted Time"):
        anim_placeholder = st.empty()   # Placeholder for sport animations
        pred_placeholder = st.empty()   # Placeholder for predicted total time (BIG & BOLD)
        diff_placeholder = st.empty()   # Placeholder for difference from user guess

        # --- Times in minutes ---
        swim_total_min = adjusted_total_sec / 60
        bike_total_min = bike_time_minutes
        run_total_min_incl_transitions = run_total_time_min + 5  # +5 min for T1+T2
        total_actual_min = swim_total_min + bike_total_min + run_total_min_incl_transitions

        # --- Animation settings ---
        steps = 80
        delay = 0.02

        # Animate Swim
        for i in range(1, steps + 1):
            current_swim = swim_total_min * i / steps
            h = int(current_swim // 60)
            m = int(current_swim % 60)
            s = int((current_swim - h*60 - m) * 60)
            anim_placeholder.markdown(f"**🏊 Swim:** {h}h {m}m {s}s")
            time.sleep(delay)

        # Animate Bike
        for i in range(1, steps + 1):
            current_bike = bike_total_min * i / steps
            h = int(current_bike // 60)
            m = int(current_bike % 60)
            s = int((current_bike - h*60 - m) * 60)
            anim_placeholder.markdown(
                f"**🏊 Swim:** {int(swim_total_min // 60)}h {int(swim_total_min % 60)}m | "
                f"🚴 Bike: {h}h {m}m {s}s"
            )
            time.sleep(delay)

        # Animate Run (+T1/T2)
        for i in range(1, steps + 1):
            current_run = run_total_min_incl_transitions * i / steps
            h = int(current_run // 60)
            m = int(current_run % 60)
            s = int((current_run - h*60 - m) * 60)
            anim_placeholder.markdown(
                f"**🏊 Swim:** {int(swim_total_min // 60)}h {int(swim_total_min % 60)}m | "
                f"🚴 Bike: {int(bike_total_min // 60)}h {int(bike_total_min % 60)}m | "
                f"🏃 Run + T1/T2: {h}h {m}m {s}s"
            )
            time.sleep(delay)

        # Show Total and Difference
        total_h = int(total_actual_min // 60)
        total_m = int(total_actual_min % 60)
        total_s = int((total_actual_min - total_h*60 - total_m) * 60)
        pred_placeholder.markdown(f"## ⏱️ Total Predicted Time: {total_h}h {total_m}m {total_s}s")

        diff_min = total_actual_min - user_predicted_total_min
        diff_h = int(abs(diff_min) // 60)
        diff_m = int(abs(diff_min) % 60)
        diff_s = int((abs(diff_min) - diff_h*60 - diff_m) * 60)

        if diff_min > 0:
            diff_placeholder.markdown(
                f"*You are {diff_h}h {diff_m}m {diff_s}s short from your predicted time.*"
            )
        elif diff_min < 0:
            diff_placeholder.markdown(
                f"*You overshot your prediction by {diff_h}h {diff_m}m {diff_s}s! Congrats!*"
            )
        else:
            diff_placeholder.markdown("*Perfect prediction! 🎉*")





 











