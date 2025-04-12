### Create QR CODE for demo


import qrcode

# Replace with your Streamlit app's URL
streamlit_url = "https://megaproject-ectdn2kyf3kv6rgkwbqxgh.streamlit.app/"

# Generate the QR code
qr = qrcode.make(streamlit_url)

# Save the QR code as an image
qr.save("app/streamlit_qr.png")
