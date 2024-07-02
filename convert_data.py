import streamlit as st
import function as func

st.title('Data Converter')

file = st.file_uploader('Upload your excel file:')
if file is not None:
    new_file = func.convert(file)

    st.write('Here is the converted data:')
    st.download_button(label="Download",
                       data=new_file,
                       file_name="updated data cms.csv",
                       mime="text/csv")