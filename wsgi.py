from app import app, db


# db.drop_all()
db.create_all()

app.run()