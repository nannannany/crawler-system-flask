from app.models.crawler_config import CrawlerConfig
from app.models.crawl_pool import CrawlPool
from config.db import db
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict


def sync_crawler_config_to_pool(logger):
    """
    从crawler_config表同步数据到crawl_pool表

    同步规则：
    从crawler_config获取所有记录的keywords, website_names, config_name, category
    重新组织成：每一个关键词+一个网站名+一组配置名的组合
    当keyword或website_name为空时，跳过该组合
    相同keyword+website_name组合的config_name会合并
    对于相同组合，category取第一个配置的值

    Returns:
        dict: 同步结果统计
    """
    try:
        # 查询所有crawler_config记录
        configs = CrawlerConfig.query.all()
        logger.info(f"获取到 {len(configs)} 条crawler_config记录")

        if not configs:
            logger.info("没有找到crawler_config记录，跳过同步")
            return {"status": "success", "message": "没有配置记录需要同步", "synced_count": 0}

        # 用于收集需要插入pool的数据
        pool_data = defaultdict(lambda: {"config_names": set(), "category": None})

        # 遍历每个配置记录
        for config in configs:
            config_name = config.config_name
            category = getattr(config, 'category', None)
            keywords = config.keywords or []
            website_names = config.website_names or []

            # 确保keywords和website_names是列表
            if not isinstance(keywords, list):
                logger.warning(f"配置 {config_name} 的keywords不是列表格式，跳过")
                continue

            if not isinstance(website_names, list):
                logger.warning(f"配置 {config_name} 的website_names不是列表格式，跳过")
                continue

            # 生成关键词和网站名的笛卡尔积
            for keyword in keywords:
                # 跳过空关键词
                if not keyword or not keyword.strip():
                    logger.debug(f"跳过空关键词，配置: {config_name}")
                    continue

                for website_name in website_names:
                    # 跳过空网站名
                    if not website_name or not website_name.strip():
                        logger.debug(f"跳过空网站名，配置: {config_name}")
                        continue

                    # 将配置名添加到对应的关键词+网站名组合中
                    pool_key = (keyword.strip(), website_name.strip())
                    pool_data[pool_key]["config_names"].add(config_name)

                    # 如果这是该组合的第一个配置，设置category
                    if pool_data[pool_key]["category"] is None:
                        pool_data[pool_key]["category"] = category

        logger.info(f"生成了 {len(pool_data)} 个唯一的关键词+网站名组合")

        # 清空现有的crawl_pool数据
        CrawlPool.query.delete()
        logger.info("清空了crawl_pool表的现有数据")

        # 批量插入新数据
        synced_count = 0
        for (keyword, website_name), data in pool_data.items():
            try:
                # 创建新的CrawlPool记录
                pool_record = CrawlPool(
                    source_url="",
                    keyword=keyword,
                    website_names=website_name,
                    config_names=list(data["config_names"]),  # 转换set为list
                    category=data["category"]
                )

                db.session.add(pool_record)
                synced_count += 1

            except Exception as e:
                logger.error(f"插入记录失败 - keyword: {keyword}, website: {website_name}, error: {str(e)}")
                continue

        # 提交事务
        db.session.commit()
        logger.info(f"成功同步 {synced_count} 条记录到crawl_pool")

        return {
            "status": "success",
            "message": f"成功同步 {synced_count} 条记录",
            "synced_count": synced_count,
            "total_configs": len(configs),
            "total_combinations": len(pool_data)
        }

    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = f"数据库操作失败: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg, "synced_count": 0}

    except Exception as e:
        db.session.rollback()
        error_msg = f"同步过程中发生未知错误: {str(e)}"
        logger.error(error_msg)
        return {"status": "error", "message": error_msg, "synced_count": 0}


if __name__ == "__main__":
    # 单体测试文件
    import sys
    import os
    import logging

    # 添加项目根目录到路径
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

    try:
        from app import create_app

        # 创建Flask应用
        app = create_app()

        # 在应用上下文中运行
        with app.app_context():
            logging.basicConfig(level=logging.INFO)
            test_logger = logging.getLogger(__name__)
            result = sync_crawler_config_to_pool(test_logger)
            print(f"同步结果: {result}")

    except ImportError as e:
        print(f"无法导入Flask应用: {e}")
        print("请确保在项目根目录下运行此脚本，或者在caiji_main中调用此函数")
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        print("建议在caiji_main中调用此函数")