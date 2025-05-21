# cw_fin_model
coursework on financial modeling

# class FinancialDataExtractor
This class is designed to extract data from an .xlsx file

# class IntermediateIndicatorsCalculator
This class performs the calculation of intermediate indicators

# class BankruptcyRiskEvaluator
This class evaluates the debtor's bankruptcy risk based on financial indicators

# class AltmanZScoreCalculator
Altman Z-score - linear discriminant model based on several coefficients

z = 0.717 * x1 + 0.847 * x2 + 3.107 * x3 + 0.420 * x4 + 0.998 * x5

    X₁ = (Оборотные активы − Краткосрочные обязательства) / Общие активы
    → текущая ликвидность (working capital / total assets)
    X₂ = Нераспределённая прибыль / Общие активы
    → накопленные резервы (retained earnings / total assets)
    X₃ = EBIT / Общие активы
    → рентабельность активов
    X₄ = Собственный капитал / Общая задолженность
    → капитализация
    X₅ = Выручка / Общие активы
    → деловая активность (оборачиваемость активов)

Z > 2.9	Низкий риск банкротства
1.23 < Z ≤ 2.9	Пограничное состояние (серая зона)
Z ≤ 1.23	Высокий риск банкротства

# TODO 
- No balance check
- No automatic data retrieval
- no frontend
