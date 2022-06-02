from datetime import date, timedelta


def get_day() -> str:
    today = date.today()
    today = today - timedelta(days=1)
    return today.strftime("%Y%m%d")


def replace_line(file_name: str, line_num: int, text: str) -> None:
    lines = open(file_name, "r").readlines()
    lines[line_num] = text
    with open(file_name, "w") as out:
        out.writelines(lines)
