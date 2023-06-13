from datetime import date, timedelta
import os


def get_day(days: int = None) -> str:
    if os.getenv("INPUT_CUSTOM_DATE") != None and os.getenv("INPUT_CUSTOM_DATE") != "":
        return str(os.getenv("INPUT_CUSTOM_DATE"))
    today = date.today()
    if days != None:
        today = today - timedelta(days=days)
    return today.strftime("%Y%m%d")


def replace_line(file_name: str, line_num: int, text: str) -> None:
    lines = open(file_name, "r").readlines()
    lines[line_num] = text
    with open(file_name, "w") as out:
        out.writelines(lines)
