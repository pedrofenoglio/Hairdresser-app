# day_manager.py
from datetime import datetime
import babel.numbers

class DayManager:
    @staticmethod
    def get_current_day():
        return datetime.now().strftime('%Y-%m-%d')
