from rest_framework import serializers


class PredictActionCandlesResponseSerializer(serializers.Serializer):
    """Сериализатор данных по свечам по акции"""
    close = serializers.FloatField(help_text='Цена закрытия за указанный временной интервал.')
    begin = serializers.DateTimeField(
        help_text='Дата и время начала временного интервала в формате YYYY-MM-DD HH:MM:SS.',
    )
    end = serializers.DateTimeField(
        help_text='Дата и время окончания временного интервала в формате YYYY-MM-DD HH:MM:SS.',
    )

    class Meta:
        description = (
            '- close: Цена закрытия за указанный временной интервал.\n'
            '- begin: Дата и время начала временного интервала в формате YYYY-MM-DD HH:MM:SS.\n'  
            '- end: Дата и время окончания временного интервала в формате YYYY-MM-DD HH:MM:SS.\n'
        )
