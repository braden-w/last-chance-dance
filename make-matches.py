import streamlit as st
import pandas as pd

st.title('Last Chance Dance Matches')

# Prompt user to upload a CSV file. To get this, go to Google Sheets and download the file as a CSV.
sheet_url = st.file_uploader('Upload a CSV file with the list of participants', type='csv')

if sheet_url is not None:
    data = pd.read_csv(sheet_url)

    # Set up input fields for column names
    name_column = st.text_input('Enter the column name with the participant\'s name', 'Your Full Name (First, Last)')
    email_column = st.text_input('Enter the column name with the participant\'s email', 'Email Address')
    netid_column = st.text_input('Enter the column name with the participant\'s NetID', 'NetID')
    romantic_matches_column = st.text_input('Enter the column name with the romantic matches', 'Romantic Matches')
    platonic_matches_column = st.text_input('Enter the column name with the platonic matches', 'Platonic Matches')
    hail_mary_column = st.text_input('Enter the column name with the hail mary option', 'The Hail Mary')

    # Indexing data for fast lookup
    index_data = {row[netid_column]: row for index, row in data.iterrows()}

    # Dictionary to store matches
    matches = {
        'romantic_matches': {},
        'platonic_matches': {}
    }

    for netid, row in index_data.items():
        # Get romantic matches
        try:
            romantic_netids = row[romantic_matches_column].split('\n')
            romantic_match_found = [match for match in romantic_netids if netid in index_data.get(match, {}).get(romantic_matches_column, '').split('\n')]
            matches['romantic_matches'][netid] = romantic_match_found
        except AttributeError:
            matches['romantic_matches'][netid] = []

        # Get platonic matches
        try:
            platonic_netids = row[platonic_matches_column].split('\n')
            platonic_match_found = [match for match in platonic_netids if netid in index_data.get(match, {}).get(platonic_matches_column, '').split('\n')]
            matches['platonic_matches'][netid] = platonic_match_found
        except AttributeError:
            matches['platonic_matches'][netid] = []

    # Display matches in Streamlit
    for match_type, match_dict in matches.items():
        st.subheader(f'{match_type.capitalize()} Results')
        for netid, netid_matches in match_dict.items():
            st.write(f'{netid}: {", ".join(netid_matches) if netid_matches else "No matches found"}')
