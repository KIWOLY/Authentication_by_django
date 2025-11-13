
# Django & Django REST Framework Authentication Project .

This project is a **comprehensive guide to authentication** in Django and Django REST Framework (DRF). It is designed to help you learn, compare, and implement different authentication methods in a single project.



## What You’ll Learn

This project covers:

1. **Session-Based Authentication**

   * The traditional username/password login system.
   * Uses Django sessions and CSRF protection.
   * Best for server-rendered apps and the Django Admin.

2. **Google OAuth 2.0 Authentication**

   * “Sign in with Google” functionality.
   * Integrates with Django using the Google OAuth 2.0 standard.
   * Best for users who prefer using their Google account instead of creating a new password.

3. **DRF Token Authentication**

   * Provides each user with a unique token.
   * Clients use the token in API requests for authentication.
   * Simple and widely used in mobile apps and server-to-server communication.

4. **JWT (JSON Web Token) Authentication**

   * Modern token-based authentication with short-lived access tokens and refresh tokens.
   * Provides better scalability for APIs.
   * Supports token rotation and blacklisting for extra security.



##  Tools & Technologies

* **Django**: For session-based authentication and project management.
* **Django REST Framework (DRF)**: For building APIs.
* **Google OAuth (social-auth-app-django)**: For Google login integration.
* **DRF Token Authentication**: For simple token-based login.
* **SimpleJWT**: For JWT access and refresh tokens.
* **CORS Headers**: To allow frontend apps (React, Flutter, etc.) to connect.



##  Project Overview

The project is organized so you can explore each authentication method separately while using the same user system. It includes:

* A **session-based login and logout** system for web users.
* A **Google OAuth login flow** that redirects users to Google, then back to the app.
* **API endpoints for token authentication** where users request a token and then access secure endpoints.
* **API endpoints for JWT authentication** where users log in and get access/refresh tokens.



##  Authentication Methods Explained

### 1) Session-Based Authentication

* Works by storing a session ID in a cookie.
* Users log in with username and password.
* Django tracks their session automatically.
* Protected against CSRF attacks.
* Good for traditional web applications.

### 2) Google OAuth 2.0

* Users click "Login with Google".
* They are redirected to Google to grant permission.
* Once approved, they are redirected back and logged in.
* Convenient for users since they don’t need a new password.

### 3) DRF Token Authentication

* Each user has a token generated after login.
* Clients send this token in every request header.
* Simple and widely used in small-scale apps.
* Tokens remain valid until revoked manually.

### 4) JWT Authentication

* Users log in and receive an **access token** and a **refresh token**.
* Access token: short-lived, used for most requests.
* Refresh token: longer-lived, used to get new access tokens.
* Supports **blacklisting** and **token rotation** for better security.
* Best for modern APIs and mobile applications.



##  Security Practices

* Always use **HTTPS** in production.
* Enable **CSRF protection** when using session-based authentication.
* Restrict **CORS origins** to only trusted frontends.
* Keep secret keys, OAuth credentials, and tokens in a **.env file**.
* Consider adding **rate limiting or login attempt limits** to prevent brute-force attacks.



##  Use Cases

* **Session Authentication** → Ideal for Django Admin or websites where users log in via browser.
* **Google OAuth** → Perfect for fast onboarding using existing Google accounts.
* **Token Authentication** → Useful for small-scale APIs or mobile apps where token management is simple.
* **JWT Authentication** → Best for scalable APIs, mobile apps, and systems requiring refresh token flows.



##  Learning Outcomes

By completing this project, you will:

* Understand the differences between session, token, and JWT authentication.
* Be able to integrate third-party login using Google OAuth.
* Learn how to secure APIs with different authentication methods.
* Gain hands-on experience setting up authentication workflows in Django and DRF.



##  Next Steps

* Add **registration and password reset flows**.
* Integrate **role-based access control** (e.g., admin vs user permissions).
* Connect with a frontend (React, Vue, Flutter) to practice cross-origin authentication.
* Deploy the project to production with proper security settings.



## 📜 License

This project is free to use for learning .

