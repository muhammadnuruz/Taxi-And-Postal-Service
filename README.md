# 🚖 Taxi & Postal Service – Django Based Platform

### 🌐 Real-Time Taxi & Postal Booking System for Tashkent ↔ Samarqand

> **Status:** ✅ Deployed and actively used in production

## 🧭 Overview

This project is a real-world logistics platform designed to streamline **taxi and postal service bookings** between **Tashkent** and **Samarqand**. Built using the **Django** framework, it features a powerful admin panel for order management, route tracking, and user coordination. The system serves both **passenger transport** and **parcel delivery** needs through a unified interface.

---

## 🚀 Key Features

- 🔄 **Dual-Service Support** – Taxi and Postal services handled via one system.
- 🌍 **Route-Specific** – Focused on the high-demand route: **Tashkent ↔ Samarqand**.
- 📅 **Online Booking** – Real-time request and confirmation workflow.
- 🧑‍💼 **Admin Dashboard** – Robust Django admin panel to manage:
  - Orders & customers
  - Vehicle assignments
  - Schedule coordination
  - Status updates
- 🔒 **Secure & Role-Based Access** – Only authorized staff can access the backend.
- 📱 **Mobile-Friendly Design** – Optimized for use on mobile devices by admins and dispatchers.
- 📨 **Notifications & Status Tracking** – Integrated updates on order progression.

---

## 🛠️ Tech Stack

| Technology     | Purpose                       |
|----------------|-------------------------------|
| **Python**     | Core language                 |
| **Django**     | Web framework & admin panel   |
| **PostgreSQL** | Relational database           |
| **HTML/CSS**   | Frontend templating           |
| **Docker** (optional) | Containerization (future-ready) |

---

## 📂 Folder Structure (Key Parts)

```bash
├── apps/
│   ├── orders/        # Booking logic for taxi & postal
│   ├── drivers/       # Driver management
│   ├── vehicles/      # Vehicle registration
│   └── users/         # Authentication & roles
├── config/            # Django project settings
├── templates/         # Admin & frontend templates
├── static/            # CSS, JS, images
└── manage.py
```

---

## 📸 Screenshots

### 🧾 Order Creation (Admin Panel)
![Order panel screenshot](https://github.com/user-attachments/assets/24ca8196-8b67-4b73-a97f-84acae7d4d3f)

### 🧾 Sample — Store Request via Telegram
![Request screenshot](https://github.com/user-attachments/assets/8975313d-e3da-4251-99a5-504388172fed)

---

## ⚙️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/muhammadnuruz/Taxi-And-Postal-Service.git
cd Taxi-And-Postal-Service

# Create virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## 🧪 Testing

```bash
# Run Django tests
python manage.py test
```

---

## 📈 Roadmap

- [x] Tashkent ↔ Samarqand route system
- [x] Taxi & postal dual-mode support
- [ ] Telegram Bot integration
- [ ] Customer mobile app (React Native / Flutter)
- [ ] Driver location tracking

---

## 👤 Author

**Muhammad Nur** – [GitHub](https://github.com/muhammadnuruz)  
> Django Back-End Developer | Logistics System Builder

---

## 📬 Contact

For demo access or collaboration, feel free to reach out:  
📧 `nur.programmer@gmail.com`  
📍 Tashkent, Uzbekistan

---

## 🏁 Final Words

This project reflects **production-level expertise in Django**, real-world deployment, and industry-specific logic for transport and postal services.  
Ideal for logistics startups, dispatch companies, or regional delivery services.

## 👨‍💻 Developed By

**Muhammad Nur Suxbatullayev**  
🎓 Back-End Developer with 1+ years of hands-on experience  
🏫 Full Scholarship Recipient at PDP University  
🧠 Skilled in building scalable and secure back-end systems using:  

🔗 **GitHub:** [github.com/muhammadnuruz](https://github.com/muhammadnuruz)  
📬 **Telegram:** [@TheMuhammadNur](https://t.me/TheMuhammadNur)

---

## ⭐ Support the Project

If this project helped you, inspired you, or you simply liked it — please consider giving it a **⭐ on GitHub**.  
Your support boosts the project's visibility and motivates continued improvements and future updates.

Thank you for being part of the journey!
