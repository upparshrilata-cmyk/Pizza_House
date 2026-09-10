# 🍕 Pizza House – AI Restaurant Management Web Application

**Pizza House** is a modern AI-powered web-based restaurant management system developed using **Python and Flask**. It helps restaurants manage customer orders, AI voice ordering, billing, GST calculation, invoices, menu, customers, table bookings, reports, and AI-based business insights from a single web application.

The system provides a simple and user-friendly interface that can be accessed through a web browser.

---

## ✨ Features

### 🎤 AI Voice Ordering

* AI-powered voice-based food ordering
* Natural language order understanding
* Customer name and mobile number handling
* Pizza item, size, quantity and toppings detection
* Automatic order detail extraction
* Speech-to-text conversion
* Text-to-speech interaction
* Faster and easier customer ordering

### 🧾 Billing & GST Management

* Automatic bill calculation
* Automatic GST calculation
* Subtotal and total amount calculation
* Invoice generation
* Invoice storage
* Printable invoices

### 📋 Order Management

* Create new restaurant orders
* View all orders
* Store complete order information
* Track customer orders
* Manage restaurant order records
* Delete orders when required

### 🍕 Menu Management

* View restaurant menu
* Add new food items
* Update food item details
* Delete food items
* Manage food prices
* Manage pizza sizes and menu information

### 👥 Customer Management

* Store customer information
* View customer details
* View customer order history
* Track customer spending
* Manage customer records

### 🪑 Table Booking

* Online table booking through the web application
* Customer name and mobile number collection
* Select booking date and time
* Select number of guests
* Select table number
* View recent table bookings
* Update booking status
* Delete bookings when required

### 📊 Reports & Analytics

* View restaurant sales information
* Order-related reports
* Revenue information
* Sales summaries
* Top-selling pizza information
* Business performance analysis

### 🤖 AI Business Insights

* AI-based restaurant business insights
* Analyze restaurant sales and order information
* Understand business performance
* Generate useful business recommendations
* Support better restaurant decision-making

### 📈 Dashboard

The dashboard provides an overview of restaurant activities, including:

* Total Orders
* Total Sales
* Total Customers
* Recent Orders
* Table Bookings
* Restaurant activities
* Business statistics

### 🔐 Login & User Management

* Secure login system
* Customer login
* Admin login
* Role-based access
* Customer-specific information
* Admin management features

---

## 🛠️ Technologies Used

* **Python** – Backend programming
* **Flask** – Web application framework
* **HTML5** – Web page structure
* **CSS3** – User interface styling
* **JavaScript** – Interactive web functionality
* **SQLite** – Database management
* **OpenAI API** – AI voice ordering and AI insights
* **Speech-to-Text** – Voice input processing
* **Text-to-Speech** – Voice responses
* **ReportLab** – Invoice generation
* **Jinja2** – Flask template rendering
* **python-dotenv** – Environment variable management

---

## 📁 Project Structure

```text
Pizza House/
│
├── app.py
├── database.py
├── pizza_house.db
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   ├── order.html
│   ├── billing.html
│   ├── menu.html
│   ├── customers.html
│   ├── reports.html
│   ├── booking.html
│   ├── booking_success.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── invoices/
```

> **Note:** The `.env` file contains private configuration such as API keys and should not be uploaded to GitHub.

---

# ⚙️ Installation

## 1. Install Python

Download and install Python on your Windows computer.

During installation, make sure to enable:

```text
Add Python to PATH
```

Check whether Python is installed:

```powershell
python --version
```

---

## 2. Download the Project

Clone this repository:

```bash
git clone https://github.com/YOUR-USERNAME/PizzaHouse-AI-Restaurant.git
```

Open the project folder:

```bash
cd "Pizza House"
```

You can also open the downloaded project folder directly in **Visual Studio Code**.

---

## 3. Create a Virtual Environment

Open the VS Code terminal and run:

```powershell
python -m venv venv
```

---

## 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

After successful activation, the terminal will show:

```text
(venv)
```

For example:

```text
(venv) PS C:\Users\YourName\Downloads\Pizza House>
```

---

## 5. Install Required Libraries

Run:

```powershell
pip install -r requirements.txt
```

If required, you can also use:

```powershell
python -m pip install -r requirements.txt
```

---

# 🔑 API Key Setup

The AI features of Pizza House require an **OpenAI API key**.

For security reasons, the API key should **not** be written directly inside the Python source code or uploaded to GitHub.

Create a `.env` file in the main project folder:

```text
Pizza House/
│
├── app.py
├── database.py
├── .env
└── ...
```

Add the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

The application loads these values using environment variables.

### ⚠️ Important Security Rule

**Never upload your `.env` file to GitHub.**

Your `.gitignore` should contain:

```gitignore
.env
venv/
.venv/
__pycache__/
*.pyc
```

---

# ▶️ How to Run the Application

Follow these steps to run Pizza House on your computer.

## 1. Open the Project in VS Code

Open the **Pizza House** project folder in Visual Studio Code.

Make sure the folder contains:

```text
Pizza House/
│
├── app.py
├── database.py
├── pizza_house.db
├── requirements.txt
├── templates/
├── static/
└── ...
```

---

## 2. Open VS Code Terminal

In Visual Studio Code, select:

```text
Terminal → New Terminal
```

Make sure the terminal is opened inside the Pizza House project folder.

Example:

```powershell
PS C:\Users\YourName\Downloads\Pizza House>
```

---

## 3. Activate Virtual Environment

Run:

```powershell
venv\Scripts\Activate.ps1
```

You should see:

```text
(venv)
```

at the beginning of the terminal.

---

## 4. Start the Flask Application

Run:

```powershell
python app.py
```

If the application starts successfully, the terminal will show a local address similar to:

```text
Running on http://127.0.0.1:5000
```

---

## 5. Open the Website

Open Google Chrome, Microsoft Edge, or another web browser.

Enter:

```text
http://127.0.0.1:5000
```

You can also use:

```text
http://localhost:5000
```

The **Pizza House** web application will open in your browser.

---

# 🔐 Login

After opening the website, the Pizza House login page will appear.

Users can log in according to their role.

### 👤 Customer

Customers can access features such as:

* Dashboard
* AI Voice Ordering
* New Order
* Table Booking
* Order information

### 👨‍💼 Admin

Administrators can access:

* Dashboard
* Orders
* Menu Management
* Customer Management
* Table Bookings
* Reports
* AI Business Insights

---

# 🎤 AI Voice Ordering Flow

The AI voice ordering system allows customers to place an order using natural speech.

For example, a customer can say:

```text
I want one large margherita pizza with extra cheese.
```

The AI system processes the voice input and identifies information such as:

```text
Food Item   → Margherita Pizza
Size        → Large
Quantity    → 1
Toppings    → Extra Cheese
```

The extracted information can then be used to create the restaurant order.

---

# 🧾 Billing Flow

```text
Customer Order
      ↓
Food Item + Size + Quantity
      ↓
Calculate Item Price
      ↓
Calculate Subtotal
      ↓
Calculate GST
      ↓
Calculate Total
      ↓
Generate Invoice
```

---

# 🪑 Table Booking Flow

```text
Customer
   ↓
Select Booking Date
   ↓
Select Booking Time
   ↓
Select Number of Guests
   ↓
Select Table
   ↓
Create Booking
   ↓
Booking Confirmation
```

Administrators can view recent bookings and manage their booking status.

---

# 🗄️ Database

Pizza House uses **SQLite** for storing application data.

The database stores information related to:

* Customers
* Orders
* Menu items
* Table bookings
* Billing information
* GST
* Invoice information
* Restaurant records

The main database file is:

```text
pizza_house.db
```

---

# 👨‍💼 Admin Features

The administrator can manage the restaurant through the admin section.

Admin features include:

* View dashboard statistics
* Manage orders
* Manage menu items
* Manage customers
* View customer order history
* Manage table bookings
* Update booking status
* Delete bookings
* View reports
* View sales information
* Generate AI business insights

---

# 👤 Customer Features

Customers can use the web application to:

* Login to the system
* Place food orders
* Use AI voice ordering
* View order information
* Book restaurant tables
* View their restaurant activities

---

# 📊 Reports & Analytics

The reports section helps the restaurant understand its business performance.

It can provide information such as:

* Total sales
* Total orders
* Revenue
* Sales summaries
* Popular pizza items
* Business performance

---

# 🤖 AI Business Insights

The AI Insights feature uses restaurant business information to provide useful analysis.

It can help identify:

* Restaurant performance
* Sales trends
* Order patterns
* Popular products
* Possible business improvements

---

# 🔒 Security

Pizza House follows basic security practices such as:

* Environment variables for API keys
* `.env` excluded from GitHub
* Login authentication
* Role-based access
* Protected admin functionality
* Parameterized SQLite queries

---

# 🛑 How to Stop the Application

To stop the Flask server, go to the VS Code terminal and press:

```text
CTRL + C
```

The web application will stop running.

---

# 🔄 How to Run the Project Again

Whenever you want to run Pizza House again:

### Step 1 – Open the project

Open the Pizza House folder in VS Code.

### Step 2 – Open Terminal

Select:

```text
Terminal → New Terminal
```

### Step 3 – Activate virtual environment

```powershell
venv\Scripts\Activate.ps1
```

### Step 4 – Start the application

```powershell
python app.py
```

### Step 5 – Open the browser

Go to:

```text
http://127.0.0.1:5000
```

---

# 🐛 Troubleshooting

## Python is not recognized

Check Python installation:

```powershell
python --version
```

If Python is not recognized, install Python and make sure **Add Python to PATH** is enabled.

---

## `pip install` error

Try:

```powershell
python -m pip install -r requirements.txt
```

---

## Virtual environment activation error

Try activating the environment using:

```powershell
venv\Scripts\activate
```

If PowerShell blocks script execution, open Command Prompt and run:

```cmd
venv\Scripts\activate
```

---

## Port 5000 is already in use

Stop the previous Flask application using:

```text
CTRL + C
```

Then start the application again:

```powershell
python app.py
```

---

## OpenAI API Error

Check that the `.env` file exists in the project folder and contains:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Make sure the API key is valid and has the required API access.

---

## Website is not opening

Make sure the Flask application is running in the VS Code terminal.

You should see an address similar to:

```text
http://127.0.0.1:5000
```

Then open that address in your browser.

---

# 🌐 Local Application URL

After starting the application, it can be accessed using:

```text
http://127.0.0.1:5000
```

or:

```text
http://localhost:5000
```

---

# 📦 Requirements

All required Python packages are listed in:

```text
requirements.txt
```

Install them using:

```powershell
pip install -r requirements.txt
```

---

# 🚀 Future Enhancements

The following features can be added in future versions:

* Online food delivery integration
* WhatsApp order integration
* Online payment gateway
* AI customer support chatbot
* Advanced sales forecasting
* Real-time order tracking
* Cloud database
* Mobile application
* Multi-restaurant management
* Customer feedback and rating system
* Loyalty and reward system
* Email and SMS notifications
* Improved real-time AI voice conversation

---

# 🎯 Project Objective

The main objective of **Pizza House – AI Restaurant Management Web Application** is to provide a simple, efficient and intelligent restaurant management solution through a web browser.

The system combines traditional restaurant management features with modern **AI and voice technology** to reduce manual work and improve restaurant operations.

It allows restaurant staff to manage:

* Orders
* Customers
* Menu
* Billing
* GST
* Invoices
* Table bookings
* Reports
* Business insights

from a single web application.

---

# 🌟 Project Highlights

```text
🍕 Restaurant Management
🤖 Artificial Intelligence
🎤 AI Voice Ordering
🧾 Billing & GST
📄 Invoice Generation
👥 Customer Management
🍽️ Menu Management
🪑 Table Booking
📊 Reports & Analytics
🔐 Login & Role Management
🗄️ SQLite Database
🌐 Flask Web Application
```

---

# 👩‍💻 Project

## Pizza House – AI Restaurant Management Web Application

A Python and Flask-based web application combining restaurant management, AI voice ordering, billing, GST calculation, invoice generation, customer management, table booking, reports and AI-powered business insights.

---

## 📌 Academic Project

This project is developed as an academic **Field Project** to demonstrate the practical use of **Python, Flask, database management, web technologies and Artificial Intelligence** in a restaurant management system.

The project focuses on reducing manual restaurant operations and providing a simple, intelligent and user-friendly web-based solution.
