Here’s the updated **README.md** file along with the test automation scripts for setting up the project in both development and production environments.

---

# **Django REST Authentication and Product API with JWT, Docker, and Swagger**

This project is a Django REST API built using Django Rest Framework (DRF) and Simple JWT for token-based authentication. The API includes features for user registration, login, password management, and product selection. It leverages Docker for containerization and PostgreSQL as the database. Swagger and ReDoc are used for auto-generated API documentation.

## **Features**

- **Authentication**: Custom user registration and JWT-based login.
- **Password management**: Password reset via email and change password functionality.
- **Product management**: APIs for product listing, selection, and reporting.
- **Session Persistence**: Search results and product selections are saved even after re-opening the browser.
- **API Documentation**: Auto-generated API documentation with Swagger and ReDoc using `drf-yasg`.
- **API Testing**: Postman collection provided for API testing.
- **Dockerized**: Runs in a Docker environment for easy deployment and scaling.

---

## **Technologies Used**

- **Backend**: Django, Django Rest Framework (DRF)
- **Authentication**: Simple JWT (JSON Web Token)
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose
- **API Documentation**: Swagger and ReDoc using `drf-yasg`
- **API Testing**: Postman

---

## **Getting Started**

### **Clone the Repository**

First, clone the repository to your local machine:

```bash
git clone https://github.com/mhsnrafi/auth-product-api-django.git
cd auth-product-api-django
```

### **Docker Setup**

Ensure you have Docker installed. Run the following command to build and start the containers:

```bash
docker-compose up --build
```

This command will:

1. Build the Docker containers for Django and PostgreSQL.
2. Run the database migrations.
3. Set up the environment for the API to run.

### **Environment Variables**

Ensure to set up environment variables using a `.env` file at the root of your project.

Example `.env` file:

```env
# General
DEBUG=1
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost 127.0.0.1

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Email (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=test@example.com
EMAIL_HOST_PASSWORD=test_password
```

---

## **Running the Project Using Docker**

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mhsnrafi/auth-product-api-django.git
   cd auth-product-api-django
   ```

2. **Create a `.env` file**:

   Create a `.env` file in the root directory and configure the necessary environment variables like the `SECRET_KEY`, `DB_USER`, `DB_PASSWORD`, and others.

3. **Build and run the Docker container**:

   Use Docker to build and run the app:

   ```bash
   docker-compose up --build
   ```

4. **Run Migrations**:

   After the containers are up, you need to run database migrations to set up the tables in the PostgreSQL database. Use the following command to run migrations:

   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a superuser (optional)**:

   To create a Django superuser for the admin panel, run:

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

   Follow the prompts to create an admin user.

6. **Access the app**:

   Once Docker has finished building and running your app, you can access it at `http://localhost:8000`.

---

## **Running Tests**

You can run the tests using Docker by executing the following command:

```bash
docker-compose exec web python manage.py test
```

This will run all your Django unit tests inside the Docker container.

---

## **Setting Up Swagger and ReDoc API Documentation**

This project uses `drf-yasg` to generate Swagger and ReDoc API documentation automatically. You can access both documentation formats by following these steps:

### **Install `drf-yasg`**

Ensure `drf-yasg` is installed by adding it to your `requirements.txt` or running:

```bash
pip install drf-yasg
```

### **Configuring Swagger and ReDoc**

**Access Swagger and ReDoc**:

   After running the project, you can view the API documentation at the following URLs:
   - Swagger UI: `http://localhost:8000/swagger/`
   - ReDoc: `http://localhost:8000/redoc/`

---

## **Postman Collection**

A Postman collection is provided for easy API testing. You can find the Postman collection in the `API.postman_collection.json` file in the root of the project.

- Import the collection into Postman to test all the endpoints.

---

## **API Reference**

### **Authentication & User Management**

| URL | Method    | Description                |
| :-------- | :------- | :------------------------- |
| `/api/user/register/` | `POST` | **Register a new user** 
| `/api/user/login/`      | `POST` | **Login user and receive JWT token** |
| `/api/user/profile/`      | `GET` | **Get profile of the authenticated user** |
| `/api/user/changepassword/`      | `POST` | **Change the password for the authenticated user** |
| `/api/user/send-reset-password-email/`      | `POST` | **Send password reset email to the user** |
| `/api/user/reset-password/<uidb64>/<token>/`      | `POST` | **Reset the user's password using a unique token** |

### **Product Management API**

| URL | Method    | Description                |
| :-------- | :------- | :------------------------- |
| `/api/products/` | `GET` | **List all products** 
| `/api/products/search/`      | `GET` | **Search products by query and sort by name, price, or stock** |
| `/api/products/select/<id>/` | `POST` | **Mark a product as selected by the user** |
| `/api/products/report/<id>/` | `POST` | **Report a product by ID** |

---

## **How to Use JWT Authentication**

To access the protected routes (like `/api/user/profile/` or `/api/user/changepassword/`), you need to authenticate using JWT.

1. **Login** using `/api/user/login/` endpoint with your credentials (email and password).
2. You will receive a token in the response.
3. Use the token in the `Authorization` header in the format `Bearer <token>` for further requests.

Example of `Authorization` header:

```
Authorization: Bearer <your_jwt_token>
```

---

## **Automation Scripts**

You can use the following bash scripts to automate your project setup in both **development** and **production** environments.

### **Development Setup Script**

Here is how to include the information about running the development and production scripts in your **README.md** file.

---

## **Running the Setup Scripts**

### **Development Setup**

For automating the development setup, you can use the provided `dev_setup.sh` script. Follow these steps to run it:

1. **Give execute permission** to the script (only needed the first time):
   ```bash
   chmod +x dev_setup.sh
   ```

2. **Run the development setup script**:
   ```bash
   ./dev_setup.sh
   ```

This script will:

- Pull the latest changes from the GitHub repository.
- Build the Docker containers.
- Run database migrations.
- Optionally create a superuser.
- Install any new Python dependencies.
- Start the Django development server.

---

### **Production Setup**

For automating the production setup, use the `prod_setup.sh` script. Follow these steps to run it:

1. **Give execute permission** to the script (only needed the first time):
   ```bash
   chmod +x prod_setup.sh
   ```

2. **Run the production setup script**:
   ```bash
   ./prod_setup.sh
   ```

This script will:

- Pull the latest changes from the GitHub repository.
- Build the Docker containers for production.
- Run database migrations without user interaction.
- Collect static files for production.
- Start the production server using **Gunicorn** with multiple worker processes.

---

By using these scripts, the setup process for both development and production environments is automated, ensuring consistency and reducing manual errors.ontains instructions for setting up both development and production environments, including running tests and accessing the API documentation via Swagger and ReDoc.
<img width="1728" alt="Screenshot 2024-10-14 at 01 31 21" src="https://github.com/user-attachments/assets/d4ed0b00-380b-4bfd-be05-af8091ff3ad1">
<img width="960" alt="Screenshot 2024-10-14 at 01 31 12" src="https://github.com/user-attachments/assets/41ccd078-9e68-4cf0-b9f3-3412c529006f">
<img width="1282" alt="Screenshot 2024-10-14 at 01 31 07" src="https://github.com/user-attachments/assets/17086a6d-6af8-4473-b9f5-058e75502a73">
<img width="1728" alt="Screenshot 2024-10-14 at 01 30 53" src="https://github.com/user-attachments/assets/8602046e-aa6a-43bf-825f-9585d9a67ab9">
<img width="1727" alt="Screenshot 2024-10-14 at 01 30 31" src="https://github.com/user-attachments/assets/03c1909c-842d-4170-b16e-8662c7d34905">




