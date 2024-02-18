# 🚀 Django API - Customers && Orders 📦

Welcome to the Customer Order Management System API! This API allows you to manage customers, products, shopping carts, and orders efficiently.

## 🔧 Setup Instructions
1. Clone the repository:
    ```
    git clone https://github.com/Aduda-Shem/Django-API.git
    ```
2. Navigate to the project directory:
    ```
    cd Django-API
    ```

3. Create a `.env` file in the root directory with the content from `.env.example`.

4. Build and start the Docker containers:
    ```
    docker compose up --build
    ```

5. The server will start running at `http://localhost:8000`.
6. ## 🧪 Testing
The test files are located under the `tests` directory with different files:
- `test_models.py`
- `test_serializers.py`
- `test_views.py`
  
To run the tests
  ```
   python manage.py test
  ```

## 📋 API Endpoints
- .

## 💡 Additional Information
- Ensure Docker and Docker Compose are installed on your system.
- Authentication is required for endpoints that modify / retrieve data. Use Token Authentication to authenticate requests.
