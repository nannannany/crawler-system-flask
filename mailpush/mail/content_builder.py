from app.models.crawl_results import CrawlResult
from app.models.users_model import User


def build_email_subject(user: User) -> str:
    """
    构造邮件主题：
      "<username>"您好，招标信息集成系统来信息了
    """
    return f'"{user.username}"您好，信息集成系统来信息了'


def build_email_body_html(user: User, results: list[CrawlResult]) -> str:
    """
    构造 HTML 格式的邮件正文，将每条 CrawlResult 单独作为一个段落输出，
    并且把 detail_url 渲染为可点击的 <a> 链接。
    """
    parts = []
    for r in results:
        # config_name 现在是字符串类型，不再是列表
        config_display = r.config_name or '未知配置'
        ts = r.publish_time.strftime('%Y-%m-%d %H:%M:%S') if r.publish_time else '未知时间'
        part = f"""
        <div style="margin-bottom:20px;">
          <p>信息集成系统刚刚获取到，关于"<strong>{r.category}</strong>"板块、"<strong>{config_display}</strong>"配置的信息：</p>
          <p>关键字：<em>{r.keyword}</em>，来源：<em>{r.website_name}</em>，时间：<em>{ts}</em>。</p>
          <p>标题：<strong>{r.title}</strong></p>
          <p>跳转网址：<a href="{r.detail_url}" target="_blank">{r.detail_url}</a></p>
          <p>—————————————————————————————————————————————————————————————————————————————————————————————————————————————————————</p>
        </div>
        """
        parts.append(part.strip())

    # 整合所有模块
    return "<html><body>" + "\n".join(parts) + "</body></html>"