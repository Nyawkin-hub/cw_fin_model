import pandas as pd
import re


class FinancialDataExtractor:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def _parse_number(self, val):
        """Безопасно парсит числовое значение из ячейки Excel."""
        try:
            if pd.isna(val):
                return 0.0
            val_str = str(val).replace(" ", "").replace(",", ".")
            if re.match(r"^\(\d+(\.\d+)?\)$", val_str):  # e.g., "(100)" => -100
                val_str = "-" + val_str.strip("()")
            return float(val_str)
        except:
            return 0.0

    def extract(
        self,
        sheet_index: int,
        row_start: int,
        row_end: int,
        columns: list[str],
        skip_short_names: bool = False
    ) -> dict[int, dict]:
        """
        Извлекает финансовые данные из указанного листа Excel.

        :param sheet_index: индекс листа (0-основанный)
        :param row_start: начальный индекс строки (включительно)
        :param row_end: конечный индекс строки (включительно)
        :param columns: список названий колонок [name_col, code_col, value1, value2, value3]
        :param skip_short_names: игнорировать строки с именами короче 4 символов
        :return: словарь {код: {name, code, values}}
        """
        df = pd.read_excel(self.filepath, sheet_name=sheet_index, engine='openpyxl')
        df = df.iloc[row_start:row_end + 1].reset_index(drop=True)

        df_sub = df[columns].copy()
        result = {}

        for _, row in df_sub.iterrows():
            name = str(row[columns[0]]).strip()
            if not name or name.lower() == 'nan':
                continue
            if skip_short_names and len(name) < 4:
                continue
            try:
                code = int(row[columns[1]])
            except (ValueError, TypeError):
                continue

            values = [self._parse_number(row[col]) for col in columns[2:]]

            result[code] = {
                "name": name,
                "code": code,
                "values": values
            }

        return result
