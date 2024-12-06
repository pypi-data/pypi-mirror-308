# Standard library imports
import warnings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Third-party imports
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

# Local/application imports
from IRS_toolkit.utils import core,financial
from IRS_toolkit.utils.constants import VALID_COUPON_FREQUENCY,VALID_TENORS,VALID_CONVENTIONS,pay_frequency

# Configure warnings
warnings.filterwarnings("ignore")


class Curve:
    """
       A class for handling yield curves used in pricing and preparing
    zero-coupon curves for cash flow computation and discounting.
        Args:
               curve (dataframe): dataframe
               date_curve (date): date curve

        Attributs:
                date : curve date
                df : a dataframe that contains dates and ZC rates and Dfs

        Functions:
                setup() : create the dataframe and interpolate rate
                ForwardRate(begin,end) : compute the forward rate for two giving dates
                Bootstrap() : compute the ZC curve using the formula refer to notion appendix
                monthly_avg_daily() : compute the monthly average of instantaneous forward rates  using spot ZC curve


    """

    def __init__(self, curve=None, date_curve=None, snowflake_instance=None,date_format="%Y-%m-%d"):
        self.date_format = date_format

        self.snowflake_instance = snowflake_instance

        if date_curve is None:
            self.date = datetime.now(tz=ZoneInfo("Europe/Paris"))
        else:
            self.date = datetime.strptime(date_curve, date_format)

        self.curve = curve

        self.df = self.curve.copy()
        self.interpolated_yield_curve = None
        """    def set_periodicity(self, period):
        self.periodicity = period"""
        self.setup()

    def setup(self):
        Dates = []
        list_tenor = self.curve.iloc[:, 0].tolist()
        for tenor in list_tenor:
            Dates.append(self.date + core.tenor_to_period(tenor))
        self.df["Date"] = Dates

        self.df.loc[-1] = ["0D", np.nan, self.date]  # adding a row
        self.df.index = self.df.index + 1  # shifting index
        self.df.sort_index(inplace=True)

        self.df.rename(columns={"Rate": "StrippedRates"}, inplace=True)
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: core.day_count(self.date, x["Date"]), axis=1
        )

    def interpolate_yield_curve(self):
        curve_data_ = self.curve.copy()
        curve_data_["relativedelta"] = curve_data_["Tenor"].apply(
            lambda x: core.tenor_to_period(x)
        )

        now = self.date

        curve_data_["relative_date"] = curve_data_["relativedelta"].apply(
            lambda x: (now + x)
        )
        curve_data_["Period"] = curve_data_["relative_date"].apply(
            lambda x: (x - now).days
        )

        df = pd.DataFrame({"Period": np.arange(1, max(curve_data_["Period"]) + 1, 1)})
        curve_data_ = df.merge(curve_data_, "left")
        curve_data_["Rate"] = curve_data_["Rate"].astype(float)
        curve_data_["Rate"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        curve_data_["Date"] = curve_data_["Period"].apply(lambda x: now + timedelta(x))
        curve_data_["day_count"] = curve_data_.apply(
            lambda x: core.day_count(self.date, x["Date"]), axis=1
        )

        curve_data_.loc[-1] = [
            0,
            "0D",
            np.nan,
            relativedelta(months=0),
            self.date,
            self.date,
            0,
        ]  # adding a row
        curve_data_.index = curve_data_.index + 1  # shifting index
        curve_data_.sort_index(inplace=True)
        curve_data_.reset_index(drop=True, inplace=True)
        curve_data_.rename(columns={"Rate": "StrippedRates"}, inplace=True)
        curve_data_ = curve_data_[
            ["day_count", "StrippedRates", "Date", "Period", "Tenor"]
        ]
        self.interpolated_yield_curve = curve_data_

    def forward_rates(
        self,
        begin:datetime,
        end:datetime,
        relative_delta=None,
        date_convention:VALID_CONVENTIONS="ACT/360",
        date_format="%Y-%m-%d",
    ):
        """
        compute forward rates

        Args:
            begin (date): start date
            end (date): end date

        Returns:
            float: forward rate
        """

        if relative_delta is None:
            relative_delta=relativedelta(days=0)

        try:
            # Convert string dates to datetime, if necessary
            begin_date = datetime.strptime(begin, date_format) if isinstance(begin, str) else begin
            end_date = datetime.strptime(end, date_format) if isinstance(end, str) else end
            end_date = end_date + relative_delta

            # Validation of date ranges
            if end_date < self.date or begin_date >= end_date:
                return None

            # Extract zero-coupon rates for the given dates
            zc_begin = self.df[self.df["Date"] == begin_date.strftime("%Y-%m-%d")]["ZC"]
            zc_end = self.df[self.df["Date"] == end_date.strftime("%Y-%m-%d")]["ZC"]

            if zc_begin.empty:
                return None  # Return None if no ZC rates found for the dates
            if zc_end.empty:
                return None  # Return None if no ZC rates found for the dates

            # Calculate discount factors (DF)
            num = (1 + zc_end.iloc[0]) ** core.day_count(self.date, end_date)
            den = (1 + zc_begin.iloc[0]) ** core.day_count(self.date, begin_date)
            result = (num / den) ** (
                1.0 / core.day_count(begin_date, end_date, date_convention)
            ) - 1

            # Compute forward rate using the formula (DF2/DF1)^(1/delta(t)) - 1
            return result

        except Exception as e:
            print(f"An error occurred while calculating forward rates: {e}")
            return None  # Return a default value or None

    def bootstrap(
        self, coupon_frequency:VALID_COUPON_FREQUENCY, date_convention:VALID_CONVENTIONS, zc_curve=None
    ):
        """
        It Transform the yield curve to a zero-coupon (ZC) curve.

        This function processes the initial curve data to compute zero-coupon rates and discount factors.
        It handles different date calculations based on whether the current day is the first of the month.
        """
        if zc_curve is None:
            zc_curve = self.df.copy()

        coupon_periods = pay_frequency[coupon_frequency]*30
        coupon_frequency_date = pay_frequency[coupon_frequency]

        zc_date = [
            self.date + relativedelta(months=i * coupon_frequency_date)
            for i in range(coupon_periods + 1)
        ]
        zc_curve_before = zc_curve[zc_curve["Date"] < zc_date[1]]
        zc_curve_before["Period"] = (zc_curve_before["Date"] - self.date).apply(
            lambda x: x.days
        )

        zc_curve_before["Coupon_period"] = zc_curve_before["day_count"]

        zc_curve_before["ZC"] = (
            1 + zc_curve_before["StrippedRates"] * zc_curve_before["Coupon_period"]
        ) ** (1 / zc_curve_before["Coupon_period"]) - 1
        zc_curve_before["DF"] = (
            1 / (1 + zc_curve_before["ZC"]) ** (zc_curve_before["Coupon_period"])
        )

        zc_curve_temp = zc_curve[zc_curve["Date"].isin(zc_date[1:])]
        zc_curve_temp.reset_index(drop=True, inplace=True)
        zc_curve_temp["Date_lagg"] = zc_curve_temp["Date"].shift()
        zc_curve_temp["Date_lagg"].fillna(self.date, inplace=True)
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: core.day_count(x["Date_lagg"], x["Date"], date_convention), axis=1
        )
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["StrippedRates"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["StrippedRates"][i] * zc_curve_temp["Coupon_period"][i]
            )
        zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
            1 / zc_curve_temp["day_count"]
        ) - 1

        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)
        self.df = zc_curve.merge(zc_curve.dropna(), "left")
        dates = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=self.date,
                    end=self.date + relativedelta(years=30),
                    freq="D",
                ),
            }
        )

        self.df = dates.merge(zc_curve, "left")
        self.df["DF"] = self.df["DF"].astype(float)
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: core.day_count(self.date, x["Date"], date_convention), axis=1
        )
        self.df["ZC"] = (1 / self.df["DF"]) ** (1 / self.df["day_count"]) - 1
        self.df["StrippedRates"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df.at[0, "DF"] = 1
        self.df.at[0, "Coupon_period"] = 0

    def monthly_avg_daily(
        self, start_date:datetime, end_date:datetime, frequency:str="D", relative_delta=None,date_format="%Y-%m-%d"
    ):
        """

        Args:
            start_date (date): start date
            end_date (date): end date

        Returns:
            Dataframe: Monthly average of daily forward rates
        """
        if relative_delta is None:
            relative_delta=relativedelta(days=0)

        if frequency == "Between Tenor":
            date_list = []
            for tenor in VALID_TENORS:
                date_forward = datetime.strptime(start_date, date_format) + core.tenor_to_period(tenor)
                date_list.append(date_forward)
        else:
            date_list = pd.date_range(start_date, end=end_date, freq=frequency)

        foreward_df = pd.DataFrame([date_list[:-1], date_list[1:]]).T
        foreward_df.columns = ["start_date", "end_date"]
        foreward_list = []
        for i, j in zip(date_list[:-1], date_list[1:]):
            foreward_list.append(self.ForwardRates(i, j, relative_delta))
        foreward_df["foreward_ZC"] = foreward_list
        foreward_df["day_count"] = foreward_df.apply(
            lambda x: core.day_count(x["start_date"], x["end_date"]), axis=1
        )
        foreward_df["foreward_simple"] = foreward_df.apply(
            lambda x: core.ZC_to_simplerate(x["foreward_ZC"], x["day_count"]), axis=1
        )

        foreward_df = foreward_df.set_index("start_date")
        foreward_df.index = pd.to_datetime(foreward_df.index)

        return foreward_df.groupby(pd.Grouper(freq="M")).mean(), foreward_df

    def bootstrap_12m_semi_yearly_coupon(self, coupon_frequency:VALID_COUPON_FREQUENCY):
        """
        Transform the yield curve to a zero-coupon (ZC) curve.

        This function processes the initial curve data to compute zero-coupon rates and discount factors.
        It handles different date calculations based on whether the current day is the first of the month.
        """
        zc_curve = self.df.copy()

        coupon_periods = {
            "quarterly": 29 * 4,
            "yearly": 29,
            "monthly": 29 * 12,
            "semi_annual": 29 * 2,
        }[coupon_frequency]
        coupon_frequency_date = {
            "quarterly": pd.DateOffset(months=3),  # "3MS",
            "yearly": pd.DateOffset(years=1),
            "monthly": pd.DateOffset(months=1),
            "semi_annual": pd.DateOffset(months=6),
        }[coupon_frequency]

        # if self.date.day == 1:
        zc_date1 = pd.date_range(
            self.date.strftime(self.date_format),
            periods=2,
            freq=pd.DateOffset(months=6),
        )

        zc_date2 = pd.date_range(
            (self.date + pd.DateOffset(years=1)).strftime(self.date_format),
            periods=coupon_periods,
            freq=coupon_frequency_date,
        )

        zc_date = zc_date1.append(zc_date2)

        zc_curve_before = zc_curve[zc_curve["Date"] < zc_date[1]]
        zc_curve_before["Period"] = (zc_curve_before["Date"] - self.date).apply(
            lambda x: x.days
        )

        zc_curve_before["Coupon_period"] = zc_curve_before["day_count"]

        zc_curve_before["ZC"] = (
            1 + zc_curve_before["StrippedRates"] * zc_curve_before["Coupon_period"]
        ) ** (1 / zc_curve_before["Coupon_period"]) - 1
        zc_curve_before["DF"] = (
            1 / (1 + zc_curve_before["ZC"]) ** (zc_curve_before["Coupon_period"])
        )

        zc_curve_temp = zc_curve[zc_curve["Date"].isin(zc_date)]
        zc_curve_temp.reset_index(drop=True, inplace=True)
        zc_curve_temp["Date_lagg"] = zc_curve_temp["Date"].shift()
        zc_curve_temp["Date_lagg"].fillna(self.date, inplace=True)
        zc_curve_temp["Coupon_period"] = zc_curve_temp.apply(
            lambda x: core.day_count(x["Date_lagg"], x["Date"]), axis=1
        )
        zc_curve_temp["DF"] = 1
        for i in range(zc_curve_temp.shape[0]):
            zc_curve_temp.loc[i, "DF"] = (
                1
                - (
                    zc_curve_temp["StrippedRates"][i]
                    * zc_curve_temp["Coupon_period"]
                    * zc_curve_temp["DF"]
                )[:i].sum()
            ) / (
                1
                + zc_curve_temp["StrippedRates"][i] * zc_curve_temp["Coupon_period"][i]
            )
        zc_curve_temp["ZC"] = (1 / zc_curve_temp["DF"]) ** (
            1 / zc_curve_temp["day_count"]
        ) - 1
        zc_curve = pd.concat([zc_curve_before, zc_curve_temp[zc_curve_before.columns]])
        zc_curve.reset_index(inplace=True, drop=True)
        self.df = self.df.merge(zc_curve.dropna(), "left")
        dates = pd.DataFrame(
            {
                "Date": pd.date_range(
                    start=self.date + relativedelta(days=1),
                    end=self.date + relativedelta(years=30),
                    freq="D",
                ),
            }
        )

        self.df = dates.merge(self.df, "left")
        self.df["DF"] = self.df["DF"].astype(float)
        self.df["DF"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )
        self.df["Period"] = (self.df["Date"] - self.date).apply(lambda x: x.days)
        self.df["day_count"] = self.df.apply(
            lambda x: core.day_count(self.date, x["Date"]), axis=1
        )
        self.df["ZC"] = (1 / self.df["DF"]) ** (1 / self.df["day_count"]) - 1
        self.df["StrippedRates"].interpolate(
            method="cubic", inplace=True, limit_direction="forward"
        )

    def accrued_coupon(
    curve,
    Cash_flows,
    notionel:float,
    valuation_date:datetime,
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
            ESTR = financial.linear_interpolation(ESTR_df)
            date_min = min(ESTR["date"])
            date_max = max(ESTR["date"])
            SDate = financial.previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date))
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
                    financial.previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                    pd.Timestamp(valuation_date),
                    relative_delta,
                )

                Day_count_years = core.day_count(
                    financial.previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
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

                Day_count_years = core.day_count(
                    pd.Timestamp(date_max) + timedelta(days=1),
                    pd.Timestamp(valuation_date),
                )
                Perf = ((1 + FRate0) ** (Day_count_years) - 1) + perf_0 / notionel
            else:
                FRate = curve.ForwardRates(
                    financial.previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                    pd.Timestamp(valuation_date),
                    relative_delta,
                )

                Day_count_years = core.day_count(
                    financial.previous_coupon_date(Cash_flows, pd.Timestamp(valuation_date)),
                    pd.Timestamp(valuation_date),
                )
                Perf = 0 if FRate is None else (1 + FRate) ** Day_count_years - 1
            result = notionel * Perf
            return result

        else:
            raise ValueError("Provide an ESTR compounded xls")
