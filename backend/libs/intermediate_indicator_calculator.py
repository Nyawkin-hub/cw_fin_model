class IntermediateIndicatorsCalculator:
    def __init__(self, balance_data: dict[int, dict], results_data: dict[int, dict]):
        self.balance = balance_data
        self.results = results_data

    def _get_values(self, code: int) -> list[float]:
        """Возвращает values по коду строки, либо нули."""
        return self.balance.get(code, {}).get("values", [0.0, 0.0, 0.0])

    def _get_results_values(self, code: int) -> list[float]:
        """Возвращает values из отчета о фин. результатах."""
        return self.results.get(code, {}).get("values", [0.0, 0.0, 0.0])

    def _sum_series(self, *series: list[float]) -> list[float]:
        """Складывает несколько списков поэлементно."""
        return [sum(values) for values in zip(*series)]

    def _sub_series(self, a: list[float], b: list[float]) -> list[float]:
        """Вычитает список b из списка a поэлементно."""
        return [x - y for x, y in zip(a, b)]

    def calculate(self) -> dict[int, dict]:
        """Возвращает словарь с расчетными показателями."""
        data = {}

        def row(i: int, name: str, values: list[float]):
            data[i] = {
                "name": name,
                "code": i,
                "values": values
            }

        # 1. Уставный капитал (стр. 1310 баланса)
        row(1, "Уставный капитал", self._get_values(1310))

        # 2. Капитал и резервы (стр. 1300 баланса)
        row(2, "Капитал и резервы", self._get_values(1300))

        # 3. Дебиторская задолженность участников по вкладам в уставный капитал (стр. 1230, частично)
        row(3, "Дебиторская задолженность участников по вкладам в уставный капитал", self._get_values(1230))  # при необходимости — фильтрация вручную

        # 4. Доходы будущих периодов (стр. 1530, без учета сч. 98)
        row(4, "Доходы будущих периодов", self._get_values(1530))  # уточнение: если известна доля "кредитовое сальдо", можно вычесть отдельно

        # 5. Ликвидные активы: 1232 + 1240 + 1250 + 1260 - 1320
        l_assets = self._sum_series(
            self._get_values(1232),
            self._get_values(1240),
            self._get_values(1250),
            self._get_values(1260),
        )
        l_assets = self._sub_series(l_assets, self._get_values(1320))
        row(5, "Ликвидные активы", l_assets)

        # 6. Текущие обязательства: 1510 + 1520 + 1530
        obligations = self._sum_series(
            self._get_values(1510),
            self._get_values(1520),
            self._get_values(1530),
        )
        row(6, "Текущие обязательства", obligations)

        # 7. Собственные средства: 1300 + 1430 + 1530 + 1540 + 1230 (в части учредителей)
        own_funds = self._sum_series(
            self._get_values(1300),
            self._get_values(1430),
            self._get_values(1530),
            self._get_values(1540),
            self._get_values(1230),  # предполагаем, что вся строка относится к задолженности учредителей
        )
        row(7, "Собственные средства", own_funds)

        # 8. Скорректированные внеоборотные активы: 1110 + 1130 + 1140 + 1150 + 1160 + 1170 + 1190
        fixed_assets = self._sum_series(
            self._get_values(1110),
            self._get_values(1130),
            self._get_values(1140),
            self._get_values(1150),
            self._get_values(1160),
            self._get_values(1170),
            self._get_values(1190),
        )
        row(8, "Скорректированные внеоборотные активы", fixed_assets)

        # 9. EBIT (стр. 2300 отчета о фин. результатах)
        row(9, "Операционная прибыль (или EBIT) до выплаты налогов", self._get_results_values(2300))

        return data
