import pandas as pd # type: ignore
from openpyxl import Workbook # type: ignore

class ExcelReportExporter:
    def __init__(self, path="full_report.xlsx"):
        self.path = path
        self.writer = pd.ExcelWriter(self.path, engine='openpyxl')

    def _to_dataframe(self, data_dict):
        return pd.DataFrame([
            {
                "Код": code,
                "Наименование": entry["name"],
                **{f"Год {i+1}": v for i, v in enumerate(entry["values"])}
            } for code, entry in data_dict.items()
        ])

    def export_balance_and_results(self, balance_data, results_data):
        df_balance = self._to_dataframe(balance_data)
        df_results = self._to_dataframe(results_data)
        df_balance.to_excel(self.writer, sheet_name="Бухгалтерский баланс", index=False)
        df_results.to_excel(self.writer, sheet_name="Фин. результаты", index=False)

    def export_intermediate_indicators(self, intermediate_data):
        df_intermediate = self._to_dataframe(intermediate_data)
        df_intermediate.to_excel(self.writer, sheet_name="Промежуточные показатели", index=False)

    def export_risk_table(self, risk_table):
        rows = []
        for year_data in risk_table:
            row = {"Год": year_data["Год"]}
            for k, v in year_data["Факт"].items():
                row[f"{k} (Факт)"] = v
            for k, v in year_data["Норма"].items():
                row[f"{k} (Норма)"] = v
            row["Прогноз платежеспособности"] = year_data["Итог"]
            rows.append(row)
        pd.DataFrame(rows).to_excel(self.writer, sheet_name="Оценка риска", index=False)

    def export_altman(self, z_scores):
        df = pd.DataFrame(z_scores)
        df.to_excel(self.writer, sheet_name="Модель Альтмана", index=False)

    def finalize(self):
        self.writer.close()
