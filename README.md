# Last Chance Dance Matches Streamlit App

https://yale-last-chance-dance-2024.streamlit.app/

![CleanShot 2024-05-15 at 08 50 07@2x](https://github.com/braden-w/last-chance-dance/assets/13159333/b4a426d9-2f9c-4df9-a929-52d6bb104d6e)

## Overview
This Streamlit application is designed for Yale's Last Chance Dance tradition, allowing participants to input their desired matches via a Google Form, which then populates a Google Sheet. The app processes these responses to determine mutual (bi-directional) matches, both romantic and platonic. The output provides participants with their successful matches, fostering potential connections.

## Features
- Import data from a Google Sheet containing form responses.
- Configure column mappings for participants' names, emails, NetIDs, and their romantic and platonic match preferences.
- Identify and display mutual romantic and platonic matches based on the bi-directional preferences of participants.

## How to Run
1. Ensure you have Python and Streamlit installed.
2. Clone this repository to your local machine.
3. Run the Streamlit app using the following command:
   ```bash
   streamlit run make-matches.py
   ```
4. Open the provided local URL in a web browser to access the app.

## Input
The application requires a public Google Sheet URL or Sheet ID. The Sheet should have responses from a Google Form with the following columns (column names are configurable within the app):
- Participant's full name
- Email address
- NetID
- Romantic match preferences (NetIDs listed)
- Platonic match preferences (NetIDs listed)
- Optional: A "Hail Mary" match column for the person the participant wants to notify, no matter if here is a match or not.

## Algorithm
The matching algorithm works as follows:
1. **Data Extraction**: Fetches data from the specified Google Sheet.
2. **Data Indexing**: Creates a dictionary with NetIDs as keys for quick lookup.
3. **Match Calculation**:
   - For each participant, the app retrieves the list of desired matches (both romantic and platonic).
   - It checks if these desired matches have reciprocated the interest (i.e., if both parties have listed each other).
   - Only matches that are bi-directional are considered successful and are included in the output.
4. **Result Display**: Displays a table with participant details and their successful matches (NetIDs, names, and emails).

## Output
The app outputs a table listing each participant who has at least one mutual match. The table includes:
- Participant's name, NetID, and email.
- Lists of mutual romantic and platonic matches (showing NetIDs, names, and emails).

## Dependencies
- Python 3
- Streamlit
- Pandas

## Contributing
Contributions to enhance the functionality or efficiency of this app are welcome. Please follow the usual fork-and-pull request workflow.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.

---

This README provides a clear understanding of what the app does, how to set it up and run it, and the underlying matching algorithm. Adjustments or additional details can be added depending on specific needs or changes in the application functionality.
