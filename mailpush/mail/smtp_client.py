import os
import smtplib
import datetime
import configparser
from itertools import cycle
from collections import defaultdict
from email.mime.text import MIMEText
from email.header import Header


def load_all_smtp_configs():
    """
    从 config/config.ini 读取所有 SMTP 配置。
    返回列表，每个元素是一个邮箱配置字典。
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    cfg_path = os.path.join(project_root, 'config', 'config.ini')
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"SMTP 配置文件未找到: {cfg_path}")

    parser = configparser.ConfigParser()
    parser.read(cfg_path, encoding='utf-8')

    configs = []
    for section in parser.sections():
        if section.lower().startswith("smtp"):
            sec = parser[section]
            configs.append({
                'host': sec.get('host'),
                'port': sec.getint('port'),
                'user': sec.get('user'),
                'password': sec.get('password'),
                'use_tls': sec.getboolean('use_tls', fallback=True)
            })

    if not configs:
        raise KeyError("配置文件中未找到任何 [smtp*] 段，请检查 config/config.ini")

    return configs


class EmailPool:
    def __init__(self, email_accounts, daily_limit=None):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        cfg_path = os.path.join(project_root, 'config', 'config.ini')

        parser = configparser.ConfigParser()
        parser.read(cfg_path, encoding='utf-8')

        if daily_limit is None:
            daily_limit = parser.getint("EMAIL", "daily_limit", fallback=30)

        self.accounts = email_accounts
        self.daily_limit = daily_limit
        self.send_count = defaultdict(int)
        self.current_date = datetime.date.today()
        self.cycle_accounts = cycle(self.accounts)

    def _reset_if_new_day(self):
        today = datetime.date.today()
        if today != self.current_date:
            self.send_count.clear()
            self.current_date = today

    def get_available_account(self):
        self._reset_if_new_day()
        for _ in range(len(self.accounts)):
            acc = next(self.cycle_accounts)
            if self.send_count[acc['user']] < self.daily_limit:
                return acc
        raise RuntimeError("邮箱池中所有邮箱今日已达到发送上限")

    def mark_sent(self, user):
        self._reset_if_new_day()
        self.send_count[user] += 1


class SMTPClient:
    def __init__(self, cfg, max_retries=3):
        self.cfg = cfg
        self.server = None
        self.from_addr = cfg['user']
        self.max_retries = max_retries

    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.server = smtplib.SMTP(self.cfg['host'], self.cfg['port'], timeout=10)
                if self.cfg['use_tls']:
                    self.server.starttls()
                self.server.login(self.cfg['user'], self.cfg['password'])
                return
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    raise RuntimeError(f"[SMTP_ERR] 连接失败，账号 {self.cfg['user']}，原因: {e}")
                else:
                    print(f"[WARN] 连接失败({e})，重试 {retries}/{self.max_retries} ...")

    def send(self, to_addr: str, subject: str, body: str, html: bool = False):
        if not self.server:
            self.connect()
        subtype = 'html' if html else 'plain'
        msg = MIMEText(body, subtype, 'utf-8')
        msg['From'] = self.from_addr
        msg['To'] = to_addr
        msg['Subject'] = Header(subject, 'utf-8')
        try:
            self.server.sendmail(self.from_addr, [to_addr], msg.as_string())
        except Exception as e:
            raise RuntimeError(f"[SMTP_ERR] 发送失败，账号 {self.from_addr}，原因: {e}")

    def close(self):
        try:
            if self.server:
                self.server.quit()
        except Exception:
            pass

    # 支持 with 语法
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



# 初始化邮箱池
smtp_configs = load_all_smtp_configs()
email_pool = EmailPool(smtp_configs, daily_limit=30)


def send_email_from_pool(to_addr, subject, body, html=False):
    acc = email_pool.get_available_account()
    client = SMTPClient(acc)
    client.send(to_addr, subject, body, html=html)
    client.close()
    email_pool.mark_sent(acc['user'])
    print(f"[INFO] 已使用邮箱 {acc['user']} 发送邮件至 {to_addr} (今日已发 {email_pool.send_count[acc['user']]}/{email_pool.daily_limit})")


if __name__ == "__main__":
    send_email_from_pool("2439314117@qq.com", "测试邮件", "这是测试正文")
