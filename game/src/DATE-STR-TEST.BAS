## =========================================
## DATE-STR-TEST.BAS — TEST HARNESS FOR DATESTR
## =========================================

GOTO MAIN    : REM PREVENT FALL-THROUGH AFTER BASLOAD PROCESSES SOURCE

#INCLUDE "DATE-STR-LIB.BAS"

MAIN:

    DIM AN(2), AS$(2)

    calendar_days_per_year% = CAL_MONTHS_PER_YEAR * CAL_DAYS_PER_MONTH
    calendar_weeks_per_month% = CAL_DAYS_PER_MONTH / CAL_DAYS_PER_WEEK

    PRINT "====================================="
    PRINT " DATE STRING TEST HARNESS (DATESTR)"
    PRINT "====================================="
    PRINT
    PRINT "CALENDAR CONSTANTS:"
    PRINT "  EPOCH YEAR         : "; CAL_EPOCH_YEAR
    PRINT "  MONTHS PER YEAR    : "; CAL_MONTHS_PER_YEAR
    PRINT "  DAYS PER MONTH     : "; CAL_DAYS_PER_MONTH
    PRINT "  DAYS PER WEEK      : "; CAL_DAYS_PER_WEEK
    PRINT "  WEEKS PER MONTH    : "; calendar_weeks_per_month%
    PRINT "  DAYS PER YEAR      : "; calendar_days_per_year%
    PRINT "  EPOCH WEEKDAY IDX  : "; CAL_EPOCH_WEEKDAY_INDEX
    PRINT
    PRINT "FORMATS:"
    PRINT "  "; DATE_FORMAT_FULL;       " = FULL"
    PRINT "  "; DATE_FORMAT_SHORT;      " = SHORT"
    PRINT "  "; DATE_FORMAT_ISO;        " = ISO"
    PRINT "  "; DATE_FORMAT_FULL_WDAY;  " = FULL+WDAY"
    PRINT "  "; DATE_FORMAT_SHORT_WDAY; " = SHORT+WDAY"
    PRINT
    PRINT "TEST CASES FOLLOW..."
    PRINT

    GOSUB RUN_TESTS

    PRINT
    PRINT "ALL TESTS DONE."
    END


RUN_TESTS:

    RESTORE

TEST_LOOP:

    READ day_number
    IF day_number = 0 THEN RETURN

    PRINT
    PRINT "-------------------------------------"
    PRINT "DAY NUMBER: "; day_number
    PRINT "-------------------------------------"

    FOR format_flag = DATE_FORMAT_FULL TO DATE_FORMAT_SHORT_WDAY

        AN(0) = day_number
        AN(1) = format_flag

        GOSUB DateStr
        GOSUB FORMAT_NAME_FOR_PRINT

        PRINT " F="; format_flag; " ("; format_name$; ")"
        PRINT "   DATESTR : "; AS$(0)
        PRINT "   WEEKDAY : "; AS$(1); " ("; AS$(2); ")"

    NEXT format_flag

    GOSUB WAIT_FOR_KEY
    GOTO TEST_LOOP


FORMAT_NAME_FOR_PRINT:

    format_name$ = "???"

    IF format_flag = DATE_FORMAT_FULL THEN format_name$ = "FULL"
    IF format_flag = DATE_FORMAT_SHORT THEN format_name$ = "SHORT"
    IF format_flag = DATE_FORMAT_ISO THEN format_name$ = "ISO"
    IF format_flag = DATE_FORMAT_FULL_WDAY THEN format_name$ = "FULL+WDAY"
    IF format_flag = DATE_FORMAT_SHORT_WDAY THEN format_name$ = "SHORT+WDAY"

    RETURN


WAIT_FOR_KEY:
    PRINT
    PRINT "PRESS ANY KEY TO CONTINUE..."
WAIT_LOOP:
    GET A$
    IF A$ = "" THEN GOTO WAIT_LOOP
    PRINT
    RETURN


REM ---------------------------------------
REM TEST DATA: INTERESTING DAY NUMBERS
REM 0 TERMINATES LIST
REM ---------------------------------------

TEST_DATA:
    DATA 1,2,3,4
    DATA 10,11,12,13
    DATA 27,28,29,30
    DATA 335,336,337,338
    DATA 0
