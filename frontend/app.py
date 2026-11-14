# Streamlit is used to build the web UI
import streamlit as st
# pandas is used to build a table from the user's inputs
import pandas as pd
# requests is used to call the Flask backend API
import requests

# Base URL of the Flask backend
# "backend" is the Docker container name; Docker's internal DNS resolves it
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("Airbnb Rental Price Prediction")

# ------------------------------------------------------------
# Section for online (single) prediction
# ------------------------------------------------------------
st.subheader("Online Prediction")

# Collect user input for property features
# Type of room being rented
room_type = st.selectbox("Room Type", ["Entire home/apt", "Private room", "Shared room"])
# Number of guests the property can host
accommodates = st.number_input("Accommodates (Number of guests)", min_value=1, value=2)
# Number of bathrooms
bathrooms = st.number_input("Bathrooms", min_value=1, step=1, value=2)
# Cancellation policy of the listing
cancellation_policy = st.selectbox("Cancellation Policy (kind of cancellation policy)", ["strict", "flexible", "moderate"])
# Whether a cleaning fee is charged
cleaning_fee = st.selectbox("Cleaning Fee Charged?", ["True", "False"])
# Whether the property can be booked instantly
instant_bookable = st.selectbox("Instantly Bookable?", ["False", "True"])
# Average review score (0 to 100)
review_scores_rating = st.number_input("Review Score Rating", min_value=0.0, max_value=100.0, step=1.0, value=90.0)
# Number of bedrooms
bedrooms = st.number_input("Bedrooms", min_value=0, step=1, value=1)
# Number of beds
beds = st.number_input("Beds", min_value=0, step=1, value=1)

# Convert user input into a DataFrame (one row)
input_data = pd.DataFrame([{
    'room_type': room_type,
    'accommodates': accommodates,
    'bathrooms': bathrooms,
    'cancellation_policy': cancellation_policy,
    'cleaning_fee': cleaning_fee,
    # The model expects 't' or 'f' instead of True/False
    'instant_bookable': 'f' if instant_bookable == "False" else "t",
    'review_scores_rating': review_scores_rating,
    'bedrooms': bedrooms,
    'beds': beds
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    try:
        # Send the inputs as JSON to the Flask API
        response = requests.post(
            f"{BACKEND_URL}/v1/rental",
            json=input_data.to_dict(orient='records')[0],
            timeout=30,  # don't wait forever if the backend is unresponsive
        )
        if response.status_code == 200:
            # Read the predicted price from the API response
            prediction = response.json()['Predicted Price (in dollars)']
            st.success(f"Predicted Rental Price (in dollars): {prediction}")
        else:
            # The API answered, but with an error
            st.error(f"Prediction API returned an error ({response.status_code}).")
    except requests.exceptions.RequestException:
        # The API could not be reached at all
        st.error("Unable to connect to the
