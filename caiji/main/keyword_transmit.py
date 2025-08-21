import json
from app.models.crawl_pool import CrawlPool
from caiji.main.modules_logs import get_module_logger
导入类


def run_spiders_from_pool(logger):
    """按 crawl_pool 配置顺序执行爬虫任务"""
    # 从 crawl_pool 表里获取所有任务，按 id 顺序读取
    tasks = CrawlPool.query.order_by(CrawlPool.id).all()

    SPIDER_MAP = {
        "网站名": 类名,
    }

    for task in tasks:
        try:
            spider_class = SPIDER_MAP.get(task.website_names)
            if not spider_class:
                logger.warning(f"未匹配到爬虫类，跳过：{task.website_names}")
                continue

            logger.info(f"启动爬虫：{task.website_names}，关键词：{task.keyword}")

            # 初始化爬虫
            spider = spider_class(
                category=task.category,
                keyword=task.keyword,
                config_name=task.config_names,
                website_name=task.website_names,
                source_url=task.source_url,
                logger=logger
            )

            # 执行爬虫
            items = spider.crawl()
            logger.info(f"{task.website_names} 爬取完成，共获取 {len(items)} 条记录")

            # 保存结果
            spider.save(items)
            logger.info(f"{task.website_names} 数据已保存至数据库")

        except Exception as e:
            logger.error(f"任务执行失败（{task.website_names}）：{e}", exc_info=True)
