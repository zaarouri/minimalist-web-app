from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)

# Create a database engine (using SQLite for demonstration purposes)
engine = create_engine('sqlite:///employees.db', connect_args={"check_same_thread": False})
Base = declarative_base()

# Define the Employee model
class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(String)

# Create tables in the database
Base.metadata.create_all(engine)

# Function to create session
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

# API endpoints
@app.route('/employees', methods=['GET'])
def get_employees():
    session = create_session()
    employees = session.query(Employee).all()
    session.close()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees])

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    session = create_session()
    new_employee = Employee(name=data['name'], position=data['position'])
    session.add(new_employee)
    session.commit()
    session.close()
    return jsonify({'message': 'Employee added successfully'})

@app.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    session = create_session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    session.close()
    if employee:
        return jsonify({'id': employee.id, 'name': employee.name, 'position': employee.position})
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.get_json()
    session = create_session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        employee.name = data['name']
        employee.position = data['position']
        session.commit()
        session.close()
        return jsonify({'message': 'Employee updated successfully'})
    else:
        return jsonify({'message': 'Employee not found'}), 404

@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    session = create_session()
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        session.close()
        return jsonify({'message': 'Employee deleted successfully'})
    else:
        return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app on localhost
