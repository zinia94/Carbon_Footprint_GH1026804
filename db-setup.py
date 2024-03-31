from src import app, db
app.app_context().push()
db.drop_all()
db.create_all()
db.session.commit()
exit(1)