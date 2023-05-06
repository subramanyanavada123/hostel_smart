import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import requests

def get_latitude_longitude(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
    response = requests.get(url).json()
    if len(response) > 0:
        latitude = response[0]['lat']
        longitude = response[0]['lon']
        return latitude, longitude
    else:
        return None

# Load dataset
df = pd.read_csv('/home/dinesh/Pictures/ETE/8TH SEM/python_scripts/hostel_database .csv')

# Main container
st.title('Government Hostels')
st.write('Use the filters below to search and sort the hostels.')

# Search feature
search_query = st.text_input('Search by Hostel Name')
df = df[df['Hostel_Name'].str.contains(search_query, case=False, na=False)]

# Sort by options
cities = df['City'].unique()
selected_city = st.selectbox('Select a city', cities)
sort_by = st.selectbox('Sort by', ['Government_Hostel', 'City', 'Price'])

# Sort dataframe
df = df[df['City'] == selected_city]
if sort_by == 'Government_Hostel':
    df = df[df['Government_Hostel'] == 'Yes']
df = df.sort_values(sort_by)

# Geocoder
geolocator = Nominatim(user_agent="hostel_app")

# Hostel container
for index, row in df.iterrows():
    hostel_name = row['Hostel_Name']
    fees = row['Price']
    seats_left = row['Seats_Left']
    gov_college = row['Government_Hostel']
    address = row['Address']

    # Highlight primary details with border and styling
    with st.container():
        st.markdown(
            f"""
            <div style="border: 1px solid #ccc; border-radius: 5px; padding: 10px; background-color: #f5f5f5;">
                <h3 style="color: #009688;">{hostel_name}</h3>
                <p><strong>Fees:</strong> {fees} per month</p>
                <p><strong>Seats Left:</strong> {seats_left}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dropdown-like behavior to show menu options
        if st.checkbox('Show Details', key=index):
            with st.expander('Details'):
                st.write('Government Hostels: {}'.format(gov_college))
                st.write('Phone Number: {}'.format(row['Phone_Number']))
                st.write('Email Address: {}'.format(row['Email_Address']))

                # Geocode address to retrieve latitude and longitude
                location = get_latitude_longitude(row['Address'])
                print(row['Address'])
                print(location)
        
                if location is not None:
                    latitude, longitude = location
                    maps_link = 'https://www.google.com/maps/@{},{},16.48h,63.22t/data=!3m5!1e1!3m3!1sABC123!2e0!3e2'.format(latitude, longitude)
                    st.write('[Locate on Google Maps]({})'.format(maps_link))
                else:
                    st.write('Unable to locate address on Google Maps.')
