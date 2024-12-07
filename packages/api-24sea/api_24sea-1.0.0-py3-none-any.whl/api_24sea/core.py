# -*- coding: utf-8 -*-
"""The core module for the datasignals package
"""

import datetime
import logging
import os
from typing import Dict, List, Optional, Union
from warnings import simplefilter

import pandas as pd
import requests as req
from pydantic import validate_call

# Local imports
from . import exceptions as E
from . import utils as U
from .datasignals import schemas as S

try:
    # delete the accessor to avoid warning
    del pd.DataFrame.datasignals
except AttributeError:
    pass

# This filter is used to ignore the PerformanceWarning that is raised when
# the DataFrame is modified in place. This is the case when we add columns
# to the DataFrame in the get_data method.
# This is the only way to update the DataFrame in place when using accessors
# and performance is not an issue in this case.
# See https://stackoverflow.com/a/76306267/7169710 for reference.
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

logging.basicConfig(format="%(message)s", level=logging.INFO)


class API:
    """Accessor for working with data signals coming from the 24SEA API."""

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None
    ):
        self.base_url: str = f"{U.BASE_URL}datasignals/"
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.auth: Optional[req.auth.HTTPBasicAuth] = None
        self.authenticated: bool = False
        self.metrics_overview: Optional[pd.DataFrame] = None

        if self.username and self.password:
            self.authenticate(self.username, self.password)
        else:
            self._auto_authenticate

    @property
    def _auto_authenticate(self):
        """Automatically authenticate using environment variables if available."""
        username = os.getenv("24SEA_API_USERNAME")
        password = os.getenv("24SEA_API_PASSWORD")
        if username and password:
            self.authenticate(username, password)

    @validate_call
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate the user with the 24SEA API. Additionally, define
        the ``metrics_overview`` dataframe.

        Parameters
        ----------
        username : str
            The username to authenticate.
        password : str
            The password to authenticate.

        Returns
        -------
        bool
            True if the authentication was successful, otherwise False.
        """
        # -- Step 1: Authenticate and check the credentials
        self.username = username
        self.password = password
        self.auth = req.auth.HTTPBasicAuth(self.username, self.password)
        # fmt: off
        try:
            r_profile = U.handle_request(
                f"{self.base_url}profile",
                {"username": self.username},
                self.auth,
                {"accept": "application/json"},
            )
            if r_profile.ok:
                self.authenticated = True
            logging.info("\033[32;1mThis dataframe has now access to https://api.24sea.eu/.\033[0m")  # noqa: E501  # pylint: disable=C0301
        except req.exceptions.HTTPError:
            raise E.AuthenticationError("\033[31;1mThe username and/or password are incorrect.\033[0m")  # noqa: E501  # pylint: disable=C0301
        # fmt: on
        # -- Step 2: Define the metrics_overview dataframe
        if self.metrics_overview is not None:
            return self.authenticated
        logging.info("Now getting your metrics_overview table...")
        r_metrics = U.handle_request(
            f"{self.base_url}metrics",
            {"project": None, "locations": None, "metrics": None},
            self.auth,
            {"accept": "application/json"},
        )
        # fmt: off
        if not isinstance(r_metrics, type(None)):
            try:
                m_ = pd.DataFrame(r_metrics.json())
            except Exception:
                raise E.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                     f"\n {r_profile.json()}")
        if m_.empty:
            raise E.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                 f"\n {r_profile.json()}")
        try:
            s_ = m_.apply(lambda x: x["metric"]
                          .replace(x["statistic"], "")
                         .replace(x["short_hand"], "")
                         .strip(), axis=1).str.strip("_").str.split("_", expand=True)  # noqa: E501  # pylint: disable=C0301
            # Just take the first two columns to avoid duplicates
            s_ = s_.iloc[:, :2]
            s_.columns = ["site_id", "location_id"]
        # fmt: on
        except Exception:
            self.metrics_overview = m_
        self.metrics_overview = pd.concat([m_, s_], axis=1)
        return self.authenticated

    @U.check_authentication
    @validate_call
    def get_metrics(
        self,
        site: Optional[str] = None,
        locations: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[List[Dict[str, Optional[str]]]]:
        """
        Get the metrics names for a site, provided the following parameters.

        Parameters
        ----------
        site : Optional[str]
            The site name. If None, the queryable metrics for all sites
            will be returned, and the locations and metrics parameters will be
            ignored.
        locations : Optional[Union[str, List[str]]]
            The locations for which to get the metrics. If None, all locations
            will be considered.
        metrics : Optional[Union[str, List[str]]]
            The metrics to get. They can be specified as regular expressions.
            If None, all metrics will be considered.

            For example:

            * | ``metrics=["^ACC", "^DEM"]`` will return all the metrics that
              | start with ACC or DEM,
            * Similarly, ``metrics=["windspeed$", "winddirection$"]`` will
              | return all the metrics that end with windspeed and
              | winddirection,
            * and ``metrics=[".*WF_A01.*",".*WF_A02.*"]`` will return all
              | metrics that contain WF_A01 or WF_A02.

        Returns
        -------
        Optional[List[Dict[str, Optional[str]]]]
            The metrics names for the given site, locations and metrics.

        .. note::
            This class method is legacy because it does not add functionality to
            the DataSignals pandas accessor.

        """
        url = f"{self.base_url}metrics"
        # fmt: on
        if headers is None:
            headers = {"accept": "application/json"}
        if site is None:
            params = {}
        if isinstance(locations, List):
            locations = ",".join(locations)
        if isinstance(metrics, List):
            metrics = ",".join(metrics)
        params = {
            "project": site,
            "locations": locations,
            "metrics": metrics,
        }

        r_ = U.handle_request(url, params, self.auth, headers)

        # Set the return type of the get_metrics method to the Metrics schema
        return r_.json()  # type: ignore

    @U.check_authentication
    def selected_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return the selected metrics for the query."""
        if self.metrics_overview is None:
            raise E.ProfileError(
                "\033[31mThe metrics overview is empty. Please authenticate "
                "first with the \033[1mauthenticate\033[22m method."
            )
        if data.empty:
            raise E.DataSignalsError(
                "\033[31mThe \033[1mselected_metrics\033[22m method can only "
                "be called if the DataFrame is not empty, or after the "
                "\033[1mget_data\033[22m method has been called."
            )
        # Get the selected metrics as the Data columns that are available
        # in the metrics_overview DataFrame
        return self.metrics_overview[
            self.metrics_overview["metric"].isin(data.columns)
        ].set_index("metric")

    @U.check_authentication
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def get_data(
        self,
        sites: Optional[Union[List, str]],
        locations: Optional[Union[List, str]],
        metrics: Union[List, str],
        start_timestamp: Union[str, datetime.datetime],
        end_timestamp: Union[str, datetime.datetime],
        outer_join_on_timestamp: bool = False,
        headers: Optional[Union[Dict[str, str]]] = None,
        data: Optional[pd.DataFrame] = None,
        as_dict: bool = False,
        normalize: bool = False,
        keep_stat_in_metric_name: bool = False,
    ) -> Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]:
        """Get the data signals from the 24SEA API.

        Parameters
        ----------
        sites : Optional[Union[List, str]]
            The site name or List of site names. If None, the site will be
            inferred from the metrics.
        locations : Optional[Union[List, str]]
            The location name or List of location names. If None, the location
            will be inferred from the metrics.
        metrics : Union[List, str]
            The metric name or List of metric names. It must be provided.
            They do not have to be the entire metric name, but can be a part
            of it. For example, if the metric name is
            ``"mean_WF_A01_windspeed"``, the user can equivalently provide
            ``sites="wf"``, ``locations="a01"``, ``metric="mean windspeed"``.
        start_timestamp : Union[str, datetime.datetime]
            The start timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        end_timestamp : Union[str, datetime.datetime]
            The end timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        outer_join_on_timestamp : bool, optional
            If True, the data will be joined on the timestamp which will be the
            index of the DataFrame. If False, the data will be concatenated
            without any join. Default is False.
        headers : Optional[Union[Dict[str, str]]], optional
            The headers to pass to the request. If None, the default headers
            will be used as ``{"accept": "application/json"}``. Default is None.
        data : pd.DataFrame
            The DataFrame to update with the data signals. If None, a new
            DataFrame will be created. Default is None.
        as_dict : bool, optional
            If True, the data will be returned as a list of dictionaries.
            Default is False.
        normalize : bool, optional
            If True, the data will be normalized based on the metrics overview.
            Default is False.
        keep_stat_in_metric_name : bool, optional
            If True, the statistic will be prepended to the metric name.
            Default is False.

        Returns
        -------
        pd.DataFrame
            The DataFrame containing the data signals.
        """
        if data is None:
            data = pd.DataFrame()
        # Clean the DataFrame
        data_ = pd.DataFrame()
        # -- Step 1: Build the query object from GetData
        query = S.GetData(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            sites=sites,
            locations=locations,
            metrics=metrics,
            headers=headers,
            outer_join_on_timestamp=outer_join_on_timestamp,
            as_dict=as_dict,
            normalize=normalize,
            keep_stat_in_metric_name=keep_stat_in_metric_name,
        )

        if query.sites is None and query.locations is None:
            query_str = (
                "metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.sites is None and query.locations is not None:
            query_str = (
                "(location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.locations is None and query.sites is not None:
            query_str = (
                "(site.str.lower() == @query.sites or site_id.str.lower() == @query.sites) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        else:
            query_str = (
                "(site_id.str.lower() == @query.sites or site.str.lower() == @query.sites) "
                "and (location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )

        nl = "\n"
        l_ = f"\033[30;1mQuery:\033[0;34m {query_str.replace(' and ', f'{nl}       and ')}\n"
        logging.info(l_)

        self._selected_metrics = self.metrics_overview.query(query_str).pipe(  # type: ignore  # noqa: E501  # pylint: disable=E501
            lambda df: df.sort_values(
                ["site", "location", "data_group", "short_hand", "statistic"],
                ascending=[True, True, False, True, True],
            )
        )
        logging.info("\033[32;1mMetrics selected for the query:\033[0m\n")
        # fmt: off
        logging.info(self._selected_metrics[["metric", "unit_str", "site",
                                             "location"]])
        # fmt: on
        data_frames = []
        grouped_metrics = self._selected_metrics.groupby(["site", "location"])

        # return grouped_metrics
        logging.info(
            f"\n\033[32;1mRequested time range:\033[0;34m "
            f"From {str(query.start_timestamp)[:-4].replace('T', ' ')} UTC "
            f"To {str(query.end_timestamp)[:-4].replace('T', ' ')} UTC\n\033[0m"
        )
        import concurrent.futures

        def fetch_data(site, location, group):
            # fmt: off
            s_ = "• " + ",".join(group["metric"].tolist()).replace(",", "\n           • ")  # noqa: E501  # pylint: disable=C0301
            logging.info(f"\033[32;1m\033[32;1m⏳ Getting data for {site} - "
                         f"{location}...\n  Metrics: \033[0;34m{s_}\n\033[0m")
            # fmt: on
            r_ = U.handle_request(
                f"{self.base_url}data",
                {
                    "start_timestamp": query.start_timestamp,
                    "end_timestamp": query.end_timestamp,
                    "project": [site],
                    "location": [location],
                    "metrics": ",".join(group["metric"].tolist()),
                },
                self.auth,
                query.headers,
            )
            # Warn if empty
            if r_.json() == []:
                logging.warning(
                    f"\033[33;1mNo data found for {site} - {location}.\033[0m"
                )
            return pd.DataFrame(r_.json())

        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            # fmt: off
            future_to_data = {
                executor.submit(fetch_data,
                                site,
                                location,
                                group): (site, location)
                for (site, location), group in grouped_metrics
            }
            # fmt: on
            for future in concurrent.futures.as_completed(future_to_data):
                data_frames.append(future.result())
            # data_frames.append(pd.DataFrame(r_.json()))

        # if left_join_on_timestamp is True, lose the location and site columns
        # and join on timestamp
        if outer_join_on_timestamp:
            for i, df in enumerate(data_frames):
                if df.empty:
                    continue
                data_frames[i] = df.set_index("timestamp")
                data_frames[i].index = pd.to_datetime(data_frames[i].index)
                # drop site and location
                if "site" in data_frames[i].columns:
                    data_frames[i].drop(["site"], axis=1, inplace=True)
                if "location" in data_frames[i].columns:
                    data_frames[i].drop(["location"], axis=1, inplace=True)
            data_ = pd.concat([data_] + data_frames, axis=1, join="outer")
        else:
            data_ = pd.concat([data_] + data_frames, ignore_index=True)

        logging.info("\033[32;1m✔️ Data successfully retrieved.\033[0m")
        logging.info(
            "Your \033[30;1mpandas DataFrame\033[0m has been updated with the "
            "queried data."
        )
        data.drop(data.index, inplace=True)
        for col in data_.columns:
            if col in data.columns:
                del data[col]
            data[col] = data_[col]
            del data_[col]
        if as_dict:
            if normalize:
                return normalize_data(
                    data, self.metrics_overview, keep_stat_in_metric_name
                ).to_dict("records")
            return data.reset_index().to_dict("records")
        if normalize:
            return normalize_data(data, self.metrics_overview)
        return data


def normalize_data(
    data: Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]],
    metrics_overview: pd.DataFrame,
    keep_stat_in_metric_name: bool = False,
) -> pd.DataFrame:
    """
    Normalize the given data based on the metrics overview.

    Parameters
    ----------
    data : Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]
        The data to be normalized. It can be either a DataFrame or a dictionary of DataFrames.
    metrics_overview : pd.DataFrame
        A DataFrame containing the information about the metrics.
    keep_stat_in_metric_name : bool, optional
        Whether to keep the statistic in the metric name, by default True.

    Returns
    -------
    Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]
        The normalized data.

    Notes
    -----
    The function performs the following steps:
    1. Transforms the data dictionary into a DataFrame if necessary.
    2. Resets the index and converts the timestamp column to datetime.
    3. Melts the data to long format.
    4. Merges the melted data with the metrics overview DataFrame.
    5. Renames columns for consistency.
    6. Extracts latitude and heading information from the metric names.
    7. Extracts sub-assembly information from the metric names.
    8. Reorders the columns.
    9. Optionally appends the statistic to the metric name.
    10. Drops the rows where the metric name is "index", "site" or "location".

    Example
    -------
    >>> import pandas as pd
    >>> from typing import Union, Dict
    >>> data = {
    ...     'timestamp': ['2021-01-01', '2021-01-02'],
    ...     'mean_WF_A01_TP_SG_LAT005_DEG000': [1.0, 1.1],
    ...     'mean_WF_A02_TP_SG_LAT005_DEG000': [2.0, 2.1]
    ... }
    >>> metrics_overview = pd.DataFrame({
    ...     'metric': ['mean_WF_A01_TP_SG_LAT005_DEG000',
    ...                'mean_WF_A02_TP_SG_LAT005_DEG000'],
    ...     'short_hand': ['TP_SG_LAT005_DEG000', 'TP_SG_LAT005_DEG000'],
    ...     'statistic': ['mean', 'mean'],
    ...     'unit': ['unit', 'unit'],
    ...     'site': ['WindFarm', 'WindFarm'],
    ...     'location': ['WFA01', 'WFA02'],
    ...     'data_group': ['SG', 'SG'],
    ...     'site_id': ['WF', 'WF'],
    ...     'location_id': ['A01', 'A02']
    ... })
    >>> normalized = normalize_data(data, metrics_overview)
    >>> normalized
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | timestamp  | full_metric_name               | value | unit | statistic | short_hand          | site_id | location_id | lat | heading | site      | location | metric_group |
    +============+================================+=======+======+===========+=====================+=========+=============+=====+=========+===========+==========+==============+
    | 2021-01-01 | mean_WF_A01_TP_SG_LAT005_DEG000| 1.0   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A01         | 5.0 | 0.0     | WindFarm  | WFA01    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-02 | mean_WF_A01_TP_SG_LAT005_DEG000| 1.1   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A01         | 5.0 | 0.0     | WindFarm  | WFA01    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-01 | mean_WF_A02_TP_SG_LAT005_DEG000| 2.0   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A02         | 5.0 | 0.0     | WindFarm  | WFA02    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-02 | mean_WF_A02_TP_SG_LAT005_DEG000| 2.1   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A02         | 5.0 | 0.0     | WindFarm  | WFA02    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    """
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    # Normalize the data
    # fmt: off
    data["timestamp"] = pd.to_datetime(data["timestamp"] \
                        if "timestamp" in data.columns else data.index)
    data = data.reset_index(drop=True)
    # Melt the data
    normalized = data.melt(id_vars=["timestamp"],
                           var_name="metric",
                           value_name="value")
    # Merge the melted data with the metrics overview DataFrame
    normalized = normalized.merge(metrics_overview, how="left",
                                  left_on="metric", right_on="metric")
    # Rename the columns
    normalized.rename(columns={"unit_str": "unit",
                               "data_group": "metric_group"},
                      inplace=True)
    # Get the lat, and heading from the metric name
    normalized["lat"] = normalized["metric"] \
                        .str.extract(r"(_LAT)(\w{3})")[1].astype(float)
    normalized["heading"] = normalized["metric"] \
                            .str.extract(r"(_DEG)(\w{3})")[1].astype(float)
    # Now get the subassembly from the metric name.
    normalized["sub_assembly"] = normalized["metric"] \
                                 .str.extract(r"(_TP_)|(_TW_)|(_MP_)") \
                                 .bfill(axis=1)[0] \
                                 .str.replace("_", "")
    # Reorder the columns
    columns = ["timestamp", "metric", "value", "unit", "statistic",
               "short_hand", "site_id", "location_id", "sub_assembly", "lat",
               "heading", "site", "location", "metric_group"]
    normalized = normalized[columns]
    if keep_stat_in_metric_name:
        normalized["stat_short_hand"] = normalized["statistic"] \
                                        + "_" \
                                        + normalized["short_hand"]
    # Drop the rows where the value of column metric is "index", "site" or
    # "location"
    # fmt: on
    normalized = normalized[
        ~normalized["metric"].isin(["index", "site", "location"])
    ]
    return normalized.reset_index(drop=True)
