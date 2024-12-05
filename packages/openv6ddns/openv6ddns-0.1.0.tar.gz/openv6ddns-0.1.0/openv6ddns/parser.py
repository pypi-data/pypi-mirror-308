import json
import csv
from datetime import datetime
from io import StringIO


class ResponseParser:
    def __init__(self, raw_data):
        self.raw_data = raw_data.strip()
        self.parsed_data = self._parse()

    def _parse(self):
        lines = self.raw_data.split("\n")
        result = {}
        for line in lines[:4]:
            key, value = line.split(":", 1)
            result[key.strip()] = self._convert_value(value.strip())
        csv_data = "\n".join(lines[4:])
        csv_reader = csv.DictReader(StringIO(csv_data))
        for row in csv_reader:
            row = {
                ("Key" if key == "#Key" else key): value for key, value in row.items()
            }
            result.update(
                {
                    key.strip(): self._convert_value(value.strip())
                    for key, value in row.items()
                }
            )
        if result.get("RESULT") == "OK":
            for key in ["Create", "LastRenew", "LastQuery"]:
                result[key] = self._convert_timestamp(result.get(key))
        return result

    def _convert_value(self, value):
        if value == "":
            return None
        if value.isdigit():
            return int(value)
        try:
            return int(value)
        except ValueError:
            return value

    def _convert_timestamp(self, value):
        if value in [None, 18000101000000]:
            return None
        try:
            return datetime.strptime(str(value), "%Y%m%d%H%M%S").isoformat()
        except (ValueError, TypeError):
            return value

    def to_json(self, indent=4):
        return json.dumps(self.parsed_data, indent=indent, ensure_ascii=False)

    def get_result(self):
        return {
            "status": self.parsed_data["RESULT"],
            "message_ja": self.parsed_data["RESULT_JA"],
            "message_en": self.parsed_data["RESULT_EN"],
            "size": self.parsed_data["RESULT_SIZE"],
        }

    def get_value(self, key):
        return self.parsed_data.get(key)
