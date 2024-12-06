import marimo

__generated_with = "0.9.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        """
        # Holiday Announcement Parser


              The Holiday Announcement Parser is a powerful tool designed to streamline your holiday scheduling process. By simply entering the holiday scheduler text, this app accurately extracts all the holidays and compensatory working days, providing a clear and organized schedule.
        """
    )
    return


@app.cell
def __(mo):
    schedule = mo.ui.text_area(
        label="Enter the annual public holiday schedule for China:",
        placeholder="国务院办公厅关于xxxx年",
        full_width=True,
    )
    schedule
    return (schedule,)


@app.cell
def __(mo, schedule_download, schedule_table):
    mo.vstack(
        [
            schedule_download,
            schedule_table,
        ],
    )
    return


@app.cell
def __(
    dict_table,
    json,
    mo,
    parse_holidays_comp_working_days,
    parse_year,
    schedule,
):
    mo.stop(len(schedule.value) == 0)

    schedule_year = parse_year(
        schedule.value.split("\n"), r"国务院办公厅关于(\d{4})年"
    )

    mo.stop(
        schedule_year is None,
        mo.md("**ValueError: Year not found in the document**"),
    )

    schedule_obj = parse_holidays_comp_working_days(
        schedule.value.split("\n"),
        schedule_year,
    )

    schedule_table = mo.ui.table(
        data=dict_table(schedule_obj), pagination=True, page_size=20
    )

    schedule_download = mo.download(
        data=json.dumps(schedule_obj, indent=2),
        filename="schedule.json",
        label="Download the schedule in JSON format",
    )
    return schedule_download, schedule_obj, schedule_table, schedule_year


@app.cell
def __():
    import re
    from datetime import date, datetime, timedelta
    import json
    from collections import OrderedDict

    HOLIDAY_PATTERN = r"((\d{4})年)?(\d{1,2})月(\d{1,2})日(至(((\d{4})年)?(\d{1,2})月)?(\d{1,2})日)?放假"
    HAS_COMP_WORKING_PATTERN = r"(.*)上班"
    COMP_WORKING_DAY_PATTERN = r"((\d{4}年)?\d{1,2}月\d{1,2}日)（星期[六日]）"

    # Convert a string in 'YYYY年MM月DD日' format to a date object.
    str_to_date = lambda s: datetime.strptime(s, "%Y年%m月%d日").date()
    # Convert a date object to a string in 'YYYY-MM-DD' format.
    date_to_str = lambda d: datetime.strftime(d, "%Y-%m-%d")


    def dict_table(obj: dict):
        max_length = max(len(v) for v in obj.values())

        result = []
        for i in range(max_length):
            new_dict = {}
            for key, value_list in obj.items():
                if i < len(value_list):
                    new_dict[key] = value_list[i]
            if new_dict:  # Only add non-empty dictionaries
                result.append(new_dict)
        return result


    def parse_year(lines: list[str], pattern: str) -> str | None:
        """Extract the year from the lines using the specified regex pattern."""
        for line in lines:
            match = re.search(pattern, line)
            if match:
                return match.group(1)
        return None


    def parse_holidays(line: str, pattern: str, default_year: str) -> list(date):
        """Extract holiday dates from a line of text based on the provided pattern and year."""
        holidays = []
        for match in re.finditer(pattern, line):
            start_year = match.group(2) or default_year
            start_month, start_day = match.group(3), match.group(4)
            end_year = match.group(8) or default_year
            end_month = match.group(9) or start_month
            end_day = match.group(10) or start_day
            start_date = str_to_date(f"{start_year}年{start_month}月{start_day}日")
            end_date = str_to_date(f"{end_year}年{end_month}月{end_day}日")
            date_range = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
            holidays.extend(
                [d for d in date_range if d.weekday() < 5]
            )  # Only include weekdays
        return list(OrderedDict.fromkeys(holidays))


    def parse_compensatory_working_days(
        line: str, pattern: str, default_year: str
    ) -> list(date):
        """Extract compensatory working days from a line of text based on the provided pattern and year."""
        comp_working_days = []
        for match in re.findall(pattern, line):
            d = match[0] if len(match[1]) else f"{default_year}年{match[0]}"
            comp_working_day = str_to_date(d)
            if comp_working_day.weekday() >= 5:  # Only include weekends
                comp_working_days.append(comp_working_day)
        return list(OrderedDict.fromkeys(comp_working_days))


    def parse_holidays_comp_working_days(file: list[str], year: str) -> dict:
        """Parse the entire schedule, extracting holidays and compensatory working days."""

        schedule = {"holidays": [], "compensatory_working_days": []}

        for line in file:
            schedule["holidays"].extend(
                map(date_to_str, parse_holidays(line, HOLIDAY_PATTERN, year))
            )
            is_comp_working = re.search(HAS_COMP_WORKING_PATTERN, line)
            if is_comp_working:
                comp_days = parse_compensatory_working_days(
                    is_comp_working.group(1),
                    COMP_WORKING_DAY_PATTERN,
                    year,
                )
                schedule["compensatory_working_days"].extend(
                    map(
                        date_to_str,
                        comp_days,
                    )
                )
        return schedule
    return (
        COMP_WORKING_DAY_PATTERN,
        HAS_COMP_WORKING_PATTERN,
        HOLIDAY_PATTERN,
        OrderedDict,
        date,
        date_to_str,
        datetime,
        dict_table,
        json,
        parse_compensatory_working_days,
        parse_holidays,
        parse_holidays_comp_working_days,
        parse_year,
        re,
        str_to_date,
        timedelta,
    )


@app.cell
def unit_test(
    COMP_WORKING_DAY_PATTERN,
    HOLIDAY_PATTERN,
    date,
    parse_compensatory_working_days,
    parse_holidays,
    parse_year,
):
    assert (
        parse_year(["国务院办公厅关于2024年"], r"国务院办公厅关于(\d{4})年")
        == "2024"
    )
    assert (
        parse_year(["国务院办公厅关于202年"], r"国务院办公厅关于(\d{4})年") is None
    )

    assert parse_holidays(
        "一、元旦：2022年12月31日至2023年1月2日放假调休，共3天。",
        HOLIDAY_PATTERN,
        "2023",
    ) == [date(2023, 1, 2)]

    assert parse_holidays(
        "一、元旦：2022年12月30日至2023年1月2日放假调休，共3天。",
        HOLIDAY_PATTERN,
        "2023",
    ) == [date(2022, 12, 30), date(2023, 1, 2)]

    assert parse_compensatory_working_days(
        "2022年12月31日（星期六）、2023年1月1日（星期日）、1月1日（星期日）上班。",
        COMP_WORKING_DAY_PATTERN,
        "2023",
    ) == [date(2022, 12, 31), date(2023, 1, 1)]
    return


if __name__ == "__main__":
    app.run()
