# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-python/-/raw/main/LICENSE

"""Channel information."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy


@dataclass(frozen=True, order=True)
class Channel:
    """Metadata associated with a channel.

    Channels are of the form:
        <source>:<identifier>

    Parameters
    ----------
    source : str
        The source associated with this channel.
    identifier : str
        The identifier associated with this channel.
    data_type : numpy.dtype
        The data type associated with this channel.
    sample_rate : float
        The sampling rate associated with this channel.
    time : int, optional
        The timestamp when this metadata became active.
    partition_id : str, optional
        The partition ID associated with this channel.

    """

    source: str
    identifier: str
    data_type: numpy.dtype
    sample_rate: float
    time: int | None = None
    partition_id: str | None = None

    @property
    def name(self) -> str:
        return str(self)

    def __repr__(self) -> str:
        return f"<{self.source}:{self.identifier}, {self.sample_rate} Hz, {self.data_type}>"  # noqa: E501

    def __str__(self) -> str:
        return f"{self.source}:{self.identifier}"

    def to_json(self, time: int | None = None) -> str:
        """Serialize channel metadata to JSON.

        Parameters
        ----------
        time : int, optional
            If specified, the timestamp when this metadata became active.

        """
        # generate dict from dataclass and adjust fields
        # to be JSON compatible. In addition, store the
        # channel name, as well as updating the timestamp
        # if passed in.
        obj = asdict(self)
        obj["channel"] = str(self)
        obj["data_type"] = numpy.dtype(self.data_type).name
        if time is not None:
            obj["time"] = time
        return json.dumps(obj)

    @classmethod
    def from_name(
        cls,
        name: str,
        data_type: numpy.dtype,
        sample_rate: float,
        time: int | None = None,
        partition_id: str | None = None,
    ) -> Channel:
        """Create a Channel from its canonical name.

        Parameters
        ----------
        name : str
            The channel name.
        time : int, optional
            The timestamp when this metadata became active.
        data_type : numpy.dtype, optional
            The data type associated with this channel.
        sample_rate : int, optional
            The sampling rate associated with this channel.

        """
        components = name.split(":")
        if len(components) != 2:
            raise ValueError(f"{name} is malformed")
        source, identifier = components
        return cls(
            source,
            identifier,
            data_type,
            sample_rate,
            time=time,
            partition_id=partition_id,
        )
