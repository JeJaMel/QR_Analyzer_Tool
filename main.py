# import pyqrcode
# from pyzbar.pyzbar import decode
# from PIL import Image
#
# qr = pyqrcode.create('Verga Luisana si es bella vale!')
# qr.png('je.png', scale=8)
#
# d = decode(Image.open('je.png'))
# print(d[0].data.decode('ascii'))

import pyqrcode
from pyzbar.pyzbar import decode
from PIL import Image
import streamlit as st
import os
import re

def generate_qr_code(data, filename="qrcode.png"):
    """Generates a QR code and saves it to a file."""
    try:
        qr = pyqrcode.create(data)
        qr.png(filename, scale=8)
        return filename
    except Exception as e:
        st.error(f"Error generating QR code: {e}")
        return None


def decode_qr_code(image_path):
    """Decodes a QR code from an image file.  Returns the decoded data as a string, or None if decoding fails."""
    try:
        img = Image.open(image_path)
        decoded_data = decode(img)

        if decoded_data:
            return decoded_data[0].data.decode('utf-8')  # Decode the byte string
        else:
            return None
    except Exception as e:
        st.error(f"Error decoding QR code: {e}")
        return None

def is_valid_url(url):
    """Checks if the given string is a valid URL starting with 'https://www.example.com'."""
    pattern = r"^https:\/\/www\.example\.com\/.*$"
    return bool(re.match(pattern, url))


def validate_qr_content(decoded_data):
    """Validates the content of a QR code based on predefined rules."""
    if decoded_data:
        if is_valid_url(decoded_data):
            return True, "Valid URL (starts with https://www.example.com/)"
        else:
            return False, "Invalid URL (does not match the required pattern)"
    else:
        return False, "No data found in QR code."

# --- Streamlit ---

def main():
    st.title("QR Code Scanner and Validator")

    # QR Code Generation Section
    st.header("Generate QR Code")
    data_to_encode = st.text_input("Enter data to encode into the QR code:")
    if st.button("Generate QR Code"):
        if data_to_encode:
            qr_filename = generate_qr_code(data_to_encode)
            if qr_filename:
                try:
                    st.image(Image.open(qr_filename), caption="Generated QR Code", use_column_width=True)
                    st.write(f"QR code saved as: {qr_filename}")
                except FileNotFoundError:
                    st.error("Error: Could not load the generated QR code image.  Check the file path.")

        else:
            st.warning("Please enter data to encode.")

    # QR Code Scanning Section
    st.header("Scan and Validate QR Code")
    uploaded_file = st.file_uploader("Upload a QR code image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Save the uploaded file
        try:
            with open("temp_qr.png", "wb") as f:
                f.write(uploaded_file.getbuffer())  # Use getbuffer() for general file-like objects

            st.image(Image.open(uploaded_file), caption="Uploaded QR Code", use_column_width=True)  # Display the image
            decoded_data = decode_qr_code("temp_qr.png")  # Decode from the saved file
            if decoded_data:
                st.success(f"Decoded data: {decoded_data}")
                is_valid, message = validate_qr_content(decoded_data)
                if is_valid:
                    st.success(f"Validation: {message}")
                else:
                    st.error(f"Validation: {message}")
            else:
                st.error("Could not decode QR code.  Make sure the image is clear and contains a valid QR code.")
        except Exception as e:
            st.error(f"An error occurred during processing: {e}")
        finally:
            # Clean up the temp file after processing
            if os.path.exists("temp_qr.png"):
                os.remove("temp_qr.png")  # Ensure file removal even if there's an error

if __name__ == "__main__":
    main()
