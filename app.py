"""
Save user info in deta db cloud.

Streamlit provides user interface to save info entered by user.
"""


from typing import List, Dict
import streamlit as st
from deta import Deta


def insert(db, email, username, name, password):
    """
    Insert info to db.
    """
    db.put({'key': username, 'email': email, 'username': username, 'name': name, 'password': password})
    st.success('info is saved')


def check(db, username):
    """
    Check if username is already in the db.
    """
    db_content: List[Dict] = db.fetch().items
    for u in db_content:
        if username in u["key"]:
            st.error(f"Sorry username {username} is already used. Try another username.")
            return False
    return True


def createdb(deta, dbname: str):
    """
    Create a deta db with dbname.
    """
    db = deta.Base(f"{dbname}")
    return db

def create_credentials(db_content):
    """
    Create a dict of dict from db_content
    """
    d = {}
    for u in db_content:
        username = u['username']
        d.update({username: u})

    return {'usernames': d}      


def main():
    db = None
    dbname = 'users'

    # Register new user.
    with st.expander('REGISTER'):
        with st.form("form", clear_on_submit=True):
            email = st.text_input("Your email")
            username = st.text_input("Your username")
            name = st.text_input("Your name")
            password = st.text_input("Your password", type='password')
            submitted = st.form_submit_button("Store in database")

    # Connect to Deta db with your project Key.
    PROJECT_KEY = st.secrets["deta_key"]
    deta = Deta(PROJECT_KEY)

    # Insert user info in db.
    if submitted:
        db = createdb(deta, dbname)
        if check(db, username):
            insert(db, email, username, name, password)

    # Show db content.
    with st.expander('DB RECORDS', expanded=True):
        isrecord = st.button('Show db')
        if isrecord:
            db = createdb(deta, dbname)
            db_content: List[Dict] = db.fetch().items
            st.write(f"Database name: {dbname}")
            st.dataframe(db_content)

    if st.button('create credential'):
        db = createdb(deta, dbname)
        db_content: List[Dict] = db.fetch().items
        d = create_credentials(db_content)
        print(d)


if __name__ == '__main__':
    main()
