from flask import Blueprint, request, jsonify
from app.models.users_model import User
from config.db import db
from datetime import datetime

bp_users = Blueprint('bp_users', __name__, url_prefix='/api/users')


@bp_users.route('/', methods=['GET'])
def get_all_users():
    """
    获取所有用户信息。
    GET /api/users/
    返回 JSON:
      {
        "username": "user1",
        "email": "user1@example.com",
        "push_categories": [...],
        "push_switch": 1,
        "created_at": "...",
        "updated_at": "..."
      }
    """
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@bp_users.route('/<string:username>', methods=['GET'])
def get_user(username):
    """
    根据用户名 username 获取单个用户信息。
    GET /api/users/<username>
    返回 JSON:
      200: {
        "username": "...",
        "email": "...",
        "push_categories": [...],
        "push_switch": 1,
        "created_at": "...",
        "updated_at": "..."
      }
      404: { "success": false, "msg": "用户不存在" }
    """

    user = User.query.get(username)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"success": False, "msg": "用户不存在"}), 404


@bp_users.route('/', methods=['POST'])
def create_user():
    """
    创建新用户。
    支持字段：username（必填）、email（必填）、push_categories（可选）、push_switch（可选）。
    POST /api/users/
    请求 JSON:
    {
      "username": "用户名",               # 必填
      "email": "用户邮箱",                # 必填
      "push_categories": ["配置1"],    # 可选，默认 []
      "push_switch": 1                   # 可选，默认 1
    }
    返回 JSON:
      200: { "success": true, "msg": "用户创建成功" }
      400: { "success": false, "msg": "username 和 email 为必填" }
      409: { "success": false, "msg": "用户名已存在" }
    """

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')

    if not username or not email:
        return jsonify({"success": False, "msg": "username 和 email 为必填"}), 400

    if User.query.get(username):
        return jsonify({"success": False, "msg": "用户名已存在"}), 409

    user = User(
        username=username,
        email=email,
        push_categories=data.get('push_categories', []),
        push_switch=data.get('push_switch', 1),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"success": True, "msg": "用户创建成功"})


@bp_users.route('/<string:username>', methods=['PUT'])
def update_user(username):
    """
    更新指定用户名的用户信息。
    支持更新字段：email、push_categories、push_switch。
    PUT /api/users/<username>
    请求 JSON:
    {
      "email": "新邮箱",                  # 可选
      "push_categories": ["军工"],       # 可选
      "push_switch": 0                   # 可选
    }
    返回 JSON:
      200: { "success": true, "msg": "用户更新成功" }
      404: { "success": false, "msg": "用户不存在" }
    """
    user = User.query.get(username)
    if not user:
        return jsonify({"success": False, "msg": "用户不存在"}), 404

    data = request.get_json()
    user.email = data.get('email', user.email)
    user.push_categories = data.get('push_categories', user.push_categories)
    user.push_switch = data.get('push_switch', user.push_switch)
    user.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify({"success": True, "msg": "用户更新成功"})


@bp_users.route('/<string:username>', methods=['DELETE'])
def delete_user(username):
    """
    删除指定用户名的用户。
    DELETE /api/users/<username>
    返回 JSON:
      200: { "success": true, "msg": "用户删除成功" }
      404: { "success": false, "msg": "用户不存在" }
    """
    user = User.query.get(username)
    if not user:
        return jsonify({"success": False, "msg": "用户不存在"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "msg": "用户删除成功"})
