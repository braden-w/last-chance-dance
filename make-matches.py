import streamlit as st
import pandas as pd
import re

st.title('Last Chance Dance Matches')

google_sheet_input = st.text_input('Enter the public Google Sheet URL or Sheet ID')

def extract_sheet_id(input_string):
	# Regular expression to extract Sheet ID from the full URL or directly use the ID
	match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', input_string)
	if match:
		return match.group(1)
	elif re.match(r'^[a-zA-Z0-9-_]+$', input_string):
		return input_string
	return None

if google_sheet_input:
	google_sheet_id = extract_sheet_id(google_sheet_input)
	if google_sheet_id:
		csv_url = f'https://docs.google.com/spreadsheets/d/{google_sheet_id}/export?format=csv'
		data = pd.read_csv(csv_url)

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
				if netid_matches:
					st.write(f'{index_data[netid][name_column]} ({netid}) matched with:')
					for match in netid_matches:
						st.write(f'\t{index_data[match][name_column]} ({match})')
	
	else:
		st.error('Invalid Google Sheet URL or Sheet ID. Please enter a valid Google Sheet URL or Sheet ID.')