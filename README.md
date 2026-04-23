# ShopDeals — Affiliate Marketing Website

A full-stack affiliate marketing platform built with **Python Flask**, **SQLite**, and **Bootstrap 5**.
Features a dark luxury UI with session-based admin authentication and full product CRUD.

---

## 🗂 Project Structure

```
affiliate_site/
├── app.py                   # Flask app, routes, models
├── requirements.txt
├── static/
│   ├── css/style.css        # Custom dark theme
│   └── js/main.js           # Animations & interactivity
└── templates/
    ├── base.html            # Layout (navbar, footer, flashes)
    ├── index.html           # Homepage — product grid + pagination
    ├── product.html         # Product detail page
    ├── login.html           # Admin login
    ├── dashboard.html       # Admin product table
    └── product_form.html    # Add / Edit product form
```

---

## ✅ Prerequisites

1. **Install Python 3.10+** from https://www.python.org/downloads/
   - During install, tick **"Add Python to PATH"** ✔
2. Open **Command Prompt** (`Win + R` → type `cmd` → Enter)
   or use **PowerShell** / **Windows Terminal**

---

## ⚡ Quick Start (Windows)

### Step 1 — Extract the project

Unzip or copy the `affiliate_site` folder somewhere convenient, e.g. `C:\Projects\affiliate_site\`

### Step 2 — Open a terminal in the project folder

In File Explorer, navigate into `affiliate_site`, click the address bar, type `cmd`, press **Enter**. Or:

```cmd
cd C:\Projects\affiliate_site
```

### Step 3 — Create a virtual environment

```cmd
python -m venv venv
```

### Step 4 — Activate the virtual environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your prompt.

> **PowerShell users:** If you get a script execution error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Then activate with: `.\venv\Scripts\Activate.ps1`

### Step 5 — Install dependencies

```cmd
pip install -r requirements.txt
```

### Step 6 — Run the app

```cmd
python app.py
```

Open your browser at **http://127.0.0.1:5000**

> On first run the database (`affiliate.db`) is created automatically
> and a default admin account is seeded.

---

## 🔁 Starting the app again later

Every time you want to run the project:

```cmd
venv\Scripts\activate
python app.py
```

---

## 🔐 Default Admin Credentials

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

**Change the password immediately in production!**

Admin panel: http://127.0.0.1:5000/admin/login

---

## 🌐 Pages

| URL                          | Description              |
|------------------------------|--------------------------|
| `/`                          | Homepage (product grid)  |
| `/product/<id>`              | Product detail + buy now |
| `/admin/login`               | Admin login              |
| `/admin/dashboard`           | Product management table |
| `/admin/product/add`         | Add new product          |
| `/admin/product/edit/<id>`   | Edit product             |
| `/admin/product/delete/<id>` | Delete product (POST)    |
| `/admin/logout`              | Logout                   |

---

## 🛡 Security Features

- Passwords hashed with `werkzeug.security` (PBKDF2-SHA256)
- All admin routes protected by `@login_required` decorator
- Session-based authentication
- CSRF-safe delete via POST form with confirmation dialog

---

## 🎨 UI Highlights

- Dark luxury theme with noise texture overlay
- Animated floating orbs on hero section
- Card hover lift with image zoom and overlay
- Staggered intersection-observer card entrance
- Responsive grid: 1 → 2 → 3 → 4 columns
- Auto-dismissing flash alerts

---

## 🚀 Production Tips (Windows)

1. Set a strong secret key before running:
   ```cmd
   set SECRET_KEY=your-very-long-random-key
   python app.py
   ```
2. For production, use **Waitress** (Windows-compatible WSGI server):
   ```cmd
   pip install waitress
   waitress-serve --port=5000 app:app
   ```
3. Replace SQLite with PostgreSQL for multi-user production use.
4. Serve static files through IIS or a CDN.
