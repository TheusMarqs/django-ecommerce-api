# 🛍️ E-Commerce API (Django)

## 📖 Description
This is the back-end for an e-commerce platform built with Django and Django Rest Framework. The API handles user authentication, product management, shopping cart, order management, and provides a real-time chat feature using WebSockets and Redis. The data is stored in a PostgreSQL database, and the application uses JWT tokens for secure user authentication.

## 🚀 Features
- **🔒 JWT Authentication**: Secure login and registration with JWT and refresh tokens.
- **📦 Product Management**: CRUD operations for products, categories, and suppliers.
- **🛒 Shopping Cart**: Add/remove items, view the cart, and proceed to checkout.
- **🧾 Order Management**: Manage customer orders and update their status.
- **💬 Real-Time Chat**: Chat functionality for customers and support agents using WebSockets and Redis.
- **📷 QR & Barcode**: APIs for retrieving product information via QR code or barcode.

## 🛠️ Tech Stack
- **Django**: Python-based web framework for rapid development.
- **Django Rest Framework (DRF)**: Toolkit for building Web APIs.
- **PostgreSQL**: Database for storing product, order, and user information.
- **Redis**: Message broker for WebSockets, used for real-time chat.
- **WebSockets**: For real-time communication between clients and support agents.
- **JWT**: For token-based user authentication.

## 🌟 Future Enhancements
Implement payment gateway integration for order payments.

## 🚀 Deployment
The backend is deployed on **Render**, a platform for hosting web applications. The API is publicly accessible via the Render domain.


