import streamlit as st
import pandas as pd
import re

st.title('Last Chance Dance Matches')

google_sheet_input = st.text_input('Enter the public Google Sheet URL or Sheet ID')

def extract_sheet_id(input_string):
	# Regular expression to extract Sheet ID from the full URL or directly use the ID
	regex_match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', input_string)
	if regex_match:
		return regex_match.group(1)
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
		netid_to_row = {row[netid_column]: row for index, row in data.iterrows()}

		# Dictionary to store matches
		display_data = []

		for current_netid, current_row in netid_to_row.items():
			romantic_matches = []
			platonic_matches = []

			# Get romantic matches
			try:
				romantic_netids = current_row[romantic_matches_column].split('\n')
				romantic_matches = [{
						'NetID': romantic_netid,
						'Name': netid_to_row[romantic_netid][name_column],
						'Email': netid_to_row[romantic_netid][email_column]
				} for romantic_netid in romantic_netids if romantic_netid in netid_to_row and current_netid in netid_to_row.get(romantic_netid, {}).get(romantic_matches_column, '').split('\n')]
			except AttributeError:
				romantic_matches = []

			# Get platonic matches
			try:
				platonic_netids = current_row[platonic_matches_column].split('\n')
				platonic_matches = [{
						'NetID': platonic_netid,
						'Name': netid_to_row[platonic_netid][name_column],
						'Email': netid_to_row[platonic_netid][email_column]
				} for platonic_netid in platonic_netids if platonic_netid in netid_to_row and current_netid in netid_to_row.get(platonic_netid, {}).get(platonic_matches_column, '').split('\n')]
			except AttributeError:
				platonic_matches = []

			# Prepare data for display
			display_data.append({
				'Name': current_row[name_column],
				'NetID': current_netid,
				'Email': current_row[email_column],
				'Romantic Matches (NetIDs)': "\n".join([match['NetID'] for match in romantic_matches]),
				'Romantic Matches (Names)': "\n".join([match['Name'] for match in romantic_matches]),
				'Romantic Matches (Emails)': "\n".join([match['Email'] for match in romantic_matches]),
				'Platonic Matches (NetIDs)': "\n".join([match['NetID'] for match in platonic_matches]),
				'Platonic Matches (Names)': "\n".join([match['Name'] for match in platonic_matches]),
				'Platonic Matches (Emails)': "\n".join([match['Email'] for match in platonic_matches])
			})

		# Filter out participants who did not get any matches
		display_df = pd.DataFrame(display_data)
		display_df = display_df[(display_df['Romantic Matches (NetIDs)'] != '') | (display_df['Platonic Matches (NetIDs)'] != '')]
		st.table(display_df)
		# Display count
		st.write(f'Total number of rows: {len(display_df)}')

	else:
		st.error('Invalid Google Sheet URL or Sheet ID. Please enter a valid Google Sheet URL or Sheet ID.')
