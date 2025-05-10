from rest_framework import serializers


class ActionSecuritiesSerializer(serializers.Serializer):
    """Сериализатор статистических данных по акции"""
    SECID = serializers.CharField(help_text='Идентификатор ценной бумаги')
    BOARDID = serializers.CharField(help_text='Идентификатор режима торгов')
    SHORTNAME = serializers.CharField(help_text='Краткое наименование ценной бумаги')
    PREVPRICE = serializers.FloatField(help_text='Цена закрытия предыдущего торгового дня')
    LOTSIZE = serializers.IntegerField(help_text='Размер лота (количество ценных бумаг в одном лоте)')
    FACEVALUE = serializers.FloatField(help_text='Номинальная стоимость ценной бумаги')
    STATUS = serializers.CharField(help_text='Статус ценной бумаги')
    BOARDNAME = serializers.CharField(help_text='Наименование режима торгов')
    SECNAME = serializers.CharField(help_text='Полное наименование ценной бумаги')
    REMARKS = serializers.CharField(help_text='Дополнительные примечания')
    MARKETCODE = serializers.CharField(help_text='Код рынка')
    INSTRID = serializers.CharField(help_text='Идентификатор инструмента')
    SECTORID = serializers.CharField(help_text='Идентификатор сектора')
    MINSTEP = serializers.FloatField(help_text='Минимальный шаг цены')
    PREVWAPRICE = serializers.FloatField(help_text='Средневзвешенная цена предыдущего дня')
    FACEUNIT = serializers.CharField(help_text='Валюта номинала')
    PREVDATE = serializers.DateField(help_text='Дата предыдущего торгового дня (формат YYYY-MM-DD)')
    ISSUESIZE = serializers.IntegerField(help_text='Общее количество выпущенных ценных бумаг')
    ISIN = serializers.CharField(help_text='ISIN код ценной бумаги')
    LATNAME = serializers.CharField(help_text='Название на латинице')
    REGNUMBER = serializers.CharField(help_text='Регистрационный номер')
    PREVLEGALCLOSEPRICE = serializers.FloatField(help_text='Официальная цена закрытия предыдущего дня')
    CURRENCYID = serializers.CharField(help_text='Валюта расчетов')
    SECTYPE = serializers.CharField(help_text='Тип ценной бумаги')
    LISTLEVEL = serializers.IntegerField(help_text='Уровень листинга')
    SETTLEDATE = serializers.DateField(help_text='Дата расчетов (формат YYYY-MM-DD)')


class ActionMarketdataSerializer(serializers.Serializer):
    """Сериализатор рыночных показателей по акции"""
    SECID = serializers.CharField(help_text='Идентификатор ценной бумаги')
    BOARDID = serializers.CharField(help_text='Идентификатор режима торгов')
    BID = serializers.FloatField(help_text='Лучшая цена спроса (покупки)')
    BIDDEPTH = serializers.IntegerField(help_text='Глубина спроса (количество лотов по лучшей цене покупки)')
    OFFER = serializers.FloatField(help_text='Лучшая цена предложения (продажи)')
    OFFERDEPTH = serializers.IntegerField(help_text='Глубина предложения (количество лотов по лучшей цене продажи)')
    SPREAD = serializers.FloatField(help_text='Спрэд между лучшими ценами покупки и продажи')
    BIDDEPTHT = serializers.IntegerField(help_text='Совокупный объем спроса')
    OFFERDEPTHT = serializers.IntegerField(help_text='Совокупный объем предложения')
    OPEN = serializers.FloatField(help_text='Цена открытия')
    LOW = serializers.FloatField(help_text='Минимальная цена за торговую сессию')
    HIGH = serializers.FloatField(help_text='Максимальная цена за торговую сессию')
    LAST = serializers.FloatField(help_text='Цена последней сделки')
    LASTCHANGE = serializers.FloatField(help_text='Изменение цены последней сделки по сравнению с предыдущей')
    LASTCHANGEPRCNT = serializers.FloatField(help_text='Изменение цены последней сделки в процентах')
    QTY = serializers.IntegerField(help_text='Количество бумаг в последней сделке')
    VALUE = serializers.FloatField(help_text='Объем сделок в валюте инструмента')
    VALUE_USD = serializers.FloatField(help_text='Объем сделок в USD')
    WAPRICE = serializers.FloatField(help_text='Средневзвешенная цена')
    LASTCNGTOLASTWAPRICE = serializers.FloatField(help_text='Разница между последней ценой и средневзвешенной')
    WAPTOPREVWAPRICEPRCNT = serializers.FloatField(help_text='Изменение средневзвешенной цены в процентах')
    WAPTOPREVWAPRICE = serializers.FloatField(help_text='Изменение средневзвешенной цены')
    CLOSEPRICE = serializers.FloatField(help_text='Цена закрытия')
    MARKETPRICETODAY = serializers.FloatField(help_text='Рыночная цена сегодня')
    MARKETPRICE = serializers.FloatField(help_text='Текущая рыночная цена')
    LASTTOPREVPRICE = serializers.FloatField(help_text='Изменение последней цены относительно предыдущего закрытия')
    NUMTRADES = serializers.IntegerField(help_text='Количество сделок за торговую сессию')
    VOLTODAY = serializers.IntegerField(help_text='Объем сделок в штуках ценных бумаг')
    VALTODAY = serializers.IntegerField(help_text='Объем сделок в валюте инструмента')
    VALTODAY_USD = serializers.IntegerField(help_text='Объем сделок в USD')
    ETFSETTLEPRICE = serializers.FloatField(help_text='Расчетная цена для ETF')
    TRADINGSTATUS = serializers.CharField(help_text='Статус торгов')
    UPDATETIME = serializers.TimeField(help_text='Время последнего обновления (формат HH:MM:SS)')


class ActionTradeStatisticsResponseSerializer(serializers.Serializer):
    """Сериализатор итоговых данных по акции, содержащих статистические данные и рыночные показатели"""
    ticker = serializers.CharField(help_text='Идентификатор ценной бумаги')
    securities = ActionSecuritiesSerializer()
    marketdata = ActionMarketdataSerializer()

    class Meta:
        description = (
            '\n\n**Статистические данные (securities):**\n{securities_fields}'
            '\n\n**Рыночные показатели (marketdata):**\n{marketdata_fields}'
        ).format(
            securities_fields='\n'.join(
                f'- {key}: {value.help_text}  ' for key, value in ActionSecuritiesSerializer().fields.items()
            ),
            marketdata_fields='\n'.join(
                f'- {key}: {value.help_text}  ' for key, value in ActionMarketdataSerializer().fields.items()
            ),
        )


class ActionCandlesResponseSerializer(serializers.Serializer):
    """Сериализатор данных по свечам по акции"""
    open = serializers.FloatField(help_text='Цена открытия за указанный временной интервал.')
    close = serializers.FloatField(help_text='Цена закрытия за указанный временной интервал.')
    high = serializers.FloatField(help_text='Максимальная цена за указанный временной интервал.')
    low = serializers.FloatField(help_text='Минимальная цена за указанный временной интервал.')
    value = serializers.FloatField(help_text='Общая стоимость всех сделок за указанный временной интервал.')
    volume = serializers.FloatField(help_text='Общий объем торгов за указанный временной интервал.')
    begin = serializers.DateTimeField(
        help_text='Дата и время начала временного интервала в формате YYYY-MM-DD HH:MM:SS.',
    )
    end = serializers.DateTimeField(
        help_text='Дата и время окончания временного интервала в формате YYYY-MM-DD HH:MM:SS.',
    )

    class Meta:
        description = (
            '- open: Цена открытия за указанный временной интервал.\n'
            '- close: Цена закрытия за указанный временной интервал.\n'
            '- high: Максимальная цена за указанный временной интервал.\n'
            '- low: Минимальная цена за указанный временной интервал.\n'  
            '- value: Общая стоимость всех сделок за указанный временной интервал.\n'  
            '- volume: Общий объем торгов за указанный временной интервал.\n'  
            '- begin: Дата и время начала временного интервала в формате YYYY-MM-DD HH:MM:SS.\n'  
            '- end: Дата и время окончания временного интервала в формате YYYY-MM-DD HH:MM:SS.\n'
        )


class ActionOrderBookResponseSerializer(serializers.Serializer):
    """Сериализатор данных по стаканам котировок по акции"""
    BOARDID = serializers.CharField(help_text='Идентификатор режима торгов')
    SECID = serializers.CharField(help_text='Идентификатор ценной бумаги')
    BUYSELL = serializers.CharField(help_text='Тип заявки: B - покупка, S - продажа')
    PRICE = serializers.FloatField(help_text='Цена заявки')
    QUANTITY = serializers.IntegerField(help_text='Количество бумаг в заявке')
    SEQNUM = serializers.IntegerField(help_text='Порядковый номер заявки')
    UPDATETIME = serializers.TimeField(help_text='Время обновления заявки в формате HH:MM:SS')
    DECIMALS = serializers.IntegerField(help_text='Количество знаков после запятой для цены')

    class Meta:
        description = (
            '- BOARDID: Идентификатор режима торгов.\n'
            '- SECID: Идентификатор ценной бумаги.\n'
            '- BUYSELL: Тип заявки: B - покупка, S - продажа.\n'
            '- PRICE: Цена заявки.\n'  
            '- QUANTITY: Количество бумаг в заявке.\n'  
            '- SEQNUM: Порядковый номер заявки.\n'  
            '- UPDATETIME: Время обновления заявки в формате HH:MM:SS.\n'  
            '- DECIMALS: Количество знаков после запятой для цены.\n'
        )


class ActionTradesResponseSerializer(serializers.Serializer):
    """Сериализатор данных по всем сделкам по акции"""
    TRADENO = serializers.IntegerField(help_text='Уникальный номер сделки')
    TRADETIME = serializers.TimeField(help_text='Время совершения сделки в формате HH:MM:SS')
    BOARDID = serializers.CharField(help_text='Идентификатор режима торгов')
    SECID = serializers.CharField(help_text='Идентификатор ценной бумаги')
    PRICE = serializers.FloatField(help_text='Цена сделки')
    QUANTITY = serializers.IntegerField(help_text='Количество бумаг в сделке')
    VALUE = serializers.FloatField(help_text='Объем сделки в денежном выражении')
    PERIOD = serializers.CharField(help_text='Период торгов')
    TRADETIME_GRP = serializers.IntegerField(help_text='Группа времени сделки')
    SYSTIME = serializers.DateTimeField(help_text='Системное время регистрации сделки')
    BUYSELL = serializers.CharField(help_text='Направление сделки: B - покупка, S - продажа')
    DECIMALS = serializers.IntegerField(help_text='Количество знаков после запятой для цены')
    TRADINGSESSION = serializers.CharField(help_text='Сессия торгов (1 - основная сессия)')

    class Meta:
        description = (
            '- TRADENO: Уникальный номер сделки.\n'
            '- TRADETIME: Время совершения сделки в формате HH:MM:SS.\n'
            '- BOARDID: Идентификатор режима торгов.\n'
            '- SECID: Идентификатор ценной бумаги.\n'  
            '- PRICE: Цена сделки.\n'  
            '- QUANTITY: Количество бумаг в сделке.\n'  
            '- VALUE: Объем сделки в денежном выражении.\n'  
            '- PERIOD: Период торгов.\n'
            '- TRADETIME_GRP: Группа времени сделки.\n'
            '- SYSTIME: Системное время регистрации сделки.\n'
            '- BUYSELL: Направление сделки: B - покупка, S - продажа.\n'
            '- DECIMALS: Количество знаков после запятой для цены.\n'
            '- TRADINGSESSION: Сессия торгов (1 - основная сессия).\n'
        )
