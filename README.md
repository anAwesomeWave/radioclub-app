# radioclub-app

## 📖 About:
Simaple web-app for radioclub. Allows users to listen to radiohead music, comment and rate it

## 📦 Installation:
1. Clone this repository from GitHub:

```
git@github.com:anAwesomeWave/radioclub-app.git
```

2. Go to project directory:

```
cd radioclub-app
```
3. Install all dependencies:

```
pip3 install -r requirements.txt
```

4. Go to backend directory, create and apply migrations:

```
cd radioclub_backend
```
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```

## 💡 Quickstart:
To start backend server, simply run:

```
python3 manage.py runserver
```