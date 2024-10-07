import streamlit as st
import joblib
import pandas as pd
from PIL import Image
import os

# Load model and label encoder
model = joblib.load('salary_predictor_model.pkl')
le = joblib.load('label_encoder.pkl')

# Function to load all images from a directory
def load_images(directory):
    images = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            img = Image.open(image_path)
            images[filename] = img
    return images

# Load images
image_directory = 'player_images'
images = load_images(image_directory)

# Extract specific images
main_image = images.get('ipl.jpg', None)  # Main image
secondary_image = images.get('cricket_image2.jpg', None)  # Additional image

# Resize function for player images (increased size)
def resize_image(image, width=250, height=250):
    return image.resize((width, height))

# Resize player images
player_images = {name: resize_image(img) for name, img in images.items() if name not in ['ipl.jpg', 'cricket_image2.jpg']}

# Resize the main cricket image
if main_image:
    main_image = main_image.resize((800, 400))  # Adjust size as needed

# Streamlit App
st.set_page_config(page_title="IPL Player Salary Predictor", page_icon=":cricket_ball:", layout="wide")

# Title
st.title("IPL Auction Price Prediction")

# Layout: Container for main content and side images
left_col, right_col = st.columns([3, 1])

with left_col:
    if main_image:
        st.image(main_image, use_column_width=True)
    
    if secondary_image:
        st.image(secondary_image, use_column_width=True, caption="IPL Highlights")

    # Add descriptive content directly below images
    st.markdown("""
        ## About This Website
        Welcome to the **IPL Player Salary Predictor**! This web application allows you to predict the future salary of IPL players based on historical data.

        **Features:**
        - **Enter Player Name**: Provide the name of the IPL player.
        - **Select Future Year**: Choose a year for which you want to predict the salary.
        - **Predict**: Click the "Predict Salary" button to see the estimated salary.

        The application uses historical salary data to predict future earnings. Simply input the player’s name and the year you’re interested in, and our model will provide an estimate of their salary.

        Enjoy exploring the potential earnings of your favorite IPL stars!
    """)

    # Input Fields
    st.subheader("Predict Player Salary")

    input_col1, input_col2 = st.columns([2, 1])

    with input_col1:
        player_name = st.text_input("Enter Player Name", "")
        year = st.number_input("Enter Year", min_value=2025, max_value=2100, value=2025)

    with input_col2:
        st.markdown("")  # Empty space for layout

    # Predict Salary
    if st.button("Predict Salary"):
        if player_name:
            try:
                # Encode the player name
                player_name_encoded = le.transform([player_name])[0]

                # Prepare the input for prediction
                input_data = pd.DataFrame([[player_name_encoded, year]], columns=['Name', 'Year'])

                # Predict
                predicted_salary = model.predict(input_data)[0]
                predicted_salary_formatted = "{:,.0f}".format(predicted_salary)

                st.success(f"The predicted salary for {player_name} in {year} is ₹{predicted_salary_formatted}.")
            except:
                st.error("Player name not found in the data.")
        else:
            st.error("Please enter a valid player name.")
st.markdown(
    """
    <footer style='text-align: center; font-size: 18px;'>
        <p>Developed by <a href='https://www.linkedin.com/in/neeraj-sanka-4a5599240/' target='_blank'>Jithendar Neeraj Sanka</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)

with right_col:
    st.subheader("Top Players")

    # Container for player images with horizontal scroll
    with st.container():
        st.markdown("<style> .scrollable { overflow-x: auto; white-space: nowrap; } </style>", unsafe_allow_html=True)
        st.markdown('<div class="scrollable">', unsafe_allow_html=True)
        
        # Display player images side by side
        for filename, img in player_images.items():
            st.image(img, width=250, caption=filename.replace('.jpg', '').replace('.png', '').title(), use_column_width=False)
        
        st.markdown('</div>', unsafe_allow_html=True)


# Additional Styling
st.markdown("""
    <style>
    .stTitle {
        font-size: 32px;
        color: #1f77b4;
        font-weight: bold;
    }
    .stSubheader {
        font-size: 26px;
        color: #ff6347;
        font-weight: bold;
    }
    .stMarkdown {
        font-size: 18px;
        color: #333;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .css-1d391kg {
        padding: 20px;
    }
    .css-1u5n39h {
        margin-top: 20px;
    }
    .scrollable {
        overflow-x: auto;
        white-space: nowrap;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)
