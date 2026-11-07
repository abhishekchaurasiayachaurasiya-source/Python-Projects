import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Smart Library Management System", layout="wide")

# Initialize Session State for Data Persistence
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame([
        {"Book ID": 1, "Title": "Python Crash Course", "Author": "Eric Matthes", "Category": "Programming", "Status": "Available", "Issued To": "-"},
        {"Book ID": 2, "Title": "Atomic Habits", "Author": "James Clear", "Category": "Self-Help", "Status": "Available", "Issued To": "-"},
        {"Book ID": 3, "Title": "Clean Code", "Author": "Robert C. Martin", "Category": "Programming", "Status": "Issued", "Issued To": "Rahul Sharma"},
        {"Book ID": 4, "Title": "The Alchemist", "Author": "Paulo Coelho", "Category": "Fiction", "Status": "Available", "Issued To": "-"},
    ])

if 'members' not in st.session_state:
    st.session_state.members = pd.DataFrame([
        {"Member ID": 101, "Name": "Rahul Sharma", "Email": "rahul@gmail.com", "Type": "Student"},
        {"Member ID": 102, "Name": "Priya Verma", "Email": "priya@gmail.com", "Type": "Faculty"},
    ])

if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame([
        {"Book": "Clean Code", "Member": "Rahul Sharma", "Date": "2026-06-01", "Action": "Issued"},
        {"Book": "Atomic Habits", "Member": "Priya Verma", "Date": "2026-06-02", "Action": "Returned"},
    ])

# Main Application Header
st.title("📚 Smart Library Management System")
st.markdown("---")

# Sidebar Navigation for Requirements
menu = st.sidebar.radio("Navigation Menu", [
    "1. Library Interface", 
    "2. Books & Member Data", 
    "3. Borrowing Statistics", 
    "4. Book Recommendations", 
    "5. Book Search & Issue/Return"
])

# ----------------- 1. LIBRARY INTERFACE -----------------
if menu == "1. Library Interface":
    st.header("🏠 Library Dashboard & Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Books", len(st.session_state.books))
    col2.metric("Total Members", len(st.session_state.members))
    issued_count = len(st.session_state.books[st.session_state.books["Status"] == "Issued"])
    col3.metric("Books Currently Issued", issued_count)
    
    st.markdown("### 🕒 Recent Library Logs")
    st.dataframe(st.session_state.history, use_container_width=True)

# ----------------- 2. BOOKS & MEMBER DATA -----------------
elif menu == "2. Books & Member Data":
    st.header("📖 Books & Member Data Management")
    
    tab1, tab2 = st.tabs(["Manage Books", "Manage Members"])
    
    with tab1:
        st.subheader("Add New Book")
        with st.form("book_form"):
            b_title = st.text_input("Book Title")
            b_author = st.text_input("Author Name")
            b_category = st.selectbox("Category", ["Programming", "Self-Help", "Fiction", "Science", "History"])
            submit_book = st.form_submit_button("Add Book")
            
            if submit_book and b_title:
                new_id = len(st.session_state.books) + 1
                new_row = {"Book ID": new_id, "Title": b_title, "Author": b_author, "Category": b_category, "Status": "Available", "Issued To": "-"}
                st.session_state.books = pd.concat([st.session_state.books, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Book '{b_title}' added successfully!")
        
        st.subheader("All Books Database")
        st.dataframe(st.session_state.books, use_container_width=True)
        
    with tab2:
        st.subheader("Register New Member")
        with st.form("member_form"):
            m_name = st.text_input("Member Name")
            m_email = st.text_input("Email Address")
            m_type = st.selectbox("Member Type", ["Student", "Faculty", "Staff"])
            submit_member = st.form_submit_button("Register Member")
            
            if submit_member and m_name:
                new_m_id = 100 + len(st.session_state.members) + 1
                new_m_row = {"Member ID": new_m_id, "Name": m_name, "Email": m_email, "Type": m_type}
                st.session_state.members = pd.concat([st.session_state.members, pd.DataFrame([new_m_row])], ignore_index=True)
                st.success(f"Member '{m_name}' registered successfully!")
        
        st.subheader("All Members Database")
        st.dataframe(st.session_state.members, use_container_width=True)

# ----------------- 3. BORROWING STATISTICS -----------------
elif menu == "3. Borrowing Statistics":
    st.header("📊 Borrowing Statistics & Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Category Pie Chart
        cat_counts = st.session_state.books['Category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        fig1 = px.pie(cat_counts, names='Category', values='Count', title="Books Distribution by Category")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        # Status Bar Chart
        status_counts = st.session_state.books['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig2 = px.bar(status_counts, x='Status', y='Count', title="Available vs Issued Books", color='Status')
        st.plotly_chart(fig2, use_container_width=True)

# ----------------- 4. BOOK RECOMMENDATIONS -----------------
elif menu == "4. Book Recommendations":
    st.header("💡 Smart Book Recommendations")
    st.write("Get suggestions based on your preferred genre and reading categories.")
    
    selected_cat = st.selectbox("Choose Your Preferred Category:", st.session_state.books['Category'].unique())
    
    recommendations = st.session_state.books[st.session_state.books['Category'] == selected_cat]
    
    if not recommendations.empty:
        st.success(f"Recommended Books in **{selected_cat}**:")
        for idx, row in recommendations.iterrows():
            st.markdown(f"👉 **{row['Title']}** by *{row['Author']}* — Status: `{row['Status']}`")
    else:
        st.info("No recommendations found for this category.")

# ----------------- 5. BOOK SEARCH & ISSUE/RETURN -----------------
elif menu == "5. Book Search & Issue/Return":
    st.header("🔍 Real-Time Book Search & Issue/Return Desk")
    
    # Search Function
    query = st.text_input("Search by Book Title, Author or Category:")
    
    df = st.session_state.books
    if query:
        filtered_df = df[
            df['Title'].str.contains(query, case=False, na=False) |
            df['Author'].str.contains(query, case=False, na=False) |
            df['Category'].str.contains(query, case=False, na=False)
        ]
    else:
        filtered_df = df
        
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown("---")
    
    # Issue / Return Operations
    st.subheader("Manage Book Issuing / Returning")
    action = st.radio("Select Action Type:", ["Issue Book", "Return Book"])
    
    if action == "Issue Book":
        available_books = df[df['Status'] == 'Available']['Title'].tolist()
        members = st.session_state.members['Name'].tolist()
        
        if available_books and members:
            b_select = st.selectbox("Select Book to Issue", available_books)
            m_select = st.selectbox("Select Member", members)
            
            if st.button("Confirm Issue"):
                st.session_state.books.loc[st.session_state.books['Title'] == b_select, 'Status'] = 'Issued'
                st.session_state.books.loc[st.session_state.books['Title'] == b_select, 'Issued To'] = m_select
                
                new_log = {"Book": b_select, "Member": m_select, "Date": str(datetime.now().date()), "Action": "Issued"}
                st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_log])], ignore_index=True)
                st.success(f"Successfully issued '{b_select}' to {m_select}!")
                st.rerun()
        else:
            st.warning("No books available for issuing or no members registered.")
            
    else:
        issued_books = df[df['Status'] == 'Issued']['Title'].tolist()
        if issued_books:
            b_return = st.selectbox("Select Book to Return", issued_books)
            if st.button("Confirm Return"):
                holder = st.session_state.books.loc[st.session_state.books['Title'] == b_return, 'Issued To'].values[0]
                st.session_state.books.loc[st.session_state.books['Title'] == b_return, 'Status'] = 'Available'
                st.session_state.books.loc[st.session_state.books['Title'] == b_return, 'Issued To'] = '-'
                
                new_log = {"Book": b_return, "Member": holder, "Date": str(datetime.now().date()), "Action": "Returned"}
                st.session_state.history = pd.concat([st.session_state.history, pd.DataFrame([new_log])], ignore_index=True)
                st.success(f"Successfully returned '{b_return}'!")
                st.rerun()
        else:
            st.info("No books are currently issued.")