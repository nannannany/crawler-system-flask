from flask import Blueprint, jsonify
from app.models.heartbeat_model import Heartbeat

bp_heartbeat = Blueprint('heartbeat', __name__, url_prefix='/api/heartbeat')


@bp_heartbeat.route('/', methods=['GET'])
def get_heartbeat_status():
    """
    GET /api/heartbeat/
    获取当前爬虫与邮件服务的心跳状态。
    返回 JSON:
    {
      "heartbeat": { … }   # id=1 的记录
    }
    """
    record = Heartbeat.query.get(1)

    return jsonify({
        'heartbeat': record.to_dict() if record else None
    })
