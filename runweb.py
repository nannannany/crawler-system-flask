from app import create_app
from app.utils.recover_caiji import start_heartbeat_monitor_caiji
from app.utils.recover_mail import start_heartbeat_monitor_mail

app = create_app()


if __name__ == '__main__':
    start_heartbeat_monitor_mail(app)
    start_heartbeat_monitor_caiji(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
