import streamlit as st
import pandas as pd
from io import BytesIO

from weather_data_getter import get_weather_file
from pdf_generator import generate
from SAM_Models import standalone_battery

default_state = {
    'address': '',
    'interval_data': [],
    'started': False,
    'weather_file': [],
    'report_file': [],
    'SAM_data': []
}

def view():
    if len(default_state) != len(st.session_state):
        for key in default_state:
            st.session_state[key] = default_state[key]
    
    st.title('SAM Projection - Cadenza BESS')

    show_form()

    if st.session_state['started']:
        st.header('Weather File')
        st.write(st.session_state['weather_file'])
        st.download_button(label='Download Report (.pdf)', data=st.session_state['report_file'], file_name='report.pdf', mime='application/pdf')

def show_form():
    with st.form("form"):
        form = {}
        form['address'] = st.text_input(label='Address', value=st.session_state['address'])
        form['interval_data'] = st.file_uploader(label="Interval Data")
        st.session_state['started'] = st.form_submit_button(label="Start")

        if st.session_state['started']:
            # Save Session
            for key in form:
                st.session_state[key] = form[key]
            st.success('Saved State!')

            st.session_state['weather_file'] = get_weather_file(form['address']) if form['address'] != '' else get_weather_file()
            st.session_state['SAM_data'] = standalone_battery.run({'resource': st.session_state['weather_file']})

            st.session_state['report_file'] = generate(st.session_state)


if __name__ == '__main__':
    view()