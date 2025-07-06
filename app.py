import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()  

TEXT_API_KEY = os.getenv("TEXT_API_KEY")
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")

st.set_page_config(page_title="Imaginate", layout="centered")

st.title("Imaginate: AI Story and Image Generator by Daniel Paul Samuel")

def generate_story_with_openrouter(prompt, model="deepseek/deepseek-r1-0528-qwen3-8b:free"):
    headers = {
        "Authorization": f"Bearer {TEXT_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a creative story generator. Write vivid, imaginative short stories based on a prompt."
            },
            {
                "role": "user",
                "content": f"Write a short story based on this prompt: {prompt} with a max word limit of 250 words."
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def generate_image_with_imagerouter(prompt):
    url = "https://api.imagerouter.io/v1/openai/images/generations"
    payload = {
        "prompt": prompt,
        "model": "google/gemini-2.0-flash-exp:free"  
    }
    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        image_url = response.json()["data"][0]["url"]
        image_data = requests.get(image_url)
        return Image.open(BytesIO(image_data.content))
    else:
        st.warning(f"Image generation failed: {response.status_code} - {response.text}")
        return None 

# --- User Prompt Input ---
user_prompt = st.text_input("Enter your story prompt:", placeholder="e.g., A time traveler visits ancient Egypt")

# --- Generate Button ---
if st.button("Generate"):
    if user_prompt.strip() == "":
        st.warning("Please enter a valid prompt.")
    else:
        with st.spinner("Generating story..."):
            generated_story = generate_story_with_openrouter(user_prompt)
            st.subheader("📖 Generated Story")
            st.write(generated_story)

            image = generate_image_with_imagerouter(user_prompt)

            if image:
                st.markdown("<div class='image-box'>", unsafe_allow_html=True)
                st.subheader("🖼️ Generated Image")
                st.image(image, caption="AI-generated image", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Image could not be generated.")

else:
    st.info("Enter a prompt and click 'Generate' to get started.")

# --- Styling ---
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)


