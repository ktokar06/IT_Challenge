class StatisticsError(Exception):
    """Ошибка расчета статистики: задание получает статус failed."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)