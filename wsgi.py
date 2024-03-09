from app import app

if __name__ == '__main':
    app.run(debug = True, port = 3000, use_reloader=False)