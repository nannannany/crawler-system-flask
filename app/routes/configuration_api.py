from flask import Blueprint, request, jsonify
from config.db import db
from app.models.base_crawler import BaseCrawler
from app.models.crawler_config import CrawlerConfig
from datetime import datetime, timedelta

bp_configuration = Blueprint('configuration', __name__, url_prefix='/api/configurations')


@bp_configuration.route('/', methods=['GET'])
def get_all_configurations():
    """
    GET /api/configurations/
    一次性读取一条 BaseCrawler 和所有 CrawlerConfig 记录，用于页面展示。
    返回 JSON:
    {
      "base_crawler": { … },         # 单条基础爬虫配置
      "crawler_configs": [ … ]       # 爬虫配置列表
    }
    """
    base = BaseCrawler.query.order_by(BaseCrawler.id).first()
    configs = CrawlerConfig.query.order_by(CrawlerConfig.updated_at.desc()).all()

    return jsonify({
        'base_crawler': base.to_dict() if base else None,
        'crawler_configs': [cfg.to_dict() for cfg in configs]
    })


@bp_configuration.route('/base', methods=['PATCH'])
def update_base_configuration():
    """
    PATCH /api/configurations/base
    更新唯一的 BaseCrawler 实例的 switch_status 和 frequency。
    请求 JSON:
    {
      "switch_status": 0 or 1,
      "frequency": <int, >=1>
    }
    返回更新后的 BaseCrawler.to_dict()
    """
    data = request.get_json() or {}

    switch_status = data.get('switch_status')
    frequency = data.get('frequency')
    if switch_status not in (0, 1):
        return jsonify({'error': 'switch_status 必须为 0 或 1'}), 400
    if not isinstance(frequency, int) or frequency < 1:
        return jsonify({'error': 'frequency 必须为正整数'}), 400

    base = BaseCrawler.query.order_by(BaseCrawler.id).first()
    if not base:
        return jsonify({'error': '未找到基础配置，请先初始化一条'}), 404

    base.switch_status = switch_status
    base.frequency = frequency
    base.updated_at = datetime.utcnow()
    # base.next_run_time = datetime.utcnow() + timedelta(hours=frequency)  #取消前端对下一次爬取时间做修改，控制权交给爬虫

    db.session.commit()

    return jsonify(base.to_dict())
