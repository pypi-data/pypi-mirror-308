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
        # Working Day Calculator

        Calculate precise dates by adding or subtracting specific working days in China, taking into account holidays and compensatory working days.
        """
    )
    return


@app.cell
def load(load_config, mo):
    config = load_config()

    start_date = mo.ui.date()
    operation = mo.ui.dropdown(options={"Add": 1, "Subtract": -1}, value="Add")
    num_days = mo.ui.text(value="0")
    return config, num_days, operation, start_date


@app.cell
def calculate(calculate_working_days, config, user_input):
    try:
        _num_days = int(user_input.value["num_days"])
        result = calculate_working_days(
            config,
            user_input.value["start_date"],
            _num_days,
            user_input.value["operation"],
        )
        if result < config.range_min or result > config.range_max:
            result = "Error: out of range"
    except Exception as e:
        result = f"Error: {e}"
    return (result,)


@app.cell
def user_input(mo, num_days, operation, start_date):
    user_input = mo.md(
        """
        | Start Date | Operation | Number of Working Days |
        | ---- | ------ | ------------ |
        |{start_date}|{operation}|{num_days}|
        """
    ).batch(
        start_date=start_date,
        operation=operation,
        num_days=num_days,
    )
    return (user_input,)


@app.cell
def response_str(date, mo, result):
    resp = mo.md(
        f"""
    | Result   |
    |----------|
    | {result.strftime("%Y-%m-%d, %A") if isinstance(result, date) else result} |
    """
    )
    return (resp,)


@app.cell
def result(mo, resp, user_input):
    mo.hstack([user_input, resp], justify="center", gap=3)
    return


@app.cell
def func_calculator(mo):
    import cn_workdays
    import os

    module_path = os.path.dirname(os.path.abspath(cn_workdays.__file__))
    config_path = os.path.join(module_path, "config.json")

    from dataclasses import dataclass
    from datetime import datetime, date, timedelta

    import json


    @dataclass
    class Config:
        holidays: list[date]
        compensatory_working_days: list[date]
        range_max: date
        range_min: date


    def load_config(file: str = config_path) -> Config:
        date_convert = lambda s: datetime.strptime(s, "%Y-%m-%d").date()

        try:
            with open(file, "r") as _f:
                data = json.load(_f)
        except FileNotFoundError:
            mo.stop(True, mo.md("**config.json does not exist.**"))
        except Exception as _e:
            mo.stop(True, mo.md(f"An error occurred: {_e}"))

        config = Config(
            # List of holidays (Monday to Friday)
            holidays=list(map(date_convert, data["holidays"])),
            # List of compensatory working days (Saturday and Sunday)
            compensatory_working_days=list(
                map(date_convert, data["compensatory_working_days"])
            ),
            range_max=date_convert(data["range_max"]),
            range_min=date_convert(data["range_min"]),
        )
        error = []

        # Check holidays for correctness
        for holiday in config.holidays:
            if not is_weekday(holiday):
                error.append(f"Error: {holiday} is not a weekday")

        # Check compensatory working days for correctness
        for working_day in config.compensatory_working_days:
            if is_weekday(working_day):
                error.append(f"Error: {working_day} is not a weekend")
        mo.stop(len(error), mo.md("\n\n".join(error)))
        return config


    def is_weekday(date_input: str | datetime | date) -> bool:
        """Check if a given date is a weekday (Monday to Friday)."""
        str_to_datetime = lambda s: datetime.strptime(s, "%Y-%m-%d").date()
        if isinstance(date_input, str):
            date_obj = str_to_datetime(date_input)
        elif isinstance(date_input, datetime | date):
            date_obj = date_input
        else:
            raise ValueError("Invalid date input")
        return date_obj.weekday() < 5


    def is_working_day(
        date_input: str | datetime | date,
        holidays: list,
        compensatory_working_days: list,
    ) -> bool:
        """Check if a given date is a working day in China, taking into account holidays and compensatory working days."""
        if is_weekday(date_input) and date_input not in holidays:
            return True
        if not is_weekday(date_input) and date_input in compensatory_working_days:
            return True
        return False


    def calculate_working_days(
        config: Config, start_date: date, num_days: int, operation: int
    ) -> date:
        count = None
        while True:
            if is_working_day(
                start_date, config.holidays, config.compensatory_working_days
            ):
                if count is None:
                    count = 0
                else:
                    count += 1
            if count == num_days:
                return start_date
            start_date = start_date + operation * timedelta(days=1)
    return (
        Config,
        calculate_working_days,
        cn_workdays,
        config_path,
        dataclass,
        date,
        datetime,
        is_weekday,
        is_working_day,
        json,
        load_config,
        module_path,
        os,
        timedelta,
    )


@app.cell
def unit_test(calculate_working_days, config, date):
    assert calculate_working_days(config, date(2024, 6, 7), 1, 1) == date(
        2024, 6, 11
    )
    assert calculate_working_days(config, date(2024, 5, 13), 1, -1) == date(
        2024, 5, 11
    )
    return


if __name__ == "__main__":
    app.run()
