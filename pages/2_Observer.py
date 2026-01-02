import streamlit as st

st.title("👁️ Observer")

world = st.session_state.get("world")
mind = st.session_state.get("mind")
schedule = st.session_state.get("schedule")

if not world or not mind or not schedule:
    st.warning("System not birthed yet. Open the main page first.")
    st.stop()

st.subheader("Day Summary")
status = schedule.status()
st.json({
    "day": status["day"],
    "state": status["state"],
    "events_total": status["events_total"],
    "event_index": status["event_index"],
    "current_place": status["current_place"],
    "current_room": status["current_room"],
})

colA, colB = st.columns(2)

with colA:
    st.subheader("Event Timeline (what A7DO experienced)")
    if schedule.events:
        for idx, ev in enumerate(schedule.events, start=1):
            st.write(f"**Event {idx}** — {ev.place_id}/{ev.room}")
            st.caption(f"people: {', '.join(ev.presence) if ev.presence else '—'} | pets: {', '.join(ev.pets) if ev.pets else '—'}")
            st.caption(f"sounds_spoken: {', '.join(ev.sounds_spoken) if ev.sounds_spoken else '—'}")
            st.caption(f"body@event: {ev.body if ev.body else '—'}")
    else:
        st.info("No events loaded.")

with colB:
    st.subheader("Mind Activity (thinking timeline)")
    # show last ~40 activity records
    activity = getattr(mind, "activity", [])
    if activity:
        for row in activity[-40:]:
            st.write(row)
    else:
        st.info("No mind activity yet.")

st.divider()

st.subheader("Learning Signals")
mind_summary = mind.summary()
st.json(mind_summary)

st.subheader("Lexicon (top)")
words = mind.known_words()
if words:
    top = list(words.items())[:30]
    st.write({k: v for k, v in top})
else:
    st.info("No lexical exposures yet.")

st.subheader("Traces (observed co-presence)")
traces = getattr(mind, "trace", [])
if traces:
    for t in traces[-25:]:
        st.write(t)
else:
    st.info("No traces yet.")

st.divider()

st.subheader("Movement Logs")
st.write("**A7DO movement**")
if schedule.movements:
    for m in schedule.movements[-25:]:
        st.write(m)
else:
    st.info("No A7DO movement logged yet.")

st.write("**Background bot movement (Observer-only)**")
moves = getattr(world, "last_bot_movements", [])
if moves:
    for m in moves:
        st.write(m)
else:
    st.info("No background movements recorded for this day yet (build a day).")