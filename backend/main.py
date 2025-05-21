from libs.financial_data_extractor import FinancialDataExtractor

extractor = FinancialDataExtractor("./data/balance.xlsx")

# Лист 1 — Бухгалтерский баланс
balance_data = extractor.extract(
    sheet_index=1,
    row_start=0,
    row_end=100,
    columns=['Unnamed: 3', 'Unnamed: 8', 'Unnamed: 10', 'Unnamed: 13', 'Unnamed: 16'],
    skip_short_names=True
)

# Лист 2 — Отчет о фин. результатах
results_data = extractor.extract(
    sheet_index=2,
    row_start=4,
    row_end=38,
    columns=['Unnamed: 4', 'Unnamed: 9', 'Unnamed: 12', 'Unnamed: 15', 'Unnamed: 19'],
    skip_short_names=True
)

# Вывод данных
# for code, data in balance_data.items():
#     print(f"{code}: {data['name']} -> {data['values']}")

# for code, data in results_data.items():
#     print(f"{code}: {data['name']} -> {data['values']}")

#----------------------------------------------------------------------------------------------#

# Расчет промежуточных показателей
from libs.intermediate_indicator_calculator import IntermediateIndicatorsCalculator

calculator = IntermediateIndicatorsCalculator(balance_data, results_data)
intermediate_data = calculator.calculate()

# for code, entry in intermediate_data.items():
#     print(f"{code}: {entry['name']} -> {entry['values']}")

#----------------------------------------------------------------------------------------------#

from libs.bankruptcy_risk_evaluator import BankruptcyRiskEvaluator

evaluator = BankruptcyRiskEvaluator(balance_data, results_data, intermediate_data)
risk_table = evaluator.evaluate()

# for year_data in risk_table:
#     print(f"Год {year_data['Год']}: {year_data['Итог']}")
#     for key in year_data["Факт"]:
#         print(f"  {key} = {year_data['Факт'][key]} (норма: {year_data['Норма'][key]})")
#     print()

verbal_forecast = evaluator.predict_risk_verbal()
print("Оценка риска банкроства дебитора по финансовым показателям:", verbal_forecast)

#----------------------------------------------------------------------------------------------#

from libs.altman_z_score_calculator import AltmanZScoreCalculator
print("\n   Вероятность по методике Альтмана:")

calc = AltmanZScoreCalculator(balance_data, results_data)
results = calc.compute_z_scores()

for r in results:
    print(f"{r['Год']}: Z = {r['Z']} — {r['Риск']}")

#----------------------------------------------------------------------------------------------#

from libs.excel_report_exporter import ExcelReportExporter

exporter = ExcelReportExporter("Полный_финансовый_отчет.xlsx")
exporter.export_balance_and_results(balance_data, results_data)
exporter.export_intermediate_indicators(intermediate_data)
exporter.export_risk_table(risk_table)
exporter.export_altman(results)
exporter.finalize()

print("Финансовый отчет успешно экспортирован в Excel.")
