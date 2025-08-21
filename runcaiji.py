from app import create_app
from caiji.main.caiji_main import main

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        main()
