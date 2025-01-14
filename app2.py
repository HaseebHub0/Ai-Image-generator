import streamlit as st
import requests
from PIL import Image
import io
from streamlit_lottie import st_lottie

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
API_TOKEN = "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"  # Replace with your Hugging Face API token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Function to call Hugging Face API
def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

# Load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")

# Streamlit UI
st.set_page_config(page_title="Text-to-Image Generator", page_icon="🖌️", layout="wide")

# CSS styling
st.markdown(
    f"""
    <style>
    body {{
        font-family: 'Arial', sans-serif;
        background-image: url('background.png'); /* Image URL yahan daalein */
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }}
    .title {{
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #0A9047;
        margin-top: 50px;
        text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }}
    .subtitle {{
        font-size: 20px;
        text-align: center;
        color: #555;
        margin-top: 10px;
    }}
    .prompt-box {{
        margin: 30px auto;
        border: 2px solid #04E762;
        border-radius: 12px;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.8); /* Transparent background for the box */
        color: #333;
        width: 65%;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease-in-out;
    }}
    .prompt-box:hover {{
        transform: scale(1.02);
    }}
    .btn {{
        margin: 30px auto;
        display: block;
        font-size: 22px;
        background-color: #04E762;
        color: white;
        border-radius: 12px;
        padding: 15px 30px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }}
    .btn:hover {{
        background-color: #039653;
        transform: scale(1.05);
    }}
    .image-container {{
        text-align: center;
        margin-top: 40px;
        transition: transform 0.3s ease;
    }}
    .download-btn {{
        padding: 15px 40px;
        background-color: #ff6347;
        color: white;
        border-radius: 12px;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }}
    .download-btn:hover {{
        background-color: #ff4500;
        transform: scale(1.05);
    }}
    .loading-container {{
        margin-top: 30px;
    }}
    .card {{
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        padding: 20px;
        margin: 20px 0;
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease;
    }}
    .card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }}
    .card-header {{
        font-size: 25px;
        font-weight: bold;
        color: #04E762;
        margin-bottom: 10px;
    }}
    .card-body {{
        font-size: 18px;
        color: #333;
    }}
    .footer {{
        font-size: 15px;
        text-align: center;
        color: #888;
        margin-top: 50px;
    }}
    .footer a {{
        color: #04E762;
        text-decoration: none;
        font-weight: bold;
    }}
    .sidebar .sidebar-content {{
        background-color: #f4f4f4;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar content
st.sidebar.markdown('<div class="title">🖌️ Generate Your Image</div>', unsafe_allow_html=True)

# Sidebar form
with st.sidebar.form(key="generate_form"):
    prompt = st.text_input("Enter your image description:")
    style = st.selectbox(
        "Select a style for your image:",
        ["Realistic", "Cartoon", "Anime", "Surreal", "Abstract"]
    )
    generate_button = st.form_submit_button("Generate Image")
    
    
st.sidebar.markdown('</div></div>', unsafe_allow_html=True)
# When the button is pressed
if generate_button:
        if prompt.strip():  # Check if the prompt is not empty
            with st.spinner("Generating your image..."):
                # Append the selected style to the prompt
                styled_prompt = f"{prompt}, in {style} style"
                
                # Show loading animation
                st_lottie(lottie_animation, height=200, key="loading", speed=1)

                response = generate_image(styled_prompt)

                if response.status_code == 200:
                    # Process and display the image
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))

                    # Resize the image to fit better
                    image = image.resize((image.width // 2, image.height // 2))

                    # Displaying image and download button outside the sidebar (in the main area)
                    st.image(image, caption=f"Generated Image in {style} Style", use_container_width=True)

                    # Provide download button outside the form
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format="PNG")
                    img_bytes.seek(0)

                    # Displaying the download button
                    st.markdown('<div class="image-container">Click the button below to download the image:</div>', unsafe_allow_html=True)
                    st.download_button(
                        label="Download Image",
                        data=img_bytes,
                        file_name="generated_image.png",
                        mime="image/png",
                        key="download"
                    )
                else:
                    st.error(f"Failed to generate image: {response.status_code} - {response.json().get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a description to generate an image.")
# Footer Section
st.markdown('<div class="footer">Created with ❤️ by <a href="https://www.linkedin.com/in/muhammad-haseeb-739884317/" target="_blank">Muhammad Haseeb</a></div>', unsafe_allow_html=True)
