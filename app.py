import streamlit as st
import pandas as pd
import os

# Custom Style for Background 
st.markdown("""
    <style>
   
    .stApp {
        background-color: #e6f0ff;  /* Light blue background */
    }

    header[data-testid="stHeader"] {
        background-color: #004080;  /* Dark blue navbar */
        color: white;
    }

    header[data-testid="stHeader"] h1 {
        color: white;
    }

    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# File name for saving contact information
csv_file = "contacts.csv"

# Load the CSV file if already exists, or start with empty data
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["First Name", "Last Name", "Address", "Email ID", "Phone Number"])

# Set the title and layout of the web page
st.set_page_config(page_title=" Keerthi's Contact Management application", layout="centered")
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("Welcome to Keerthi Contact Management Website ")

# Creating navigation tabs for different features
tab1, tab2, tab3, tab4 = st.tabs([" Add New", "Modify", " Delete", " View All"])

#  TAB 1: Add a new contact 
with tab1:
    st.subheader("Add New Contact")

    # Input form to get new contact details
    with st.form("add_contact_form", clear_on_submit=True):
        fname = st.text_input("First Name")  # User input for first name
        lname = st.text_input("Last Name")   # User input for last name
        address = st.text_area("Address")    # Address field
        email = st.text_input("Email ID")    # Email field
        phone = st.text_input("Phone Number")  # Phone number field

        submitted = st.form_submit_button("Add Contact")

        # Validations before adding new contact
        if submitted:
            if not fname or not lname or not address or not email or not phone:
                st.warning("Please fill in all fields.")
            elif "@" not in email or "." not in email:
                st.warning("Invalid email format.")
            elif not phone.isdigit() or len(phone) != 10:
                st.warning("Phone number must be 10 digits.")
            elif email in df["Email ID"].values:
                st.warning("This email already exists.")
            else:
                # Creating a new row with the entered data
                new_row = pd.DataFrame([{
                    "First Name": fname,
                    "Last Name": lname,
                    "Address": address,
                    "Email ID": email,
                    "Phone Number": phone
                }])
                # Adding the new contact to the data
                df = pd.concat([df, new_row], ignore_index=True)
                # Saving the updated data to CSV
                df.to_csv(csv_file, index=False)
                st.success(" Contact added successfully!")

#  TAB 2: Modify an existing contact 
with tab2:
    st.subheader("Modify Contact")
    if not df.empty:
        selected_email = st.selectbox("Select Email to Edit", df["Email ID"])
        contact = df[df["Email ID"] == selected_email].iloc[0]

        # Fields pre-filled with selected contact's info
        fname_edit = st.text_input("First Name", value=contact["First Name"], key="edit_fname")
        lname_edit = st.text_input("Last Name", value=contact["Last Name"], key="edit_lname")
        address_edit = st.text_area("Address", value=contact["Address"], key="edit_address")
        email_edit = st.text_input("Email ID", value=contact["Email ID"], key="edit_email")
        phone_edit = st.text_input("Phone Number", value=contact["Phone Number"], key="edit_phone")

        if st.button("Update Contact"):
            # Validations before updating
            if not fname_edit or not lname_edit or not address_edit or not email_edit or not phone_edit:
                st.warning("All fields must be filled.")
            elif email_edit != selected_email and email_edit in df["Email ID"].values:
                st.warning("Email already exists!")
            elif not phone_edit.isdigit() or len(phone_edit) != 10:
                st.warning("Phone number must be 10 digits.")
            else:
                # Updating the contact in the DataFrame
                df.loc[df["Email ID"] == selected_email] = [fname_edit, lname_edit, address_edit, email_edit, phone_edit]
                df.to_csv(csv_file, index=False)
                st.success(" Contact updated successfully!")
    else:
        st.info("No contacts found to modify.")

#  TAB 3: Delete a contact 
with tab3:
    st.subheader("Delete Contact")
    if not df.empty:
        delete_email = st.selectbox("Select Email to Delete", df["Email ID"])
        if st.button("Delete Contact"):
            # Remove the selected contact from the DataFrame
            df = df[df["Email ID"] != delete_email]
            df.to_csv(csv_file, index=False)
            st.success(" Contact deleted successfully!")
    else:
        st.info("No contacts available for deletion.")

# TAB 4: View all contacts 
with tab4:
    st.subheader("All Contacts")
    if not df.empty:
        # Displaying the entire contact list in a table
        st.dataframe(df)
    else:
        st.info("No contacts found.")

# Close styled container 
st.markdown('</div>', unsafe_allow_html=True)
