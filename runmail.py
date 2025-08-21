import time
import traceback
import datetime
import sys
from app import create_app
from mailpush.mail.content_builder import build_email_subject, build_email_body_html
from mailpush.mail.info_query import build_user_notifications
from mailpush.mail.update_status import mark_results_pushed, mark_stale_results
from logs.logger_config import setup_mail_logger, get_logger
from mailpush.mail.smtp_client import email_pool, SMTPClient
from mailpush.mail.email_heartbeat import EmailHeartbeat
from mailpush.mail.email_count import EmailCount


def run_mail_cycle():
    logger = get_logger(__name__)

    try:
        notifications = build_user_notifications()
    except Exception as e:
        logger.error(f"[FATAL] 获取待推送列表失败: {e}")
        logger.debug(traceback.format_exc())
        return

    if not notifications:
        logger.info("当前无待推送通知")
        return

    logger.info(f"本轮共需推送给 {len(notifications)} 个用户")

    email_count = EmailCount('config/email_count.txt')

    user_list = list(notifications.items())
    idx = 0

    while idx < len(user_list):
        try:
            acc = email_pool.get_available_account()
        except RuntimeError as e:
            logger.error(f"[STOP] 邮箱池无可用账号: {e}")
            break

        sent_num = email_count.get_count(acc['user'])
        logger.info(f"[POOL] 当前使用账号 {acc['user']} (已发 {sent_num}/{email_pool.daily_limit})")

        try:
            with SMTPClient(acc) as smtp:
                while idx < len(user_list) and email_count.get_count(acc['user']) < email_pool.daily_limit:
                    user, results = user_list[idx]
                    try:
                        subject = build_email_subject(user)
                        body = build_email_body_html(user, results)
                        smtp.send(user.email, subject, body, html=True)
                        email_count.increment(acc['user'])
                        logger.info(f"[OK] {user.username} <{user.email}> 已发送 (账号 {acc['user']})")
                        mark_results_pushed(results)
                    except Exception as e:
                        logger.error(f"[SEND_ERR] 发送给 {user.username} <{user.email}> 失败: {e}")
                        logger.debug(traceback.format_exc())
                    idx += 1
        except Exception as e:
            logger.error(f"[SMTP_ERR] 账号 {acc['user']} SMTP 会话错误: {e}")
            logger.debug(traceback.format_exc())
            continue

    # 清理遗留数据
    try:
        logger.info("[CLEAN] 开始清理超过24小时的遗留数据")
        stale_count = mark_stale_results(hours=24) or 0
        if stale_count > 0:
            logger.info(f"[CLEAN] 已清理 {stale_count} 条超过24小时的遗留数据")
        else:
            logger.info("[CLEAN] 无需清理遗留数据")
    except Exception as e:
        logger.error(f"[CLEAN_ERR] 清理遗留数据时发生错误: {e}")
        logger.debug(traceback.format_exc())


def main():
    logger = setup_mail_logger(include_console=True)
    app = create_app()

    with app.app_context():
        logger.info("=== 邮件推送服务启动 ===")
        logger.info("执行间隔: 10分钟")

        email_heartbeat = EmailHeartbeat(app)
        email_heartbeat.start_heartbeat()

        try:
            while True:
                cycle_start_time = datetime.datetime.now()
                logger.info(f"--- 开始执行推送任务 ({cycle_start_time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
                try:
                    run_mail_cycle()
                    logger.info("--- 推送任务执行完成 ---")
                except Exception as e:
                    logger.error(f"[CYCLE_ERR] 推送任务执行失败: {e}")
                    logger.debug(traceback.format_exc())
                logger.info("等待下次执行 (10分钟后)")
                time.sleep(10 * 60)
        except KeyboardInterrupt:
            logger.info("=== 收到停止信号，邮件推送服务正常退出 ===")
            sys.exit(0)
        except Exception as e:
            logger.critical(f"[FATAL] 服务运行时发生严重错误: {e}")
            logger.debug(traceback.format_exc())
            sys.exit(1)


if __name__ == '__main__':
    main()
