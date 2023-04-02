from app import app
from utils.db import db
from utils.log_manager import login_manager_app


with app.app_context():
    db.init_app(app)
    db.create_all()
    login_manager_app.init_app(app)
    
    

if __name__=='__main__':
    app.run()
    