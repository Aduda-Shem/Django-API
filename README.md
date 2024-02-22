# 🚀 Django API - E-Commerce 📦

Customer Order Management System API! This API allows you to manage customers, products, and orders efficiently with authentication and authorization using OpenID Client(specifically the oauth2_provider).

## 🔧 Setup Instructions
1. Clone the repository:
    ```
    git clone https://github.com/Aduda-Shem/Django-API.git
    ```
2. Navigate to the project directory:
        ```
        cd Django-API
        ```

3. Create a `.env` file in the root directory with the content from `.env.example` as env sample.
        ```
        touch .env
        ```

4. The docker is run using docker containers, To Build and start the Docker containers:
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
   - `http://localhost:8000/customers`
   - `http://localhost:8000/products`
   - `http://localhost:8000/products`

## 💡 Additional Information
- Ensure Docker and Docker Compose are installed on your system.
- Authentication is required for endpoints that modify / retrieve data. Use Token Authentication to authenticate requests, To obtain TOkens follow the steps below:

------------------------------------------
# 🔒 Authentication and Authorization

To set up authentication and authorization using OpenID Connect:

## Getting Started

Build an OAuth2 provider using Django, Django OAuth Toolkit, and OAuthLib.

OAuth is an open standard for access delegation, commonly used to grant websites or applications access to user information on other websites without requiring passwords.

## Step-by-Step Guide

1. **Install Django OAuth Toolkit:**
    ```
    pip install django-oauth-toolkit
    ```

2. **Configure Django OAuth Toolkit:**
    Add `oauth2_provider` to `INSTALLED_APPS` and run migrations.
    ```
    python manage.py migrate oauth2_provider
    ```

3. **Include OAuth URLs:**
    Include `oauth2_provider.urls` in `urls.py`.

    either:
    ```
        from django.urls import include, path

        urlpatterns = [
            ...
            path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
        ]
    ```
    OR using re_path():
    ```
        from django.urls import include, re_path

        urlpatterns = [
            ...

            re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
        ]
    ```
 
4. **Set LOGIN_URL in settings.py:**
    Set `LOGIN_URL='/admin/login/'` in `settings.py`.

5. **Create a SuperUser:**
    ```
    python manage.py createsuperuser
    ```
    Login into the admin then browse to `http://127.0.0.1:8000/o/applications/register/` to register a new application

    Before saving, copy the `client id` and `client secret` , set the Redirect url as `http://127.0.0.1:8000/o/callback`
    

6. **Authorization Code Flow:**
    - Register an application.
        ![Alt text](READMEscreenshots/registerapp.png)
    
    - generate an authentication code grant with PKCE (Proof Key for Code Exchange), useful to prevent authorization code injection.
    We do this by generating a `code_verifier` random string between 43 and 128 characters, encided to produce a `code_challenge`, sample script:
    ```
    import random
    import string
    import base64
    import hashlib

    code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
    code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))
    print("code_verifier: ", code_verifier)

    code_challenge = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
    print("code_challenge: ", code_challenge)

    ```
    - After generating, start the Authorization code flow by using 
    ```
    http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge=[YOUR_CODE_CHALLENGE]=S256&client_id=[YOUR_CLIENT_ID]&redirect_uri=[YOUR_REDIRECT_URI]&scope=openid

    ```
    - Authorize the web app.
        ![Alt text](READMEscreenshots/authorize.png)
        
    - Obtain an access token.
    ```
        http://127.0.0.1:8000/o/authorize/?response_type=code&code_challenge=x00bLi98SBgwXewDAZ6OsVxVpTqaphvbTVG7vVrRNr4&code_challenge_method=S256&client_id=hUn9pxrpL0MinLPTyCcTv7zzbgCaXDrsAW84dweS&redirect_uri=http://localhost:8000/o/callbak&scope=openid

    ```
    - The above will redirect and generate a code
    `http://127.0.0.1:8000/o/callbak?code=lux5uTBJIbsOPbMuvDcI5TVtUGsxA6`
    ![Alt text](REAeDMEscreenshots/authcode.png)

    - Now We will head over to postman to generate the toke we will use to authenticate our views
    ![Alt text](READMEscreenshots/generate_access_token.png)
