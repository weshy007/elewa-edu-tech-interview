# Staff Management System

## Introduction
This is a web-based application designed to streamline task management and organization within a company. The application has different user roles, including system administrators, managers, and employees, each with distinct functionalities and permissions.


## Features
- System Administrator: The system administrator has the highest level of access within the application.
    - Assign users the manager role after logging in.

- Manager Role: Managers can create different departments or groups and assign employees (users) to these groups.

    - Task Management:
        - Create Tasks: Managers can create new tasks for employees.
        - Edit Tasks: Managers can edit existing tasks to update details or change assignments.
        - Delete Tasks: Managers can delete tasks that are no longer needed.

    - Employee Management:
        - Move Employees: Managers can move employees from one department to another as needed.
        - Remove Employees: Managers can remove an employee from the organization entirely.

- Employee Role.
    - Task Viewing: Employees can sign in and view their assigned tasks.
    - Task Status Management:
    - Mark as Done: Employees can mark tasks as completed, removing them from the task board.
    - Mark as In Progress: Employees can update tasks to reflect that they are currently being worked on.


## Installation
1. Clone the repository: `git clone https://github.com/weshy007/elewa-edu-tech-interview.git`

2. Install dependencies:
    - Create an environment with `pipenv shell` then install depandancies with `pipenv sync`.
3. Configure settings:
    - Rename `example.env` to `.env` and update the configuration variables accordingly.

## Usage
1. Run migrations: `make migrate`. 
2. Create a superuser for accessing the admin panel: `python manage.py createsuperuser`
3. Start the development server: `make serve`
4. Access the application in your web browser at `http://localhost:8000`.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Create a new pull request.

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or suggestions, please contact [Waithaka Waweru](https://twitter.com/ItsWeshy) on X.

