from app import create_app
import flask_monitoringdashboard as dashboard
from app.model import *


app = create_app()
dashboard.config.init_from(file='config.cfg')
dashboard.bind(app)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')