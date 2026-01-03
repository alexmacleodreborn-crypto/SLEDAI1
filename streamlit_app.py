if "a7do" not in st.session_state:
    st.session_state.a7do = A7DOState()
    st.session_state.world = WorldController()
    st.session_state.cycle = DayCycle(
        st.session_state.a7do,
        st.session_state.world
    )

if st.button("Run Birth"):
    st.session_state.cycle.initialise_if_needed()

if st.button("Run Day"):
    st.session_state.cycle.run_day()

if st.button("Sleep"):
    st.session_state.cycle.sleep()
    st.session_state.cycle.advance_day()