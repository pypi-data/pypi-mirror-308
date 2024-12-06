# Standard library imports
from datetime import datetime, timedelta

from zoneinfo import ZoneInfo

# Third-party library imports
import pandas as pd
from dateutil.relativedelta import relativedelta
from IRS_toolkit.utils.constants import VALID_CONVENTIONS
from IRS_toolkit.utils.core import linear_interpolation, day_count, previous_coupon_date
# Constants
tz = ZoneInfo("Europe/Paris")


def zc_to_simplerate(zero_coupon_rate_coumpound:float, day_count:float) -> float:
    """
    Convert zero coupon rate to simple rate.

    Args:
        zero_coupon_rate_coumpound (float): Zero coupon rate (compound)
        day_count (float): Period of time in years

    Returns:
        float: Simple rate
    """
    # Return 0 if day_count is 0 or zc is None to avoid division by zero or None errors
    if day_count == 0 or zero_coupon_rate_coumpound is None:
        return 0

    # Calculate and return the simple rate
    return ((1 + zero_coupon_rate_coumpound) ** day_count - 1) / day_count


def accrued_coupon(
    curve,
    Cash_flows,
    notionel,
    valuation_date,
    ESTR_df=None,
    relative_delta=None,
) -> float:
    """This function computes the accrued coupon of the float leg
        and for the past we use ESTR compounded and for the future we compute forwards

    Args:
        curve (curve): yield curve
        ESTR (dataframe): Estr compounded
        Cash_flows (Dataframe): dataframe
        notionel (float): float
        valuation_date (datetime): valuation date

    Returns:
        float: accrued coupon
    """

    if relative_delta is None:
        relative_delta=relativedelta(days=0)

    if ESTR_df is not None:
        # if ESTR file is provided
        # we don't have weekends so we need to use interplation
        ESTR_df = ESTR_df.rename(
            columns={"dates": "date", "DATES": "date", "estr": "ESTR"}
        )
        ESTR = linear_interpolation(ESTR_df)
        date_min = min(ESTR["date"])
        date_max = max(ESTR["date"])
        SDate = previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date))
        SDate = SDate.strftime("%Y-%m-%d")

        ESTR_start = ESTR[ESTR["date"] == SDate]["ESTR"]
        ESTR_end = ESTR[ESTR["date"] == valuation_date]["ESTR"]
        ESTR_max = ESTR[ESTR["date"] == date_max]["ESTR"]
        if (
            curve.date.strftime("%Y-%m-%d") > SDate and date_max < SDate
            # Here my start Date is a Date in which no ESTR no FORWARD RATE (can't compute the forward)
        ):
            raise ValueError(
                "Forward can't be computed (ex :Use an ESTR compounded up to curve date)"
            )

        result = 0

        if SDate < date_min or SDate > date_max:
            FRate = curve.ForwardRates(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
            )
            Perf = 0 if FRate is None else (1 + FRate) ** Day_count_years - 1
        elif valuation_date <= date_max:
            Perf = (float(ESTR_end) / float(ESTR_start)) - 1
        elif valuation_date > date_max:
            perf_0 = (float(ESTR_max) / float(ESTR_start)) - 1
            FRate0 = curve.ForwardRates(
                pd.Timestamp(date_max) + timedelta(days=1),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                pd.Timestamp(date_max) + timedelta(days=1),
                pd.Timestamp(valuation_date),
            )
            Perf = ((1 + FRate0) ** (Day_count_years) - 1) + perf_0 / notionel
        else:
            FRate = curve.ForwardRates(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
                relative_delta,
            )

            Day_count_years = day_count(
                previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                pd.Timestamp(valuation_date),
            )
            Perf = 0 if FRate is None else (1 + FRate) ** Day_count_years - 1
        result = notionel * Perf
        return result

    else:
        raise ValueError("Provide an ESTR compounded xls")

def spread_amount(list_start_dates_cashflow:list[datetime], list_end_dates_cashflow:list[datetime], notionel:float, spread:float, valuation_date:datetime, convention:VALID_CONVENTIONS) -> float:
    """this function compute the spread amount for a giving valuation date and start date

    Args:
        cashflow (dataframe): coupon start and end dates
        notionel (float): notionel amount
        spread (float): swap spread
        valuation_date (datetime): valuation date

    Returns:
        float: the spread amount
    """
    period = day_count(
        previous_coupon_date(list_start_dates_cashflow, list_end_dates_cashflow, pd.Timestamp(valuation_date)),
        pd.Timestamp(valuation_date),
        convention,
    )
    return notionel * (spread) * period

def dv01(actual: float, up: float, down: float) -> float:
    """

    Args:
        actual (float): unshifted value
        up (float): value with shifted curve (+1 bps)
        down (float): value with shifted curve (-1 bps)

    Returns:
        float: sensitivity of the swap price
    """
    return (abs(actual - up) + abs(actual - down)) / 2