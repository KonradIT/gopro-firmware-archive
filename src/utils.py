from datetime import date


def get_day() -> str:
	today = date.today()
	return today.strftime("%d%m%Y")

def replace_line(file_name: str, line_num: int, text: str) -> None:
	lines = open(file_name, "r").readlines()
	lines[line_num] = text
	with open(file_name, "w") as out:
		out.writelines(lines)
