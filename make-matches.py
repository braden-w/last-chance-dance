import streamlit as st
import pandas as pd
import numpy as np

st.title('Last Chance Dance Matches')

# Prompt user to upload a CSV file. To get this, go to Google Sheets and download the file as a CSV.
sheet_url = st.file_uploader('Upload a CSV file with the list of participants', type='csv')

# Prompt user for column name with the participant's name in "First, Last". Default to "Your Full Name (First, Last)"
name_column = st.text_input('Enter the column name with the participant\'s name', 'Your Full Name (First, Last)')

# Prompt user for column name with the participant's email. Default to "Email Address"
email_column = st.text_input('Enter the column name with the participant\'s email', 'Email Address')

# Prompt user for column name with the participant's NetID. Default to "NetID"
netid_column = st.text_input('Enter the column name with the participant\'s NetID', 'NetID')

# Prompt user for column name with romantic matches. Default to "Romantic Matches"
romantic_matches_column = st.text_input('Enter the column name with the romantic matches', 'Romantic Matches')

# Prompt user for column name with platonic matches. Default to "Platonic Matches"
platonic_matches_column = st.text_input('Enter the column name with the platonic matches', 'Platonic Matches')

# Prompt user for column name with the hail mary option. Default to "The Hail Mary"
hail_mary_column = st.text_input('Enter the column name with the hail mary option', 'The Hail Mary')

