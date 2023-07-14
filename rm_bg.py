import streamlit as st
from rembg import remove
from PIL import Image
import tempfile
import os

def remove_background(image):
    with st.spinner("Processing..."):
        # Open the image
        inp = Image.open(image)

        # Remove the background
        output = remove(inp)

        return output

def download_processed_image(processed_image):
    # Create a temporary file path
    temp_file_path = os.path.join(tempfile.gettempdir(), "processed_image.png")

    # Save the processed image to the temporary file path
    processed_image.save(temp_file_path)

    # Set the download path to the user's "Downloads" folder
    download_folder = os.path.expanduser("~/Downloads")
    os.makedirs(download_folder, exist_ok=True)
    download_path = os.path.join(download_folder, "processed_image.png")

    # Move the temporary file to the download path
    os.rename(temp_file_path, download_path)

    # Return the download path
    return download_path

def main():
    # Set the app title and description
    st.set_page_config(
        page_title="Background Remover App",
        page_icon=":scissors:",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Read the contents of the external CSS file
    css = """
    <style>
    {}
    </style>
    """.format(open("templates/main.css").read())

    # Add the external CSS styles
    st.markdown(css, unsafe_allow_html=True)

    # App content
    st.title("Background Remover App")
    st.write("Upload a photo and remove the background")

    # Create a file uploader
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Process the uploaded image and get the processed image
        processed_image = remove_background(uploaded_file)

        # Display the processed image
        st.image(processed_image, caption="Processed Image", use_column_width=True)

        # Create a download button for the processed image
        if st.button("Download Processed Image"):
            download_path = download_processed_image(processed_image)
            st.markdown(f"**Instructions to download the processed image:**")
            st.markdown(f"1. Right-click on the image.")
            st.markdown(f"2. Choose 'Save Image As' or similar option.")
            st.markdown(f"3. Select the desired location to save the image on your device.")
            st.markdown(f"4. Click 'Save' to download the image.")

if __name__ == "__main__":
    main()
