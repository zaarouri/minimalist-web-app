import streamlit as st
import requests

API_URL = "http://localhost:5000/employees"  # Change the URL as per your server

# Function to get all employees from the Flask backend
def get_employees():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to add an employee via the Flask backend
def add_employee(name, position):
    new_employee = {'name': name, 'position': position}
    response = requests.post(API_URL, json=new_employee)
    return response.json()

# Function to update an employee via the Flask backend
def update_employee(employee_id, name, position):
    updated_employee = {'name': name, 'position': position}
    url = f"{API_URL}/{employee_id}"
    response = requests.put(url, json=updated_employee)
    return response.json()

# Function to delete an employee via the Flask backend
def delete_employee(employee_id):
    url = f"{API_URL}/{employee_id}"
    response = requests.delete(url)
    return response.json()

def main():
    st.title('Employee Management System')

    menu = ['View Employees', 'Add Employee', 'Update Employee', 'Delete Employee']
    choice = st.sidebar.selectbox('Select Operation', menu)

    if choice == 'View Employees':
        st.header('Employee Records')
        employees = get_employees()
        if not employees:
            st.write("No employee records available.")
        else:
            for employee in employees:
                st.write(f"ID: {employee['id']}, Name: {employee['name']}, Position: {employee['position']}")

    elif choice == 'Add Employee':
        st.header('Add Employee')
        name = st.text_input('Enter name')
        position = st.text_input('Enter position')
        if st.button('Add'):
            result = add_employee(name, position)
            st.write(result)

    elif choice == 'Update Employee':
        st.header('Update Employee')
        employee_id = st.text_input('Enter employee ID to update')
        name = st.text_input('Enter new name')
        position = st.text_input('Enter new position')
        if st.button('Update'):
            result = update_employee(employee_id, name, position)
            st.write(result)

    elif choice == 'Delete Employee':
        st.header('Delete Employee')
        employee_id = st.text_input('Enter employee ID to delete')
        if st.button('Delete'):
            result = delete_employee(employee_id)
            st.write(result)

if __name__ == '__main__':
    main()
