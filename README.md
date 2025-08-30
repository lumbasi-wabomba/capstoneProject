

# UniCollab: Your Collaborative Workspace


Welcome to **UniCollab**, a powerful and flexible platform designed to streamline collaboration for teams and individuals. Whether you're managing projects, tracking tasks, sharing resources, or communicating with your team, UniCollab provides the tools you need in a secure and organized environment.

This repository contains the backend API for UniCollab, built with Django and Django REST Framework.

## Table of Contents

1.  [What is UniCollab?](#what-is-unicollab)
2.  [Key Features](#key-features)
3.  [Technologies Under the Hood](#technologies-under-the-hood)
4.  [Getting Started (For Developers)](#getting-started-for-developers)
    *   [Prerequisites](#prerequisites)
    *   [Installation Steps](#installation-steps)
    *   [Database Setup](#database-setup)
    *   [Running the Server](#running-the-server)
5.  [API Usage (For Developers & Integrators)](#api-usage-for-developers--integrators)
    *   [Authentication](#authentication)
    *   [Core API Endpoints](#core-api-endpoints)
    *   [Understanding the Code Flow](#understanding-the-code-flow)
6.  [Project Structure](#project-structure)
7.  [Contributing](#contributing)
8.  [License](#license)

---

## 1. What is UniCollab?

UniCollab is a backend API that powers a collaborative application. It provides a robust set of functionalities to manage various aspects of teamwork:

*   **User Accounts:** Securely manage user registration, login, and profiles.
*   **Project Management:** Create, organize, and oversee multiple projects.
*   **Task Tracking:** Assign, prioritize, and monitor tasks within projects.
*   **Resource Sharing:** Centralize and share files and documents relevant to your projects.
*   **Real-time Communication:** Facilitate messaging within project contexts.
*   **Notifications:** Keep users informed about important updates and activities.
*   **Scheduling:** Plan and manage events and deadlines for individuals and teams.

This API is designed to be consumed by various frontend applications (web, mobile, desktop) to provide a seamless user experience.

## 2. Key Features

UniCollab offers a comprehensive suite of features to enhance collaboration:

### **User & Access Management**
*   **Secure User Accounts:** Users can easily **register** with a username, email, and password.
*   **Flexible Login:** Log in using either your username or email.
*   **Token-Based Security:** All authenticated interactions use secure **API tokens**, ensuring your data is protected.
*   **Personal Profiles:** Each user has a profile showing their projects, tasks, notifications, schedules, and uploaded files.

### **Project Organization**
*   **Create & Manage Projects:** Easily set up new projects with a title and description.
*   **Team Collaboration:** Add multiple **members** to a project, fostering teamwork.
*   **Visibility Control:** Mark projects as **public** (visible to all) or **private** (visible only to members).
*   **Creator Ownership:** The project creator is automatically added as a member and has administrative control.

### **Task & Workflow Management**
*   **Detailed Task Creation:** Define tasks with titles, descriptions, and assign them to specific users.
*   **Priority Levels:** Categorize tasks by **Low, Medium, or High priority** to focus on what matters most.
*   **Status Tracking:** Monitor task progress with clear statuses: **To Do, In Progress, and Done**.
*   **Due Dates:** Set **due dates** to ensure timely completion (the system prevents setting dates in the past!).
*   **Filtering:** Quickly find tasks by their status or priority.

### **Resource Sharing**
*   **Centralized Files:** Upload and link resources (like documents or external links) directly to projects.
*   **Easy Access:** Resources are easily accessible to project members.
*   **Public/Private Resources:** Control who sees your resources by marking them public or private.

### **Communication & Notifications**
*   **Project Messaging:** Send and receive messages directly within any project you're a member of.
*   **Automated Notifications:** Get alerts for important events, categorized as:
    *   **Reminders:** For upcoming deadlines or events.
    *   **Updates:** For changes in projects or tasks.
    *   **Mentions:** When someone refers to you.
    *   **Messages:** For new chat messages.
*   **Read Status:** Keep track of which notifications you've already seen.

### **Scheduling & Events**
*   **Event Planning:** Create and manage events with specific start and end times.
*   **Team Events:** Designate events as "team events" for broader project visibility.
*   **Smart Scheduling:** The system validates event times to prevent illogical entries (e.g., end time before start time).

## 3. Technologies Under the Hood

UniCollab is built using robust and widely-used technologies:

*   **Backend Framework:**
    *   **Python 3:** The core programming language.
    *   **Django (5.2.5):** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
    *   **Django REST Framework (3.16.1):** A powerful toolkit for building Web APIs in Django, providing serialization, authentication, and viewset functionalities.
*   **Database:**
    *   **MySQL:** The primary relational database used for production environments, ensuring data integrity and scalability.
    *   **SQLite:** Used for development and testing, offering a lightweight, file-based database solution.
*   **Other Key Libraries:**
    *   `django-filter`: Simplifies filtering data in API views.
    *   `asgiref`: ASGI support for Django.
    *   `sqlparse`: A non-validating SQL parser.

## 4. Getting Started (For Developers)

Follow these steps to set up UniCollab on your local machine for development or testing.

### Prerequisites

Make sure you have the following installed on your system:

*   **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
*   **pip**: Python's package installer (usually comes with Python).
*   **MySQL Server**: If you plan to use MySQL as your database. Instructions vary by OS.

### Installation Steps

1.  **Clone the Repository:**
    Open your terminal or command prompt and run:
    ```bash
    git clone https://github.com/your-username/unicollab.git # Replace with actual repo URL
    cd unicollab
    ```

2.  **Create a Virtual Environment (Highly Recommended):**
    A virtual environment isolates your project's dependencies from other Python projects.
    ```bash
    python -m venv venv
    ```
    **Activate the virtual environment:**
    *   **macOS/Linux:** `source venv/bin/activate`
    *   **Windows:** `venv\Scripts\activate`

3.  **Install Dependencies:**
    With your virtual environment active, install all required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

UniCollab is configured to use MySQL by default.

1.  **Create a MySQL Database and User:**
    Log in to your MySQL server and create a database and a user for UniCollab.
    ```sql
    CREATE DATABASE unicollab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER 'unicollab'@'localhost' IDENTIFIED BY '#Kenya@2025'; 
    GRANT ALL PRIVILEGES ON unicollab.* TO 'unicollab'@'localhost';
    FLUSH PRIVILEGES;
    ```
    **Security Note:** The password `#Kenya@2025` is a placeholder from the `settings.py`. **You MUST change this to a strong, unique password** for any production deployment.

2.  **Apply Database Migrations:**
    These commands create the necessary tables in your database based on the models defined in the project.
    ```bash
    python manage.py makemigrations unicollab
    python manage.py migrate
    ```

3.  **Create an Admin User:**
    This user will have access to the Django admin panel (`/admin/`) where you can manage data directly.
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your admin username, email, and password.

### Running the Server

Start the Django development server:
```bash
python manage.py runserver
```
The API will now be accessible at `http://127.0.0.1:8000/`. You can test it using tools like Postman, Insomnia, or directly from your browser for GET requests.

## 5. API Usage (For Developers & Integrators)

This section provides an overview of how to interact with the UniCollab API.

### Authentication

All sensitive API endpoints require **Token Authentication**.

1.  **Register:**
    *   **Endpoint:** `POST /register/`
    *   **Body (JSON):**
        ```json
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "strongpassword123",
            "password2": "strongpassword123"
        }
        ```
    *   **Response:** Returns user details and your `token`.

2.  **Login:**
    *   **Endpoint:** `POST /login/`
    *   **Body (JSON):**
        ```json
        {
            "username": "newuser", 
            "password": "strongpassword123"
        }
        ```
    *   **Response:** Returns your `token`.

3.  **Using the Token:**
    For all subsequent authenticated requests, include the token in the `Authorization` header:
    `Authorization: Token <YOUR_GENERATED_TOKEN_HERE>`

4.  **Logout:**
    *   **Endpoint:** `POST /logout/`
    *   **Headers:** `Authorization: Token <YOUR_CURRENT_TOKEN>`
    *   **Effect:** Invalidates your current token.

### Core API Endpoints

UniCollab uses Django REST Framework's `DefaultRouter` to provide standard RESTful endpoints.

*   **Users:** `/users/`
    *   `GET /users/`: List all users (admin) or your own profile (authenticated user).
    *   `GET /users/me/`: Get details of the currently authenticated user.
*   **Projects:** `/projects/`
    *   `GET /projects/`: List projects you are a member of or created.
    *   `POST /projects/`: Create a new project.
    *   `GET /projects/{id}/members/`: Get all members of a specific project.
*   **Tasks:** `/tasks/`
    *   `GET /tasks/`: List tasks assigned to you or public tasks.
    *   `POST /tasks/`: Create a new task.
    *   `POST /tasks/{id}/assign/`: Assign an existing task to a user.
    *   **Filtering:** Add `?status=to_do` or `?priority=high` to filter tasks.
*   **Schedules:** `/schedules/`
    *   `GET /schedules/`: List schedules you created.
    *   `POST /schedules/`: Create a new schedule/event.
*   **Resources:** `/resources/`
    *   `GET /resources/`: List public resources or resources you uploaded.
    *   `POST /resources/`: Upload a new resource.
*   **Notifications:** `/notifications/`
    *   `GET /notifications/`: List your notifications.
    *   **Filtering:** Add `?type=reminder` to filter notifications by type.
*   **Messages:** `/messages/`
    *   `GET /messages/`: List messages from projects you're in, or messages you sent.
    *   `POST /messages/`: Send a new message within a project.

### Understanding the Code Flow (For Deeper Dive)

The UniCollab API follows a standard Django REST Framework (DRF) pattern, which is based on the Model-View-Controller (MVC) architectural pattern (though Django often refers to it as MVT - Model-View-Template, for APIs it's closer to MVC).

1.  **Models (`unicollab/models.py`): The Data Blueprint**
    *   This is where the **structure of your data** is defined. Each class here (e.g., `User`, `Project`, `Task`) corresponds to a table in your database.
    *   They define fields (like `title`, `description`, `due_date`) and relationships between different pieces of data (e.g., a `Task` belongs to a `Project`, a `Project` has many `members`).
    *   **Example:** The `Task` model defines its `priority` and `status` using predefined choices, ensuring data consistency.

2.  **Serializers (`unicollab/serializers.py`): Data Translators**
    *   Serializers act as **translators** between complex Django model objects and simple data formats like JSON (which APIs use).
    *   They convert data from your database into a format that can be sent over the internet, and vice-versa.
    *   They also perform **data validation**. For instance, the `TaskSerializer` checks if a `due_date` is in the past, and the `MessageSerializer` ensures you're a member of a project before sending a message.
    *   **Example:** `UserSerializer` not only translates user details but also includes nested data for related projects, tasks, and notifications, providing a rich user profile.

3.  **Views (`unicollab/views.py`): The Request Handlers**
    *   Views are the **entry points for API requests**. They receive HTTP requests (GET, POST, PUT, DELETE).
    *   They decide what to do with the request:
        *   **Authentication:** Verify the user's identity using their API token.
        *   **Permissions:** Check if the authenticated user has the right to perform the requested action (e.g., only project members can send messages).
        *   **Logic:** Interact with models (to fetch or save data) and serializers (to validate and format data).
        *   **Response:** Send back an appropriate HTTP response (e.g., 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized).
    *   **`ModelViewSet`**: DRF provides powerful `ModelViewSet`s that automatically handle common operations (create, retrieve, update, delete) for a model, reducing boilerplate code.
    *   **`@action`**: Custom actions (like assigning a task) are defined using the `@action` decorator.
    *   **Example:** When you `POST` to `/projects/`, the `ProjectViewSet` handles it. It uses the `ProjectSerializer` to validate your data, then saves the new project to the database, automatically setting you as the creator and a member.

4.  **URLs (`config/urls.py` & `unicollab/urls.py`): The Address Book**
    *   These files define the **API's address book**. They map specific web addresses (URLs) to the corresponding views that should handle requests to those addresses.
    *   `DefaultRouter` in `unicollab/urls.py` automatically creates a set of URLs for each `ModelViewSet` (e.g., `/users/`, `/users/{id}/`, `/projects/`, etc.), making it easy to expose your API.
    *   **Example:** A request to `GET /tasks/?status=done` is routed to the `TaskViewSet`, which then uses its `get_queryset` method and `DjangoFilterBackend` to return only tasks marked as 'done'.

This structured approach ensures that the code is modular, maintainable, and scalable, making it easier for developers to understand, extend, and debug the application.

## 6. Project Structure

```
.
├── config/                     # Main Django project configuration
│   ├── asgi.py                 # ASGI configuration for async apps
│   ├── __init__.py             # Python package marker
│   ├── settings.py             # **Crucial: All Django settings (database, installed apps, security)**
│   ├── urls.py                 # Main URL dispatcher for the entire project
│   └── wsgi.py                 # WSGI configuration for web servers
├── unicollab/                  # The core application for collaboration features
│   ├── admin.py                # Registers models for the Django admin interface
│   ├── apps.py                 # App configuration (e.g., app name)
│   ├── __init__.py             # Python package marker
│   ├── migrations/             # Database schema changes (auto-generated)
│   │   └── 0001_initial.py     # Initial database setup
│   ├── models.py               # **Defines all database tables (User, Project, Task, etc.)**
│   ├── serializers.py          # **Handles data conversion and validation for API requests**
│   ├── tests.py                # Placeholder for unit and integration tests
│   ├── urls.py                 # **Defines API endpoints specific to the unicollab app**
│   └── views.py                # **Contains the logic for handling API requests and responses**
├── manage.py                   # Django's command-line utility for administrative tasks
├── requirements.txt            # Lists all Python dependencies for the project
├── README.md                   # This file!
└── .gitignore                  # Specifies files/folders to be ignored by Git
```

## 7. Contributing

We welcome contributions to UniCollab! If you'd like to help improve this project, please follow these guidelines:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix:
    `git checkout -b feature/your-awesome-feature`
    or
    `git checkout -b bugfix/fix-issue-123`
3.  **Make your changes.** Ensure your code adheres to the project's style.
4.  **Write clear commit messages:**
    `git commit -m "feat: Add new task filtering by due date"`
5.  **Push your branch** to your forked repository:
    `git push origin feature/your-awesome-feature`
6.  **Open a Pull Request** to the `main` branch of the original repository. Describe your changes clearly.

