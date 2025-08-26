

---

# 📌 README

---

## 📦 Equipment Control System

This project was developed using **Django** to manage and track equipment.  
It allows you to control devices in different states: **active, inactive, in stock, with technicians, or with customers**.  

It also provides a **tracking view**, where you can search by **MAC Address** or **Serial Number**, and see the full history of movements, including the responsible people and the reasons.



## 🚀 Technologies Used
- [Django](https://www.djangoproject.com/) — Backend web framework
- [Chart.js](https://www.chartjs.org/) — Dynamic charts for frontend

## ⚙️ How to Run the Project

1. Clone the repository:<br>
   ```bash
   git clone https://github.com/Miichaaeell/controle_de_equipamento.git
   ```
2. Create and activate your virtual environment.

3. Install dependencies:
   ```bash
    pip install -r requirements.txt
    ```  

4. Run migrations:<br>
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```


5. Create a superuser:<br>
    ```bash
    python manage.py createsuperuser
    ```

6. Start the development server:<br>
    ```bash
    python manage.py runserver

    ```

  Visit in your browser: http://127.0.0.1:8000

---
## 📊 Populate Database for Testing

The project includes a custom management command that generates 2000 fake records automatically:<br><br>
  ```bash
  python manage.py populatedb
  ```

## ⚠️ Important: You must already have at least one user created before running this command.
---
## 📌 Main Features

Equipment registration and management.

Quick search by MAC Address or Serial Number.

Complete movement history for each equipment.

Statistics and charts with Chart.js.

Automatic test data generation via populatedb command.

---
👨‍💻 Author<br>
@Miichaaeell
