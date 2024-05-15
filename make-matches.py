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
		display_data = []

		for netid, row in index_data.items():
			romantic_matches = []
			platonic_matches = []

			# Get romantic matches
			try:
				romantic_netids = row[romantic_matches_column].split('\n')
				romantic_matches = [{
						'NetID': match,
						'Name': index_data[match][name_column],
						'Email': index_data[match][email_column]
				} for match in romantic_netids if match in index_data and netid in index_data.get(match, {}).get(romantic_matches_column, '').split('\n')]
			except AttributeError:
				romantic_matches = []

			# Get platonic matches
			try:
				platonic_netids = row[platonic_matches_column].split('\n')
				platonic_matches = [{
						'NetID': match,
						'Name': index_data[match][name_column],
						'Email': index_data[match][email_column]
				} for match in platonic_netids if match in index_data and netid in index_data.get(match, {}).get(platonic_matches_column, '').split('\n')]
			except AttributeError:
				platonic_matches = []

			# Prepare data for display
			display_data.append({
				'Name': row[name_column],
				'NetID': netid,
				'Email': row[email_column],
				'Romantic Matches (NetIDs)': "\n".join([m['NetID'] for m in romantic_matches]),
				'Romantic Matches (Names)': "\n".join([m['Name'] for m in romantic_matches]),
				'Romantic Matches (Emails)': "\n".join([m['Email'] for m in romantic_matches]),
				'Platonic Matches (NetIDs)': "\n".join([m['NetID'] for m in platonic_matches]),
				'Platonic Matches (Names)': "\n".join([m['Name'] for m in platonic_matches]),
				'Platonic Matches (Emails)': "\n".join([m['Email'] for m in platonic_matches])
			})

		display_df = pd.DataFrame(display_data)
		st.table(display_df)

	else:
		st.error('Invalid Google Sheet URL or Sheet ID. Please enter a valid Google Sheet URL or Sheet ID.')
