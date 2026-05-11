class CalendarService:
    def week_view(self) -> dict:
        return {
            "timezone": "Europe/Istanbul",
            "events": [
                {"day": "Tue", "start": "14:00", "end": "15:30", "title": "Yazilim Mimari Atolyesi", "conflict": True},
                {"day": "Wed", "start": "18:30", "end": "19:30", "title": "Veri Bilimi ve Gelecek", "conflict": False},
            ],
        }


calendar_service = CalendarService()
