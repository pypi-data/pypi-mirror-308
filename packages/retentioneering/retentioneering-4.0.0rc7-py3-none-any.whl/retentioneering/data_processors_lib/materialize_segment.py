from __future__ import annotations

import numpy as np
import pandas as pd

from retentioneering.backend.tracker import collect_data_performance, time_performance
from retentioneering.data_processor import DataProcessor
from retentioneering.eventstream.segments import (
    SEGMENT_DELIMITER,
    SEGMENT_TYPE,
    _calculate_segment_col,
    _create_segment_event,
    _get_segment_mask,
)
from retentioneering.eventstream.types import (
    AddSegmentType,
    EventstreamSchemaType,
    EventstreamType,
    SeriesWithValidator,
)
from retentioneering.params_model import ParamsModel
from retentioneering.utils.doc_substitution import docstrings
from retentioneering.utils.hash_object import hash_dataframe


class MaterializeSegmentParams(ParamsModel):
    name: str


@docstrings.get_sections(base="MaterializeSegment")  # type: ignore
class MaterializeSegment(DataProcessor):
    """
    Propagate segment synthetic events to a column.

    Parameters
    ----------
    name : str
        Name of a segment to convert

    Returns
    -------
    Eventstream
        Eventstream with added column.
    """

    params: MaterializeSegmentParams

    @time_performance(scope="materialize_segment", event_name="init")
    def __init__(self, params: MaterializeSegmentParams) -> None:
        super().__init__(params=params)

    @time_performance(scope="materialize_segment", event_name="apply")
    def apply(self, df: pd.DataFrame, schema: EventstreamSchemaType) -> pd.DataFrame:
        name = self.params.name
        hash_before = hash_dataframe(df)
        shape_before = df.shape

        segment_col = _calculate_segment_col(df, schema, name)
        df[name] = segment_col

        collect_data_performance(
            scope="rename_segment",
            event_name="metadata",
            called_params=self.to_dict()["values"],
            performance_data={
                "parent": {
                    "shape": shape_before,
                    "hash": hash_before,
                },
                "child": {
                    "shape": df.shape,
                    "hash": hash_dataframe(df),
                },
            },
        )

        return df
