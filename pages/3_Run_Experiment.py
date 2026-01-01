import streamlit as st

from a7do.schedule import Schedule
from a7do.mind import A7DOMind
from a7do.planner import birth_sequence, drive_home_sequence, arrive_home_sequence
from a7do.future_paths import FuturePathRegistry
from a7do.events import ExperienceEvent
from a7do.profiles import ObjectProfile

st.title("✅ Run Experiment — Authorise Wake + Execute Schedule")

world = st.session_state.get("world")
profiles = st.session_state.get("profiles")
if not world:
    st.warning("Create World Cage first.")
    st.stop()
if not profiles or not profiles.has_parents():
    st.warning("Create World Profiles first (Mum + Dad).")
    st.stop()

if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()
schedule = st.session_state.schedule

if "mind" not in st.session_state:
    st.session_state.mind = A7DOMind(world_map=world, profiles=profiles, schedule=schedule)
mind = st.session_state.mind

if "future_paths" not in st.session_state:
    st.session_state.future_paths = FuturePathRegistry()
registry = st.session_state.future_paths

status = schedule.status()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Day", status["day"])
c2.metric("State", status["state"])
c3.metric("Place", status["place_id"])
c4.metric("Events Remaining", status["events_remaining"])

st.divider()

colA, colB, colC = st.columns(3)

with colA:
    if st.button("Load Day 0 (Birth→Drive→Home)"):
        evs = []
        evs += birth_sequence(world, schedule)
        evs += drive_home_sequence(world, schedule)
        evs += arrive_home_sequence(world, schedule)
        schedule.load(0, evs, start_place="hospital_cwh", start_room="delivery_room")
        st.success(f"Loaded Day 0 with {len(evs)} events.")
        st.rerun()

with colB:
    if st.button("Authorise Wake"):
        schedule.authorise_wake()
        mind.trace.append({"phase": "wake", "day": schedule.day, "place_id": schedule.spatial.place_id})
        st.rerun()

with colC:
    if st.button("Step 1 Event", disabled=(schedule.state != "awake")):
        ev = schedule.next_event()
        if ev is None:
            schedule.sleep()
            mind.sleep()
            schedule.complete()
        else:
            mind.ingest(ev)
        st.rerun()

st.divider()

st.subheader("Build Day 2 from Approved Paths (Observer-side registry → events)")

if st.button("Build Day 2 from Approved Paths"):
    approved = registry.list(status="approved")
    if not approved:
        st.warning("No approved paths in registry. Go to Observer page and approve some.")
    else:
        evs = []
        start_place, start_room = "house_a7do", "living_room"

        # convert approved paths → grounded events
        for p in approved[:10]:
            if p.type == "object":
                name = p.proposal.get("name", "object")
                if name not in profiles.objects:
                    profiles.objects[name] = ObjectProfile(
                        name=name,
                        category=p.proposal.get("category", "toy"),
                        colour=p.proposal.get("colour"),
                        shape=p.proposal.get("shape"),
                        affordances=p.proposal.get("affordances", []),
                    )
                evs.append(ExperienceEvent(
                    place_id=start_place, room=start_room,
                    agent="Dad", action="showed", obj=name,
                    narrator="Grounded object exposure at home",
                    emphasis=[name.upper()],
                    sound={"pattern": "gentle voice"},
                    touch={"pattern": "held near hands", "temp": "warm"},
                    presence=["Dad", "Mum"],
                    body=schedule.body.snapshot(),
                ))
                registry.mark_scheduled(p.path_id)

            elif p.type == "person":
                speaker = p.proposal.get("name")
                if speaker:
                    evs.append(ExperienceEvent(
                        place_id=start_place, room=start_room,
                        agent=speaker, action="said", obj="hello",
                        narrator="Neighbour greeting (transaction recorded)",
                        sound={"pattern": "hello voice"},
                        touch={"pattern": "pat"},
                        presence=[speaker, "Mum", "Dad"],
                        body=schedule.body.snapshot(),
                        transaction={"target": "A7DO", "outcome": "calm"}
                    ))
                    registry.mark_scheduled(p.path_id)

            elif p.type == "routine" and p.proposal.get("name") == "short_walk_to_park":
                evs.append(ExperienceEvent(
                    place_id="house_a7do", room="hall",
                    agent="Mum", action="carried", obj="you",
                    narrator="Movement to park",
                    motor={"type": "carried", "intensity": "steady"},
                    to_place_id="park_01",
                    pos_xyz=world.places["park_01"].pos_xyz,
                    sound={"pattern": "outside air"},
                    smell={"pattern": "grass"},
                    presence=["Mum", "Dad"],
                    body=schedule.body.snapshot(),
                ))
                registry.mark_scheduled(p.path_id)

        schedule.load(2, evs, start_place=start_place, start_room=start_room)
        st.success(f"Loaded Day 2 with {len(evs)} events from approved paths.")
        st.rerun()

st.divider()
st.subheader("Queue Preview")
if schedule.queue:
    for i, ev in enumerate(schedule.queue[:25], 1):
        st.write(f"**{i}.** {ev.place_id}:{ev.room} | {ev.agent} {ev.action} {ev.obj or ''} → {ev.to_place_id or ''}")
else:
    st.info("No queue loaded.")