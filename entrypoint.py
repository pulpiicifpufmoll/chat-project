from app import app, io, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    io.run(app, debug= True, host="0.0.0.0", port=5001)
