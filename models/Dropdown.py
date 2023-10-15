from models.Department import *
from models.Employee import *
# Get all drop down items from the database

class Dropdown(object):


    def get_position_values():
        departments = Department.query.order_by(Department.id.desc()).all()
        # create new dict and store all values to dict
        department_position_relations = {}
        # iterate over departments and store each id and name in variablles
        for row in departments:
            key = row.deptName
            dept_id = row.id

            # select all Position that belong to department
            position = Position.query.filter_by(deptID = dept_id).all()

            # build new list structure(service_lst) that includes the names of the position that belong
            # to the selected department
            position_lst = []
            for row in position:
                position_lst.append(row.positionName)

            # update the dictionary with position name as a key
            department_position_relations[key] = position_lst
            
        return department_position_relations
    
    def get_employee_values():
        departments = Department.query.order_by(Department.id.desc()).all()
        # create new dict and store all values to dict
        department_employee_relations = {}
        # iterate over departments and store each id and name in variablles
        for row in departments:
            key = row.deptName
            dept_id = row.id

            # select all employees that belong to department
            employees = Employee.query.filter_by(department = dept_id).all()

            # build new list structure(employee_lst) that includes the names of the employees that belong
            # to the selected department
            employee_lst = []
        
            for row in employees:
                employee_lst.append(row.full_name)

            # update the dictionary with service name as a key
            department_employee_relations[key] = employee_lst
    
        return department_employee_relations
    
    def get_collage_values():
        collage = collage.query.order_by(collage.id.desc()).all()
        # create new dict and store all values to dict
        collage_branch_relations = {}
        # iterate over departments and store each id and name in variablles
        for row in collage:
            key = row.collageName
            collage_id = row.id

            # select all branchs that belong to collage/subcity
            collage = collage.query.filter_by(collageID = collage_id).all()

            # build new list structure(branch_lst) that includes the names of the services that belong
            # to the selected department
            branch_lst = []
            for row in collage:
                branch_lst.append(row.branchName)

            # update the dictionary with branch name as a key
            collage_branch_relations[key] = branch_lst
        
        return collage_branch_relations