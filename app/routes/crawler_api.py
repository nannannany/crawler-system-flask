from flask import Blueprint, request, jsonify
from config.db import db
from app.models.crawler_config import CrawlerConfig

bp_crawler = Blueprint('crawler_api', __name__, url_prefix='/api/crawler')


@bp_crawler.route('/<string:config_name>', methods=['GET'])
def get_config_by_name(config_name):
    """
    根据配置名 config_name 获取单条爬虫配置详情。
    GET /api/crawler/<config_name>
    返回 JSON:
      200: { "success": true,  "data": { ... } }
      404: { "success": false, "msg": "配置不存在" }
    """
    cfg = CrawlerConfig.query.get(config_name)
    if not cfg:
        return jsonify({"success": False, "msg": "配置不存在"}), 404

    return jsonify({"success": True, "data": cfg.to_dict()})


@bp_crawler.route('/<string:config_name>', methods=['PUT'])
def update_config(config_name):
    """
    更新指定配置名 config_name 对应的爬虫配置。
    支持更新字段：config_name（允许改名）、keywords、website_names、source_urls、category、created_user。
    PUT /api/crawler/<config_name>
    请求 JSON:
    {
      "config_name": "新配置名",         # 可选
      "keywords": [...],               # 可选
      "website_names": [...],          # 可选
      "source_urls": [...],            # 可选
      "category": "...",               # 必填
      "created_user": "用户名"           # 必填
    }
    返回 JSON:
      200: { "success": true, "msg": "配置更新成功" }
      400: { "success": false, "msg": "参数错误" }
      404: { "success": false, "msg": "配置不存在" }
    """
    data = request.get_json() or {}

    category = data.get('category')
    created_user = data.get('created_user')

    if not category or not created_user:
        return jsonify({"success": False, "msg": "category 和 created_user 为必填"}), 400

    cfg = CrawlerConfig.query.get(config_name)
    if not cfg:
        return jsonify({"success": False, "msg": "配置不存在"}), 404

    new_name = data.get('config_name')
    if new_name:
        cfg.config_name = new_name

    if 'keywords' in data:
        cfg.keywords = data['keywords']
    if 'website_names' in data:
        cfg.website_names = data['website_names']
    if 'source_urls' in data:
        cfg.source_urls = data['source_urls']

    cfg.category = category
    cfg.created_user = created_user

    db.session.commit()

    return jsonify({"success": True, "msg": "配置更新成功"})


@bp_crawler.route('/', methods=['POST'])
def create_config():
    """
    新建一条爬虫配置。
    支持字段：config_name（必填）、keywords（可选）、website_names（可选）、source_urls（可选）、category（必填）、created_user（必填）。
    POST /api/crawler/
    请求 JSON:
    {
      "config_name": "唯一配置名",       # 必填
      "keywords": [...],               # 可选，默认空列表
      "website_names": [...],          # 可选，默认空列表
      "source_urls": [...],            # 可选，默认空列表
      "category": "...",               # 必填
      "created_user": "用户名"           # 必填
    }
    返回 JSON:
      201: { "success": true, "msg": "配置创建成功" }
      400: { "success": false, "msg": "参数错误" }
      409: { "success": false, "msg": "配置名已存在" }
    """
    data = request.get_json() or {}

    config_name = data.get('config_name')
    category = data.get('category')
    created_user = data.get('created_user')

    if not config_name or not category or not created_user:
        return jsonify({"success": False, "msg": "config_name, category 和 created_user 为必填"}), 400

    if CrawlerConfig.query.get(config_name):
        return jsonify({"success": False, "msg": "配置名已存在"}), 409

    keywords = data.get('keywords', [])
    website_names = data.get('website_names', [])
    source_urls = data.get('source_urls', [])

    cfg = CrawlerConfig(
        config_name=config_name,
        keywords=keywords,
        website_names=website_names,
        source_urls=source_urls,
        category=category,
        created_user=created_user,
    )

    db.session.add(cfg)
    db.session.commit()

    return jsonify({"success": True, "msg": "配置创建成功"}), 201


@bp_crawler.route('/<string:config_name>', methods=['DELETE'])
def delete_config(config_name):
    """
    删除指定配置名 config_name 的配置项。
    DELETE /api/crawler/<config_name>
    返回 JSON:
      200: { "success": true,  "msg": "配置已删除" }
      404: { "success": false, "msg": "配置不存在" }
    """
    cfg = CrawlerConfig.query.get(config_name)
    if not cfg:
        return jsonify({"success": False, "msg": "配置不存在"}), 404

    db.session.delete(cfg)
    db.session.commit()
    return jsonify({"success": True, "msg": "配置已删除"})


# 测试用接口，输出所有
@bp_crawler.route('/', methods=['GET'])
def list_configs():
    """
    GET /api/crawler/
    列出所有 CrawlerConfig 记录，返回 JSON:
    {
      "success": true,
      "data": [ { ... }, ... ]
    }
    """
    configs = CrawlerConfig.query.order_by(CrawlerConfig.updated_at.desc()).all()
    return jsonify({
        "success": True,
        "data": [c.to_dict() for c in configs]
    })