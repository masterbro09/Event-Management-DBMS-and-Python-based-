Event Management System

This Event Management System is a web-based application built using Streamlit and SQLite. It allows users to manage events, attendees, and tickets while providing analytics with interactive visualizations for better trend analysis.

Features

Manage Events

Add new events with details like:

Event Name

Event Date

Venue ID

Ticket Price

View all events in a tabular format.

Delete specific events by their Event ID.

Manage Attendees

Add new attendees with details like:

Attendee Name

Email

Assign them to an Event.

Specify ticket price.

View all attendees in a tabular format.

Delete specific attendees by their Attendee ID.

Event Analytics

Generate insights on:

Total revenue per event.

Total attendees per event.

Interactive visualizations including:

Scatter Plot: Revenue vs. Attendees.

Line Charts: Revenue and Attendees over time.

Bar Chart: Revenue by event.

Scatter Plot: Date vs. Revenue.

Technologies Used

Backend:

SQLite: Lightweight database for storing event, attendee, and ticket information.

Frontend:

Streamlit: Framework for building interactive web applications.

Visualizations:

Altair: For scatter plots and other interactive visualizations.

Streamlit Charts: For line and bar charts.

Installation and Setup

Prerequisites

Python 3.9 or above installed.

Install Required Libraries

Run the following command to install dependencies:

pip install streamlit pandas altair sqlite3

Clone the Repository

Clone the project repository (if applicable) or copy the project files into a local directory.

Run the Application

Start the Streamlit server by running:

streamlit run app.py

Access the Application

Open your browser and navigate to:

http://localhost:8501

Directory Structure

event_management/
├── app.py         # Main Streamlit application
├── database.py    # Database setup and utility functions
├── README.md      # Project documentation
├── requirements.txt  # List of dependencies

How to Use

Manage Events:

Navigate to the "Manage Events" section using the sidebar.

Add new events or delete existing ones.

View a list of all events in tabular format.

Manage Attendees:

Navigate to the "Manage Attendees" section.

Add new attendees and assign them tickets for events.

View and manage attendee information.

Analytics:

Navigate to the "Analytics" section.

View insights and trends with:

Revenue vs. Attendees Scatter Plot.

Revenue Over Time Line Chart.

Attendees Over Time Line Chart.

Revenue by Event Bar Chart.

Known Issues

Ensure all required data (e.g., event and attendee details) is entered correctly to avoid data integrity issues.

Future Improvements

Add user authentication for managing events and attendees securely.

Enable file export (e.g., CSV or Excel) for event and attendee data.

Advanced analytics using machine learning (e.g., event success predictions).
