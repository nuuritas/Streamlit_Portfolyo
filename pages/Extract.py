import streamlit as st
from midas_extract import midas_exporter
import tempfile

filename = "midas_8.pdf"

# portfoy_df, investment_df, hesap_df = midas_exporter(filename)

uploaded_file = st.file_uploader("Choose a file",accept_multiple_files=False,type=['pdf'])
if uploaded_file is not None:
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        # Save the uploaded file's content to the temporary file
        temp_file.write(uploaded_file.getvalue())
        # Ensure the data is flushed to the file
        temp_file.flush()

        # Now you can use temp_file.name as the filename for your function
        # midas1 = parser.from_file(temp_file.name)["content"]
        portfoy_df, investment_df, hesap_df = midas_exporter(temp_file.name)

    st.dataframe(portfoy_df)



