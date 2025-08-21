from .configuration_api import bp_configuration
from .crawler_api import bp_crawler
from .result_api import bp_result
from .users_api import bp_users
from .heartbeat_api import bp_heartbeat
from .auth import bp_login


def register_routes(app):
    """
    蓝图注册
    """
    app.register_blueprint(bp_configuration)
    app.register_blueprint(bp_crawler)
    app.register_blueprint(bp_result)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_heartbeat)
    app.register_blueprint(bp_login)
