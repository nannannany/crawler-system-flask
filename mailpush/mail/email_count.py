import os
import json
import datetime
from collections import defaultdict

class EmailCount:
    def __init__(self, filepath='config/email_count.txt'):
        self.filepath = filepath
        self.current_date = datetime.date.today()
        self.send_count = self._load_counts()

    def _load_counts(self):
        if not os.path.exists(self.filepath):
            return defaultdict(int)
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 如果日期不是今天，清空计数
            if data.get('date') != self.current_date.isoformat():
                return defaultdict(int)
            return defaultdict(int, data.get('counts', {}))
        except Exception:
            # 读取异常时，返回空计数
            return defaultdict(int)

    def _save_counts(self):
        data = {
            'date': self.current_date.isoformat(),
            'counts': dict(self.send_count)
        }
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reset_if_new_day(self):
        today = datetime.date.today()
        if today != self.current_date:
            self.current_date = today
            self.send_count.clear()
            self._save_counts()

    def get_count(self, user):
        self.reset_if_new_day()
        return self.send_count[user]

    def increment(self, user):
        self.reset_if_new_day()
        self.send_count[user] += 1
        self._save_counts()
