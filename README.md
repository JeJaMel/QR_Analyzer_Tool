# QR Code Scanner and Validator

This project is a simple web application built with Streamlit that allows you to:

*   Generate QR codes from text input.
*   Scan and decode QR codes from uploaded images.
*   Validate the content of decoded QR codes based on a predefined URL pattern.

## Prerequisites

*   Python 3.7+
*   A Google Colab environment (for easy setup)
*   An ngrok account and API key (for exposing the application via a public URL)

## Libraries Used

*   `pyqrcode`: For generating QR codes.
*   `pyzbar`: For decoding QR codes from images.
*   `pillow`: For image processing.
*   `streamlit`: For creating the web interface.
*   `pyngrok`: For creating an ngrok tunnel to make the app publicly accessible.
*   `pypng`: To make sure that it saves images

## Setup and Usage in Google Colab

1.  **Clone/Copy the Code:**
    *   Create a folder in your Google Drive (e.g., `QR_script`).
    *   Upload the `main.py` file to that folder.

2.  **Google Colab Setup:**

    *   Create a new Google Colab notebook.
    *   Copy and paste the following code blocks into separate cells in the notebook:

        **Block 1: Mount Google Drive (Optional)**

        ```python
        from google.colab import drive
        drive.mount('/content/drive')
        ```

        *   **Note:** This block is only necessary if you plan to load or save QR code images from/to your Google Drive. If you only intend to work with uploaded files, you can skip this step.

        **Block 2: Install Dependencies**

        ```python
        !pip install pyqrcode pyzbar pillow streamlit pyngrok pypng
        ```

        *   This cell installs all the necessary Python libraries.  Make sure to run this cell first.

        **Block 3: ZBar Library Installation (Conditional)**

        ```python
        try:
            from pyzbar.pyzbar import decode
            print("pyzbar imported successfully (ZBar library likely already installed).")
        except ImportError:
            print("ZBar library not found. Installing...")
            !apt-get install -y zbar-tools
            import os
            os.kill(os.getpid(), 9)  # Restart the runtime after installing ZBar
        ```

        *   This block attempts to import `pyzbar`. If it fails, it installs the ZBar library using `apt-get` and restarts the Colab runtime.

        **Block 4: Ngrok Setup and Streamlit Execution**

        ```python
        from pyngrok import ngrok

        ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN")  # Replace with your ngrok API key

        tunnel = ngrok.connect(addr="8501", proto="http", bind_tls=True)  # Streamlit's default port

        public_url = tunnel.public_url
        print(f"Public URL: {public_url}")

        !streamlit run --server.port 8501 /content/drive/MyDrive/QR_script/main.py &
        ```

        *   **Important:** Replace `"YOUR_NGROK_AUTHTOKEN"` with your actual ngrok API key.
        *   This block sets up the ngrok tunnel, retrieves the public URL, and starts the Streamlit server, pointing to your `main.py` script in Google Drive.

3.  **Run the Colab Notebook:**

    *   Execute the cells in the notebook one by one, in order.
    *   After the last cell executes, you will see a "Public URL" printed in the output.
    *   Click on the URL to access the web application in your browser.

## How to Use the Web Application

1.  **Generate QR Code:**

    *   Enter the text you want to encode into the "Enter data to encode into the QR code:" text input field.
    *   Click the "Generate QR Code" button.
    *   The generated QR code will be displayed. You can download the QR code image using the "Download QR Code" button.

2.  **Scan and Validate QR Code:**

    *   Upload a QR code image using the "Upload a QR code image" file uploader.
    *   The application will decode the QR code. If the decoding is successful:
        *   The decoded data will be displayed.
        *   The application will validate the decoded data against the URL pattern `https://www.example.com/...`.
        *   A message indicating whether the validation was successful or not will be displayed.
        *   You can download the decoded data as a text file using the "Save and Download Base64 Text File" button.
