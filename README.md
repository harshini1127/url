# URL Shortener Web Application  
A simple and efficient URL shortening web application built using **Flask**, **SQLite**, and **SQLAlchemy**.  
This project allows users to shorten long URLs, create custom aliases, track clicks, view analytics, and manage their own shortened links through login and registration.

---

## 🚀 Features

### 🔑 User Authentication
- User registration with secure password hashing  
- Login with session-based authentication  
- Logout functionality  

### 🔗 URL Shortening
- Shorten long URLs instantly  
- Option to set a **custom alias**  
- Automatically generates unique short IDs using `nanoid`  
- Redirects users to the original URL  
- Tracks number of visits (click count)  

### 📊 Analytics API
Each shortened URL provides detailed analytics:
- Original URL  
- Short ID  
- Click count  
- Created time  
- Last accessed time  

### 🗄️ Database
- Uses **SQLite** for local storage  
- Uses **SQLAlchemy ORM** for modeling and managing data  

---

## 📁 Project Structure

url_shortener/
│
├── app.py # Main Flask app
├── db.py # SQLAlchemy database instance
├── models.py # User & URL models
├── shortener.py # Random short ID generator
├── requirements.txt # Python dependencies
│
├── templates/
│ ├── index.html # URL shortener homepage
│ ├── login.html # Login page
│ └── register.html # Registration page
│
└── static/
└── style.css # (Optional) CSS styling

---

## 🛠️ Installation & Setup (Step-by-Step)

### 1. Clone the Repository
```bash
git clone https://github.com/harshini1127/url_shortener.git
cd url_shortener
✨ Technologies Used
Technology    	Purpose
Python	        Backend logic
Flask	           Web framework
SQLAlchemy	      ORM for database
SQLite	         Local database
Bootstrap 5	     UI styling
Jinja2	         Template rendering
nanoid	          Short ID generator

🎯 Future Enhancements
Forgot Password functionality
User dashboard to view all URLs
Dark mode UI
QR Code generator for each short link
Admin panel

👩‍💻 Author
Harshini
GitHub: harshini1127

