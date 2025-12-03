## =========================================
## DATE-STR-LIB.BAS — DateStr library
## =========================================
## CONFIGURABLE CALENDAR CONSTANTS
## =========================================

#DEFINE CAL_EPOCH_YEAR          412
#DEFINE CAL_MONTHS_PER_YEAR     12
#DEFINE CAL_DAYS_PER_MONTH      28
#DEFINE CAL_DAYS_PER_WEEK       7

## Day 1 of the epoch year maps to this weekday index (1..CAL_DAYS_PER_WEEK)
#DEFINE CAL_EPOCH_WEEKDAY_INDEX 1

## DATE STRING FORMAT CONSTANTS
#DEFINE DATE_FORMAT_FULL         0   ## "NOVEMBER 28TH, 412"
#DEFINE DATE_FORMAT_SHORT        1   ## "NOV 28TH, 412"
#DEFINE DATE_FORMAT_ISO          2   ## "412-11-28"
#DEFINE DATE_FORMAT_FULL_WDAY    3   ## "MONDAY, NOVEMBER 28TH, 412"
#DEFINE DATE_FORMAT_SHORT_WDAY   4   ## "MON NOV 28TH, 412"

## =========================================
## SUBROUTINE: DateStr
##
## CALL:
##   AN(0) = day_number (1-based, day 1 = first day of CAL_EPOCH_YEAR)
##   AN(1) = format_flag:
##              DATE_FORMAT_FULL       (0) -> "NOVEMBER 28TH, 412"
##              DATE_FORMAT_SHORT      (1) -> "NOV 28TH, 412"
##              DATE_FORMAT_ISO        (2) -> "412-11-28"
##              DATE_FORMAT_FULL_WDAY  (3) -> "MONDAY, NOVEMBER 28TH, 412"
##              DATE_FORMAT_SHORT_WDAY (4) -> "MON NOV 28TH, 412"
##
## RETURNS:
##   AS$(0) = formatted date string
##   AS$(1) = weekday full name  (e.g. "MONDAY")
##   AS$(2) = weekday short name (e.g. "MON")
## =========================================

DateStr:

    IF date_tables_initialized_flag% = 0 THEN GOSUB Init_Date_Tables

    calendar_day_index = AN(0) - 1
    IF calendar_day_index < 0 THEN calendar_day_index = 0

    format_flag = INT(AN(1))
    IF format_flag < DATE_FORMAT_FULL THEN format_flag = DATE_FORMAT_FULL
    IF format_flag > DATE_FORMAT_SHORT_WDAY THEN format_flag = DATE_FORMAT_FULL

    calendar_days_per_year% = CAL_MONTHS_PER_YEAR * CAL_DAYS_PER_MONTH

    year_offset% = INT(calendar_day_index / calendar_days_per_year%)
    year_number = CAL_EPOCH_YEAR + year_offset%
    calendar_day_index = calendar_day_index - year_offset% * calendar_days_per_year%

    month_index% = INT(calendar_day_index / CAL_DAYS_PER_MONTH) + 1
    IF month_index% < 1 THEN month_index% = 1
    IF month_index% > CAL_MONTHS_PER_YEAR THEN month_index% = CAL_MONTHS_PER_YEAR

    day_of_month% = INT(calendar_day_index - (month_index% - 1) * CAL_DAYS_PER_MONTH) + 1
    IF day_of_month% < 1 THEN day_of_month% = 1
    IF day_of_month% > CAL_DAYS_PER_MONTH THEN day_of_month% = CAL_DAYS_PER_MONTH

    day_string$ = MID$(STR$(day_of_month%), 2)

    day_suffix$ = "TH"
    day_ones_digit% = day_of_month% - INT(day_of_month% / 10) * 10
    day_last_two_digits% = day_of_month% - INT(day_of_month% / 100) * 100

    IF day_last_two_digits% > 10 AND day_last_two_digits% < 14 THEN GOTO Skip_Ordinal_Suffix

    IF day_ones_digit% = 1 THEN day_suffix$ = "ST"
    IF day_ones_digit% = 2 THEN day_suffix$ = "ND"
    IF day_ones_digit% = 3 THEN day_suffix$ = "RD"

Skip_Ordinal_Suffix:

    year_string$ = MID$(STR$(year_number), 2)

    REM ----- DAY OF WEEK CALCULATION -----
    temp_weekday_index% = calendar_day_index + CAL_EPOCH_WEEKDAY_INDEX - 1
    temp_weekday_index% = temp_weekday_index% - INT(temp_weekday_index% / CAL_DAYS_PER_WEEK) * CAL_DAYS_PER_WEEK
    weekday_index% = temp_weekday_index% + 1

    weekday_full_string$  = weekday_full_name$(weekday_index%)
    weekday_short_string$ = weekday_short_name$(weekday_index%)

    AS$(1) = weekday_full_string$
    AS$(2) = weekday_short_string$

    IF format_flag = DATE_FORMAT_FULL THEN GOSUB Format_Full_Month : RETURN
    IF format_flag = DATE_FORMAT_SHORT THEN GOSUB Format_Short_Month : RETURN
    IF format_flag = DATE_FORMAT_ISO THEN GOSUB Format_Iso_Numeric : RETURN
    IF format_flag = DATE_FORMAT_FULL_WDAY THEN GOSUB Format_Full_Month_With_Weekday : RETURN
    IF format_flag = DATE_FORMAT_SHORT_WDAY THEN GOSUB Format_Short_Month_With_Weekday : RETURN

    REM Fallback, should never hit:
    GOSUB Format_Full_Month
    RETURN


Format_Full_Month:
    REM FORMAT: "NOVEMBER 28TH, 412"
    AS$(0) = month_full_name$(month_index%) + " " + day_string$ + day_suffix$ + ", " + year_string$
    RETURN


Format_Short_Month:
    REM FORMAT: "NOV 28TH, 412"
    AS$(0) = month_short_name$(month_index%) + " " + day_string$ + day_suffix$ + ", " + year_string$
    RETURN


Format_Iso_Numeric:
    REM FORMAT: "412-11-28"

    month_numeric_string$ = MID$(STR$(month_index%), 2)
    IF month_index% < 10 THEN month_numeric_string$ = "0" + month_numeric_string$

    day_numeric_string$ = day_string$
    IF day_of_month% < 10 THEN day_numeric_string$ = "0" + day_numeric_string$

    AS$(0) = year_string$ + "-" + month_numeric_string$ + "-" + day_numeric_string$
    RETURN


Format_Full_Month_With_Weekday:
    REM FORMAT: "MONDAY, NOVEMBER 28TH, 412"
    AS$(0) = weekday_full_string$ + ", " + month_full_name$(month_index%) + " " + day_string$ + day_suffix$ + ", " + year_string$
    RETURN


Format_Short_Month_With_Weekday:
    REM FORMAT: "MON NOV 28TH, 412"
    AS$(0) = weekday_short_string$ + " " + month_short_name$(month_index%) + " " + day_string$ + day_suffix$ + ", " + year_string$
    RETURN


Init_Date_Tables:
    REM ONE-TIME INIT: MONTH AND WEEKDAY NAME TABLES

    DIM month_full_name$(CAL_MONTHS_PER_YEAR), month_short_name$(CAL_MONTHS_PER_YEAR)
    DIM weekday_full_name$(CAL_DAYS_PER_WEEK), weekday_short_name$(CAL_DAYS_PER_WEEK)

    date_tables_initialized_flag% = 1

    month_full_name$(1) = "JANUARY"
    month_full_name$(2) = "FEBRUARY"
    month_full_name$(3) = "MARCH"
    month_full_name$(4) = "APRIL"
    month_full_name$(5) = "MAY"
    month_full_name$(6) = "JUNE"
    month_full_name$(7) = "JULY"
    month_full_name$(8) = "AUGUST"
    month_full_name$(9) = "SEPTEMBER"
    month_full_name$(10) = "OCTOBER"
    month_full_name$(11) = "NOVEMBER"
    month_full_name$(12) = "DECEMBER"

    month_short_name$(1) = "JAN"
    month_short_name$(2) = "FEB"
    month_short_name$(3) = "MAR"
    month_short_name$(4) = "APR"
    month_short_name$(5) = "MAY"
    month_short_name$(6) = "JUN"
    month_short_name$(7) = "JUL"
    month_short_name$(8) = "AUG"
    month_short_name$(9) = "SEP"
    month_short_name$(10) = "OCT"
    month_short_name$(11) = "NOV"
    month_short_name$(12) = "DEC"

    weekday_full_name$(1) = "MONDAY"
    weekday_full_name$(2) = "TUESDAY"
    weekday_full_name$(3) = "WEDNESDAY"
    weekday_full_name$(4) = "THURSDAY"
    weekday_full_name$(5) = "FRIDAY"
    weekday_full_name$(6) = "SATURDAY"
    weekday_full_name$(7) = "SUNDAY"

    weekday_short_name$(1) = "MON"
    weekday_short_name$(2) = "TUE"
    weekday_short_name$(3) = "WED"
    weekday_short_name$(4) = "THU"
    weekday_short_name$(5) = "FRI"
    weekday_short_name$(6) = "SAT"
    weekday_short_name$(7) = "SUN"

    RETURN
