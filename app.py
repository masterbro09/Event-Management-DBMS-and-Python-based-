import streamlit as st
import pandas as pd
from database import create_database, get_db_connection
import altair as alt


# Initialize database
create_database()

# Streamlit application
st.set_page_config(page_title="Event Management System", layout="wide")

st.title("🎉 Event Management System")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Home", "Manage Events", "Manage Attendees", "Analytics"])

if menu == "Home":
    st.write("Welcome to the Event Management System! Use the sidebar to navigate.")

elif menu == "Manage Events":
    st.subheader("Manage Events")

    # Form to add a new event
    with st.form("event_form"):
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Event Date")
        venue_id = st.number_input("Venue ID", min_value=1, step=1)
        ticket_price = st.number_input("Ticket Price", min_value=0.0, step=0.1)
        submit = st.form_submit_button("Add Event")

        if submit:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Events (EventName, EventDate, VenueID, TicketPrice) VALUES (?, ?, ?, ?)",
                           (event_name, event_date, venue_id, ticket_price))
            conn.commit()
            conn.close()
            st.success("Event added successfully!")

    # Display and delete events
    conn = get_db_connection()
    df_events = pd.read_sql_query("SELECT * FROM Events", conn)

    if not df_events.empty:
        st.write("### Events List")
        st.dataframe(df_events)

        event_id_to_delete = st.number_input("Enter Event ID to delete", min_value=1, step=1)
        if st.button("Delete Event"):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Events WHERE EventID = ?", (event_id_to_delete,))
            conn.commit()
            st.success(f"Event with ID {event_id_to_delete} deleted successfully!")
            conn.close()
    else:
        st.info("No events available.")

elif menu == "Manage Attendees":
    st.subheader("Manage Attendees")

    # Form to add a new attendee
    with st.form("attendee_form"):
        attendee_name = st.text_input("Attendee Name")
        attendee_email = st.text_input("Attendee Email")
        event_id = st.number_input("Event ID", min_value=1, step=1)
        ticket_price = st.number_input("Ticket Price", min_value=0.0, step=0.1)
        submit = st.form_submit_button("Add Attendee")

        if submit:
            conn = get_db_connection()
            cursor = conn.cursor()
            try:
                # Add attendee
                cursor.execute("INSERT INTO Attendees (AttendeeName, Email) VALUES (?, ?)",
                               (attendee_name, attendee_email))
                attendee_id = cursor.lastrowid

                # Assign ticket to attendee
                cursor.execute("INSERT INTO Tickets (EventID, AttendeeID, Price) VALUES (?, ?, ?)",
                               (event_id, attendee_id, ticket_price))
                conn.commit()
                st.success("Attendee added and ticket assigned successfully!")
            except sqlite3.IntegrityError:
                st.error("Email already exists. Please use a unique email.")
            conn.close()

    # Display and delete attendees
    conn = get_db_connection()
    df_attendees = pd.read_sql_query("SELECT * FROM Attendees", conn)

    if not df_attendees.empty:
        st.write("### Attendees List")
        st.dataframe(df_attendees)

        attendee_id_to_delete = st.number_input("Enter Attendee ID to delete", min_value=1, step=1)
        if st.button("Delete Attendee"):
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Attendees WHERE AttendeeID = ?", (attendee_id_to_delete,))
            conn.commit()
            st.success(f"Attendee with ID {attendee_id_to_delete} deleted successfully!")
            conn.close()
    else:
        st.info("No attendees available.")

elif menu == "Analytics":
    st.subheader("Event Analytics")

    # Query data for analytics
    conn = get_db_connection()
    query = '''
        SELECT 
            e.EventName AS Event, 
            COUNT(t.TicketID) AS Attendees, 
            COALESCE(SUM(t.Price), 0) AS Revenue,
            e.EventDate AS Date
        FROM Events e
        LEFT JOIN Tickets t ON e.EventID = t.EventID
        GROUP BY e.EventID
    '''
    df_analytics = pd.read_sql_query(query, conn)
    conn.close()

    # Display analytics
    st.write("### Event Analytics")
    if not df_analytics.empty:
        st.dataframe(df_analytics)

        # Scatter Plot: Revenue vs Attendees
        st.write("### Scatter Plot: Revenue vs Attendees")
        st.altair_chart(
            alt.Chart(df_analytics).mark_circle(size=60).encode(
                x='Attendees',
                y='Revenue',
                color='Event',
                tooltip=['Event', 'Attendees', 'Revenue']
            ).interactive()
        )

        # Line Chart: Revenue Over Time
        st.write("### Line Chart: Revenue Over Time")
        df_analytics['Date'] = pd.to_datetime(df_analytics['Date'])  # Convert date column
        df_sorted = df_analytics.sort_values('Date')
        st.line_chart(df_sorted.set_index('Date')[['Revenue']])

        # Line Chart: Attendees Over Time
        st.write("### Line Chart: Attendees Over Time")
        st.line_chart(df_sorted.set_index('Date')[['Attendees']])

        # Bar Chart: Revenue by Event
        st.write("### Revenue by Event (Bar Chart)")
        st.bar_chart(df_analytics.set_index("Event")["Revenue"])

        # Scatter Plot: Date vs Revenue
        st.write("### Scatter Plot: Date vs Revenue")
        st.altair_chart(
            alt.Chart(df_analytics).mark_point(filled=True, size=100).encode(
                x='Date:T',
                y='Revenue',
                color='Event',
                tooltip=['Event', 'Revenue', 'Date']
            ).interactive()
        )
    else:
        st.info("No analytics data available. Add events and attendees first.")
