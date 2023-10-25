import streamlit as st 
import requests
import cv2
import pandas as pd

# Function to search for nutrition data
def search_food_data(search_string):
    # Replace 'YOUR_API_KEY' with your actual API key from FoodData Central.
    api_key = 'YOUR_API_KEY'
    
    # The base URL for the FoodData Central API.
    base_url = 'https://api.nal.usda.gov/fdc/v1/'

    # Construct the URL for the search endpoint.
    search_url = f'{base_url}foods/search'

    # Parameters for the search request.
    params = {
        'query': search_string,
        'api_key': api_key
    }

    try:
        # Send the GET request to the API.
        response = requests.get(search_url, params=params)

        # Check if the request was successful.
        if response.status_code == 200:
            data = response.json()
            if data['foods']:
                # Extract and display nutrition information for the first result.
                food = data['foods'][0]
                return food
            else:
                return None
        else:
            return None
    except Exception as e:
        return None

# Streamlit app
def main():
    st.title("Food Data and Image Recognition App")
    
    # Search for nutrition data
    st.header("Search for Nutrition Data")
    search_string = st.text_input("Enter a food item to search for:")
    if st.button("Search"):
        if search_string:
            food_data = search_food_data(search_string)
            if food_data:
                st.write(f"Food: {food_data['description']}")
                st.write("Nutrition Information:")
                for nutrient in food_data['foodNutrients']:
                    st.write(f"{nutrient['nutrientName']}: {nutrient['value']} {nutrient['unitName']}")
            else:
                st.write("No results found for the given search string.")
    
    # Food object recognition
    st.header("Food Object Recognition from Image")
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        # You can use image recognition libraries like OpenCV or deep learning models for food object recognition here.
        # For brevity, this example doesn't include actual food object recognition code.
        st.write("Food objects recognized:")
        st.dataframe(pd.DataFrame(columns=["Food Object"]))

if __name__ == "__main__":
    main()
