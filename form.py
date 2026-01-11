import datetime
import streamlit as st
import requests

st.title("AI Travel Planner ✈️")
st.markdown("Plan your perfect trip with us! Just input the details and we will plan as per your preferences.")

destination = st.text_input("Where do you want to visit?")

start = datetime.datetime.now()
days = st.date_input(
    "When are you planning to visit?",
    (start, start + datetime.timedelta(days=7)),
    start,
    start + datetime.timedelta(days=730),
    format="MM/DD/YYYY",
)

# times = st.time_input(
#     "Preferred time to travel (if any)?",
#     datetime.datetime.now(),
# )

commute = st.multiselect(
    "Preferred commute options",
    ["Rental", "Public Transportation", "Ride Sharing", "Biking", "Walking"]
)

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
    ]
)

specifics = st.text_area(
    "Any specific places or activities you want to include?",
    help="E.g., 'Visit the Eiffel Tower', 'Hiking in the Grand Canyon', etc."
)

if st.button("Create Travel Plan"):
    if not destination:
        st.error("Please enter a destination")
    else:
        payload = {
            "destination": destination,
            "start": days[0].isoformat(),
            "end": days[1].isoformat(),
            "commute": commute,
            "focus": focus,
            "specifics": specifics
        }

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