# API-Backend Setup and Deployment Guide 🚀

## Setting Up Your Python Django Project 🐍

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**:
   - Configure your database settings in `settings.py`.
   - Run initial migrations:
     ```bash
     python manage.py migrate
     ```

5. **Create a Superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

## Deploying to Heroku 🌐

1. **Login to Heroku**:
   ```bash
   heroku login
   ```

2. **Use Existing Heroku App**:
   - The app name is `manychat-api`.

3. **Set Up Heroku Postgres** (if using PostgreSQL):
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev --app manychat-api
   ```

4. **Configure Environment Variables**:
   - Set your environment variables using:
     ```bash
     heroku config:set KEY=VALUE --app manychat-api
     ```

5. **Prepare for Deployment**:
   - Ensure your `Procfile` is set up correctly:
     ```
     web: gunicorn your_project_name.wsgi
     ```

6. **Deploy Your Code**:
   - Push your changes to the origin repository:
     ```bash
     git push origin main
     ```
   - This will automatically trigger deployment on Heroku.

7. **Run Migrations on Heroku**:
   - Before accessing your app, make sure to run migrations:
     ```bash
     heroku run python manage.py migrate -a manychat-api
     ```

## Conclusion 🎉

You are now set up to develop and deploy your Django project on Heroku! Happy coding! 💻
