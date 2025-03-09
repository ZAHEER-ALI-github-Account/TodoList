import streamlit as st
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 task TEXT NOT NULL,
                 status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Add a task
def add_task(task):
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "Pending"))
    conn.commit()
    conn.close()

# Get all tasks
def get_tasks():
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

# Update task status
def update_task_status(task_id, status):
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()

# Delete a task
def delete_task(task_id):
    conn = sqlite3.connect("todo.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Streamlit UI
st.title("Advanced To-Do List")

# Add task section
task_input = st.text_input("Enter a new task:")
if st.button("Add Task"):
    if task_input:
        add_task(task_input)
        st.success("Task added successfully!")
        st.rerun()
    else:
        st.warning("Task cannot be empty.")

# Display tasks
tasks = get_tasks()
if tasks:
    for task in tasks:
        task_id, task_text, status = task
        col1, col2, col3 = st.columns([6, 2, 2])
        col1.write(f"{task_text} ({status})")
        if col2.button("Complete", key=f"complete_{task_id}"):
            update_task_status(task_id, "Completed")
            st.rerun()
        if col3.button("Delete", key=f"delete_{task_id}"):
            delete_task(task_id)
            st.rerun()
else:
    st.write("No tasks available.")
