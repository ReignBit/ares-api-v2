activate_this = '.venv/bin/activate'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import create_app()

application = create_app("app.config.ProductionConfig")
