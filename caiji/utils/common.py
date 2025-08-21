from datetime import datetime
import logging


def to_timestamp(org: str) -> datetime | None:
    """
    将页面上的时间字符串解析为 datetime 对象。
    支持以下格式：
      - "2025.04.27 15:08:45"
      - "2025年05月20日14点30分"
      - "2025年05月15日14:30"
      - "2025年05月15日09时"
      - "2025-04-28"
    返回：
      - 匹配成功时的 datetime 对象
      - 解析失败或空字符串时返回 None
    """
    if not org:
        logging.error("to_timestamp: 输入时间字符串为空")
        return None

    logging.debug(f"to_timestamp, 原始字符串: {org}")
    formats = [
        "%Y.%m.%d %H:%M:%S",   # 2025.04.27 15:08:45
        "%Y年%m月%d日%H点%M分",  # 2025年05月20日14点30分
        "%Y年%m月%d日%H:%M",    # 2025年05月15日14:30
        "%Y年%m月%d日%H时",     # 2025年05月15日09时
        "%Y-%m-%d",            # 2025-04-28
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(org, fmt)
            logging.debug(f"to_timestamp, 解析格式 {fmt}, 结果: {dt}")
            return dt
        except ValueError:
            continue

    logging.error(f"to_timestamp: 无法识别的时间格式: {org}")
    return None
