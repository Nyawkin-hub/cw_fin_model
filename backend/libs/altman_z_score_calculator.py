class AltmanZScoreCalculator:
    def __init__(self, balance_data: dict, results_data: dict):
        self.balance = balance_data
        self.results = results_data

    def get_values(self, code: int):
        return self.balance.get(code, {}).get("values", [0.0, 0.0, 0.0])

    def get_results(self, code: int):
        return self.results.get(code, {}).get("values", [0.0, 0.0, 0.0])

    def extrapolate_next_year(self, values):
        # Прогноз значения на следующий год по среднему темпу роста
        if len(values) < 2:
            return values + [values[-1] if values else 0.0]

        growth_rates = []
        for i in range(1, len(values)):
            prev, curr = values[i - 1], values[i]
            if prev != 0:
                growth = (curr - prev) / abs(prev)
                growth_rates.append(growth)

        avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0.0
        forecast = values[-1] * (1 + avg_growth)
        return values + [forecast]

    def compute_z_scores(self):
        z_scores = []

        # Прогнозируем данные на 2025
        assets = self.extrapolate_next_year(self.get_values(1600))
        current_assets = self.extrapolate_next_year(self.get_values(1200))
        current_liabilities = self.extrapolate_next_year(self.get_values(1500))
        retained_earnings = self.extrapolate_next_year(self.get_values(1370))
        ebit = self.extrapolate_next_year(self.get_results(2300))
        equity = self.extrapolate_next_year(self.get_values(1300))
        liabilities = self.extrapolate_next_year(self.get_values(1400))
        revenue = self.extrapolate_next_year(self.get_results(2110))

        for i in range(len(assets)):
            try:
                total_assets = assets[i] or 1

                x1 = (current_assets[i] - current_liabilities[i]) / total_assets
                x2 = retained_earnings[i] / total_assets
                x3 = ebit[i] / total_assets
                x4 = equity[i] / (liabilities[i] or 1)
                x5 = revenue[i] / total_assets

                z = 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * x5

                if z > 2.9:
                    risk = "Низкий риск банкротства"
                elif z > 1.23:
                    risk = "Пограничное состояние"
                else:
                    risk = "Высокий риск банкротства"

                z_scores.append({
                    "Год": 2022 + i,
                    "Z": round(z, 3),
                    "Риск": risk
                })
            except Exception as e:
                z_scores.append({
                    "Год": 2022 + i,
                    "Z": None,
                    "Риск": f"Ошибка расчета: {e}"
                })

        return z_scores
