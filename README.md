To setup, install these packages

```bash
pip install SQLAlchemy flask-socketio simple-websocket
```

To run the app, 

```bash
python3 app.py
```

Since this app uses cookies, you can't open it in separate tabs to test multiple client communication. This is because cookies are shared across tabs.
You'd have to use multiple browsers to test client communication.