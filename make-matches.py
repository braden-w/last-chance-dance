import streamlit as st
import pandas as pd
import re

st.title('Last Chance Dance Matches')

google_sheet_input = st.text_input('Enter the public Google Sheet URL or Sheet ID. Google Sheet must be public to anyone with the link for this app to work.')

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
		romantic_matches_pairs = set()
		platonic_matches_pairs = set()

		for current_netid, current_row in netid_to_row.items():
			current_romantic_matches = []
			current_platonic_matches = []

			# Get romantic matches
			try:
				romantic_netids = current_row[romantic_matches_column].split('\n')
				current_romantic_matches = [{
						'NetID': romantic_netid,
						'Name': netid_to_row[romantic_netid][name_column],
						'Email': netid_to_row[romantic_netid][email_column]
				} for romantic_netid in romantic_netids if romantic_netid in netid_to_row and current_netid in netid_to_row.get(romantic_netid, {}).get(romantic_matches_column, '').split('\n')]
				for match in current_romantic_matches:
						pair = tuple(sorted([current_row[email_column], match['Email']]))
						romantic_matches_pairs.add(pair)
			except AttributeError:
				current_romantic_matches = []

			# Get platonic matches
			try:
				platonic_netids = current_row[platonic_matches_column].split('\n')
				current_platonic_matches = [{
						'NetID': platonic_netid,
						'Name': netid_to_row[platonic_netid][name_column],
						'Email': netid_to_row[platonic_netid][email_column]
				} for platonic_netid in platonic_netids if platonic_netid in netid_to_row and current_netid in netid_to_row.get(platonic_netid, {}).get(platonic_matches_column, '').split('\n')]
				for match in current_platonic_matches:
						pair = tuple(sorted([current_row[email_column], match['Email']]))
						platonic_matches_pairs.add(pair)
			except AttributeError:
				current_platonic_matches = []

			# Prepare data for display
			display_data.append({
				'Name': current_row[name_column],
				'NetID': current_netid,
				'Email': current_row[email_column],
				'Romantic Matches': current_romantic_matches,
				'Platonic Matches': current_platonic_matches
			})

		# Filter out participants who did not get any matches
		display_df = pd.DataFrame(display_data)
		display_df = display_df[(display_df['Romantic Matches'].map(len) > 0) | (display_df['Platonic Matches'].map(len) > 0)]
		st.table(display_df)
		# Display count
		st.write(f'Total number of rows: {len(display_df)}')

		st.subheader('Romantic Matches')
		romantic_matches_data = []
		for row in display_data:
			if row['Romantic Matches']:
				romantic_matches_data.append({
					'Name': row['Name'],
					'Email': row['Email'],
					'Romantic Matches': ', '.join([f"{match['Name']} ({match['Email']})" for match in row['Romantic Matches']])
				})
		romantic_df = pd.DataFrame(romantic_matches_data)
		st.table(romantic_df)

		st.subheader('Platonic Matches')
		platonic_matches_data = []
		for row in display_data:
			if row['Platonic Matches']:
				platonic_matches_data.append({
					'Name': row['Name'],
					'Email': row['Email'],
					'Platonic Matches': ', '.join([f"{match['Name']} ({match['Email']})" for match in row['Platonic Matches']])
				})
		platonic_df = pd.DataFrame(platonic_matches_data)
		st.table(platonic_df)

		st.subheader('These People Received Hail Mary')
		hail_mary_data = []
		for current_netid, current_row in netid_to_row.items():
			try:
				hail_mary_netid = current_row[hail_mary_column]
				if hail_mary_netid in netid_to_row:
					hail_mary_data.append({
						"NetID": hail_mary_netid,
						"Receiver's Email": netid_to_row[hail_mary_netid][email_column],
						"Receiver's Name": netid_to_row[hail_mary_netid][name_column],
						"Sender's NetID": current_netid,
						"Sender's Name": current_row[name_column],
						"Sender's Email": current_row[email_column]
					})
			except KeyError:
				continue
		hail_mary_df = pd.DataFrame(hail_mary_data)
		st.table(hail_mary_df)

		# Generate CSVs
		romantic_matches_csv = pd.DataFrame([", ".join(pair) for pair in romantic_matches_pairs], columns=['Romantic Matches'])
		romantic_matches_csv.to_csv('romantic_matches.csv', index=False)
		platonic_matches_csv = pd.DataFrame([", ".join(pair) for pair in platonic_matches_pairs], columns=['Platonic Matches'])
		platonic_matches_csv.to_csv('platonic_matches.csv', index=False)

		hail_mary_csv = hail_mary_df[["Receiver's Email", "Receiver's Name", "Sender's Name", "Sender's NetID", "Sender's Email"]]
		hail_mary_csv.to_csv('hail_mary_matches.csv', index=False)

		st.subheader('Download CSVs')
		st.download_button(label='Download Romantic Matches CSV', data=romantic_matches_csv.to_csv(index=False), file_name='romantic_matches.csv', mime='text/csv')
		st.download_button(label='Download Platonic Matches CSV', data=platonic_matches_csv.to_csv(index=False), file_name='platonic_matches.csv', mime='text/csv')
		st.download_button(label='Download Hail Mary Matches CSV', data=hail_mary_csv.to_csv(index=False), file_name='hail_mary_matches.csv', mime='text/csv')

	else:
		st.error('Invalid Google Sheet URL or Sheet ID. Please enter a valid Google Sheet URL or Sheet ID, and make sure the Google Sheet is public to anyone with the link.')
