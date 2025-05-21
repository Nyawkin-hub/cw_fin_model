class BankruptcyRiskEvaluator:
    def __init__(self, balance_data: dict, result_data: dict, intermediate_data: dict):
        self.balance = balance_data
        self.results = result_data
        self.intermediate = intermediate_data

    def _get(self, source, code, default=[0.0, 0.0, 0.0]):
        return source.get(code, {}).get("values", default)

    def _calc_ratios(self):
        out = {}

        # Года
        years = len(self._get(self.balance, 1600))

        # Показатели
        total_assets = self._get(self.balance, 1600)
        obligations = self._get(self.balance, 1400)
        revenue = self._get(self.results, 2110)
        ebit = self._get(self.results, 2300)
        curr_assets = self._get(self.balance, 1200)
        short_liabilities = [
            sum(x) for x in zip(
                self._get(self.balance, 1510),
                self._get(self.balance, 1520),
                self._get(self.balance, 1530),
            )
        ]
        own_funds = self._get(self.intermediate, 7)  # Собственные средства
        fixed_assets = self._get(self.intermediate, 8)

        # 1. Чистые активы
        net_assets = [a - b for a, b in zip(total_assets, obligations)]
        out['Чистые активы, тыс. руб.'] = net_assets

        # 2. Запас прочности по точке безубыточности
        bez_ubytochnost = [e / r if r != 0 else 0.0 for e, r in zip(ebit, revenue)]
        out['Запас прочности по точке безубыточности, %'] = bez_ubytochnost

        # 3. Текущая ликвидность
        liquidity = [ca / sl if sl != 0 else 0.0 for ca, sl in zip(curr_assets, short_liabilities)]
        out['Текущая ликвидность'] = liquidity

        # 4. Коэффициент обеспеченности собственными оборотными средствами
        koeff_obesp = [
            (own - fix) / ca if ca != 0 else 0.0
            for own, fix, ca in zip(own_funds, fixed_assets, curr_assets)
        ]
        out['Коэффициент обеспеченности собственными оборотными средствами'] = koeff_obesp

        # 5. Коэффициент восстановления платежеспособности
        recovery = [
            (own_funds[i] - own_funds[i - 1]) / own_funds[i - 1]
            if i > 0 and own_funds[i - 1] != 0 else 0.0
            for i in range(years)
        ]
        out['Коэффициент восстановления платежеспособности'] = recovery

        # 6. Коэффициент утраты платежеспособности
        loss = [
            (own_funds[i] - own_funds[i - 1]) / net_assets[i - 1]
            if i > 0 and net_assets[i - 1] != 0 else 0.0
            for i in range(years)
        ]
        out['Коэффициент утраты платежеспособности'] = loss

        return out

    def _get_norms(self):
        return {
            'Чистые активы, тыс. руб.': lambda v: v > 0,
            'Запас прочности по точке безубыточности, %': lambda v: v > 0.1,
            'Текущая ликвидность': lambda v: v >= 1.0,
            'Коэффициент обеспеченности собственными оборотными средствами': lambda v: v > 0.1,
            'Коэффициент восстановления платежеспособности': lambda v: v > 0.1,
            'Коэффициент утраты платежеспособности': lambda v: v > -0.1,
        }

    def evaluate(self):
        calculated = self._calc_ratios()
        norms = self._get_norms()
        years = len(next(iter(calculated.values())))
        result_table = []

        for i in range(years):
            year_data = {"Год": 2022 + i, "Факт": {}, "Норма": {}, "Итог": ""}
            passed = 0

            for key, values in calculated.items():
                fact_val = round(values[i], 4)
                is_ok = norms[key](fact_val)
                norm_val = "OK" if is_ok else "BAD"
                if is_ok:
                    passed += 1
                year_data["Факт"][key] = fact_val
                year_data["Норма"][key] = norm_val

            # Прогноз по количеству пройденных норм
            if passed >= 5:
                prognosis = "Высокая платежеспособность"
            elif passed >= 3:
                prognosis = "Удовлетворительная"
            elif passed >= 1:
                prognosis = "Низкая"
            else:
                prognosis = "Критическая"

            year_data["Итог"] = prognosis
            result_table.append(year_data)

        return result_table

    
    def predict_risk_verbal(self):
        evaluation = self.evaluate()
        latest_year_data = evaluation[-1]  # Последний год

        status = latest_year_data["Итог"]

        if status == "Высокая платежеспособность":
            return "В ближайшие 12 месяцев низкая вероятность банкротства"
        elif status == "Удовлетворительная":
            return "В ближайшие 6 месяцев умеренная вероятность банкротства"
        elif status == "Низкая":
            return "В ближайшие 3 месяца высокая вероятность банкротства"
        else:
            return "В ближайшие 3 месяца очень высокая вероятность банкротства"