from app import app

# This is required for Vercel
application = app

if __name__ == '__main__':
    app.run(debug=True) 