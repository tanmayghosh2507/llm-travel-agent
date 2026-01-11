import datetime
import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Planner ✈️", layout="centered")
start = datetime.datetime.now()

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1

if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip with us! Just input the details and we will plan as per your preferences.")

def get_page_headline() -> str:
    if st.session_state.step <= 2:
        return f"### {st.session_state.answers['location']} Trip"

    return (
        f"### {st.session_state.answers['location']} Trip - "
        f"{st.session_state.answers['days'][0].strftime('%B %d')} ({st.session_state.answers['arrival_time']}) "
        f"to {st.session_state.answers['days'][1].strftime('%B %d')} ({st.session_state.answers['departure_time']})"
    )

# STEP 1 — Location
if st.session_state.step == 1:
    location = st.text_input("Where do you want to visit?")
    
    if st.button("Next") and location:
        st.session_state.answers["location"] = location
        st.session_state.step = 2
        st.rerun()

# STEP 2 — Date
elif st.session_state.step == 2:
    st.markdown(get_page_headline())
    days = st.date_input(
        "When are you planning to visit?",
        (start, start + datetime.timedelta(days=7)),
        start,
        start + datetime.timedelta(days=730),
        format="MM/DD/YYYY",
    )

    if len(days) == 2:
        arrival_time = st.selectbox(
            f"When are you arriving on {days[0]}?",
            ["Morning", "Afternoon", "Evening", "Night"]
        )
        departure_time = st.selectbox(
            f"When are you departing on {days[1]}?",
            ["Morning", "Afternoon", "Evening", "Night"],
            index=2
        )

    if st.button("Next"):
        st.session_state.answers["days"] = days
        st.session_state.answers["arrival_time"] = arrival_time
        st.session_state.answers["departure_time"] = departure_time
        st.session_state.step = 3
        st.rerun()
    elif st.button("Back"):
        st.session_state.step = 1
        st.rerun()

# STEP 3 — Commute preference
elif st.session_state.step == 3:
    st.markdown(get_page_headline())
    commute = st.multiselect(
        "Preferred commute option(s)",
        ["Rental Car", "Public Transportation", "Cabs", "Bike", "Walk"],
        max_selections=3
    )
    
    if commute:
        if st.button("Next"):
            st.session_state.answers["commute"] = commute
            st.session_state.step = 4
            st.rerun()
    elif st.button("Doesn't matter"):
        st.session_state.step = 4
        st.rerun()

    if st.button("Back"):
        st.session_state.step = 2
        st.rerun()

# STEP 4 — Focus
elif st.session_state.step == 4:
    st.markdown(get_page_headline())
    if "commute" in st.session_state.answers:
        st.markdown(f"**Commute Preference:** {', '.join(st.session_state.answers['commute'])}")
    focus = st.multiselect(
        "Key focus",
        [
            "Food",
            "Nightlife",
            "Romantic Getaway",
            "Nature & Wildlife",
            "Guided Tours & Shows",
            "Shopping & Markets",
            "Culture & Heritage",
            "Adventure & Sports",
            "Relaxation & Wellness",
            "Family-Friendly Activities",
            "Hidden Gems",
            "Luxury Experiences",
            "Budget-Friendly Options"
        ],
        max_selections=5
    )

    if focus:
        if st.button("Next"):
            st.session_state.answers["focus"] = focus
            st.session_state.step = 5
            st.rerun()
    elif st.button("Nothing in mind!"):
        st.session_state.step = 5
        st.rerun()
    
    if st.button("Back"):
        st.session_state.step = 3
        st.rerun()


# STEP 5 — Specifics
elif st.session_state.step == 5:
    st.markdown(get_page_headline())
    if "commute" in st.session_state.answers:
        st.markdown(f"**Commute Preference:** {', '.join(st.session_state.answers['commute']) if st.session_state.answers['commute'] else 'No preference'}")
    if "focus" in st.session_state.answers:
        st.markdown(f"**Key Focus:** {', '.join(st.session_state.answers['focus']) if st.session_state.answers['focus'] else 'No specific focus'}")
    specifics = st.text_area(
        "Any specific places, events or activities you want to include?",
        help="E.g., 'Visit the Eiffel Tower', 'Watch a NBA match', 'Hike the Rattlesnake Ridge' etc."
    )

    if st.button("Create Travel Plan"):
        if specifics:
            st.session_state.answers["specifics"] = specifics
        st.session_state.step = 6
        st.rerun()
    elif st.button("Back"):
        st.session_state.step = 4
        st.rerun()

elif st.session_state.step == 6:
    payload = {
        "destination": st.session_state.answers["location"],
        "start": st.session_state.answers["days"][0].isoformat() + "," + st.session_state.answers["arrival_time"],
        "end": st.session_state.answers["days"][1].isoformat() + "," + st.session_state.answers["departure_time"],
    }

    if "commute" in st.session_state.answers:
        payload["commute"] = st.session_state.answers["commute"]
    if "focus" in st.session_state.answers:
        payload["focus"] = st.session_state.answers["focus"]
    if "specifics" in st.session_state.answers:
        payload["specifics"] = st.session_state.answers["specifics"]

    with st.spinner("Generating your travel plan..."):
        try:
            response = requests.post(
                "http://localhost:8000/generate-plan",
                json=payload,
                timeout=150
            )

            response.raise_for_status()
            result = response.json()
            
            if "status" in result and result["status"] == 1:
                st.success("Travel Plan Created!")
                st.write(result["plan"])
            else:
                st.error("Travel Plan couldn't be created! Error: " + str(result["plan"]))
                
        except requests.exceptions.Timeout:
            st.error("Request timed out. The AI model may be loading. Please try again in a moment.")
        except requests.exceptions.ConnectionError:
            st.error("Connection error. Make sure the backend server is running on http://localhost:8000")
        except Exception as e:
            st.error(f"Error: {str(e)}")
