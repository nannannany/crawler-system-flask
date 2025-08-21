from flask import Blueprint, request, jsonify
from app.models.crawl_results import CrawlResult
from config.db import db

bp_result = Blueprint('result_api', __name__, url_prefix='/api/results')


@bp_result.route('/', methods=['POST'])
def get_crawl_results():
    """
    查询 crawl_results 表数据，支持根据 category、config_name 和 website_name 过滤。

    请求示例：
      POST /api/results
      Content-Type: application/json

      {}                                                        # 查询所有数据（默认第1页，15条）
      {"page": 2, "page_size": 20}                             # 分页查询所有数据（第2页，20条）
      {"category": "招标"}                                      # 按类别查询
      {"config_name": "招标投标网"}                            # 按配置名查询
      {"website_name": "政策"}                                 # 按网站名称查询
      {"category": "招标", "config_name": "sina_tech", "website_name": "招标投标网"}  # 多条件查询
      {"category": "招标", "config_name": "tencent_sports", "page": 2, "page_size": 30}
    """
    try:
        # 获取JSON数据，如果没有JSON数据则使用空字典
        json_data = request.get_json() or {}

        # 获取分页参数，设置默认值
        page = max(int(json_data.get('page', 1)), 1)
        page_size = max(int(json_data.get('page_size', 15)), 1)
    except (ValueError, TypeError):
        return jsonify({"error": "分页参数必须为整数"}), 400

    # 获取过滤参数，允许为空
    category = json_data.get('category')
    config_name = json_data.get('config_name')
    website_name = json_data.get('website_name')

    # 构建查询
    query = db.session.query(CrawlResult)

    # 根据传入的参数进行过滤
    if category:
        query = query.filter(CrawlResult.category == category)
    if config_name:
        query = query.filter(CrawlResult.config_name == config_name)
    if website_name:
        query = query.filter(CrawlResult.website_name == website_name)

    # 查询总记录数
    total = query.count()

    # 分页查询数据
    results = (
        query.order_by(CrawlResult.publish_time.desc().nullslast())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    data = [r.to_dict() for r in results]

    return jsonify({
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total
        }
    })


# 保留GET方法兼容性
@bp_result.route('/', methods=['GET'])
def get_crawl_results_get():
    """
    通过查询字符串获取抓取结果列表（兼容 GET 请求方式）。
    支持参数：
      - page: 页码（默认 1）
      - page_size: 每页数量（默认 15）
      - category: 按类别过滤（可选）
      - config_name: 按配置名过滤（可选）
      - website_name: 按网站名称过滤（可选）

    返回 JSON 分页数据。
    """
    try:
        page = max(int(request.args.get('page', 1)), 1)
        page_size = max(int(request.args.get('page_size', 15)), 1)
    except ValueError:
        return jsonify({"error": "分页参数必须为整数"}), 400

    # 获取过滤参数
    category = request.args.get('category')
    config_name = request.args.get('config_name')
    website_name = request.args.get('website_name')

    # 构建查询
    query = db.session.query(CrawlResult)

    # 根据传入的参数进行过滤
    if category:
        query = query.filter(CrawlResult.category == category)
    if config_name:
        query = query.filter(CrawlResult.config_name == config_name)
    if website_name:
        query = query.filter(CrawlResult.website_name == website_name)

    # 查询总记录数
    total = query.count()

    # 分页查询数据
    results = (
        query.order_by(CrawlResult.publish_time.desc().nullslast())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    data = [r.to_dict() for r in results]

    return jsonify({
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total
        }
    })
