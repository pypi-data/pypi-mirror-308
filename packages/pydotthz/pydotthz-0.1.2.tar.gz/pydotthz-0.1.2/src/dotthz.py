import h5py
from dataclasses import dataclass, field
from typing import Dict
import numpy as np
from pathlib import Path


@dataclass
class DotthzMetaData:
    user: str = ""
    email: str = ""
    orcid: str = ""
    institution: str = ""
    description: str = ""
    md: Dict[str, str] = field(default_factory=dict)
    version: str = "1.00"
    mode: str = ""
    instrument: str = ""
    time: str = ""
    date: str = ""

    def add_field(self, key, value):
        self.md[key] = value


@dataclass
class DotthzMeasurement:
    datasets: Dict[str, np.ndarray] = field(default_factory=dict)
    meta_data: DotthzMetaData = field(default_factory=DotthzMetaData)


@dataclass
class DotthzFile:
    groups: Dict[str, DotthzMeasurement] = field(default_factory=dict)

    @classmethod
    def new(cls):
        return cls(groups={})

    @classmethod
    def from_data(cls, data: np.ndarray, meta_data: DotthzMetaData):
        measurement = DotthzMeasurement(datasets={"ds1": data}, meta_data=meta_data)
        return cls(groups={"Measurement 1": measurement})

    @classmethod
    def load(cls, path: Path):
        file = h5py.File(str(path), 'r')
        groups = {}

        for group_name, group in file.items():
            measurement = DotthzMeasurement()

            # Load datasets
            if "dsDescription" in group.attrs:
                ds_description_attr = group.attrs["dsDescription"]
                if isinstance(ds_description_attr, np.ndarray):
                    # Assume it’s a single-element array; get the first element
                    ds_description_str = ds_description_attr[0] if ds_description_attr.size == 1 else ", ".join(
                        map(str, ds_description_attr))
                else:
                    ds_description_str = ds_description_attr  # Already a string

                ds_descriptions = ds_description_str.split(", ") if isinstance(ds_description_str, str) else []
                for i, desc in enumerate(ds_descriptions):
                    dataset_name = f"ds{i + 1}"
                    if dataset_name in group:
                        measurement.datasets[desc] = group[dataset_name][...]

            # Load metadata attributes
            for attr in ["description", "date", "instrument", "mode", "time"]:
                if attr in group.attrs:
                    setattr(measurement.meta_data, attr, group.attrs[attr])
                    # Load user metadata with structure "ORCID/user/email/institution"

            if "thzVer" in group.attrs:
                if type(group.attrs["thzVer"]) == list:
                    measurement.meta_data.version = group.attrs["thzVer"][0]
                else:
                    measurement.meta_data.version = group.attrs["thzVer"]

            # Load user metadata with structure "ORCID/user/email/institution"
            if "user" in group.attrs:
                user_info = group.attrs["user"].split("/")
                fields = ["orcid", "user", "email", "institution"]
                for i, part in enumerate(user_info):
                    if i < len(fields):
                        setattr(measurement.meta_data, fields[i], part)

            # Load additional metadata descriptions and values
            if "mdDescription" in group.attrs:
                # Retrieve "mdDescription" attribute and handle possible array type
                md_description_attr = group.attrs["mdDescription"]
                if isinstance(md_description_attr, np.ndarray):
                    # Join array elements if necessary
                    md_description_str = md_description_attr[0] if md_description_attr.size == 1 else ", ".join(
                        map(str, md_description_attr))
                else:
                    md_description_str = md_description_attr  # Already a string

                # Now apply split if it’s a string
                md_descriptions = md_description_str.split(", ") if isinstance(md_description_str, str) else []

                # Iterate over the split descriptions to populate metadata
                for i, desc in enumerate(md_descriptions):
                    md_name = f"md{i + 1}"
                    if md_name in group.attrs:
                        measurement.meta_data.md[desc] = str(group.attrs[md_name])
            groups[group_name] = measurement
        file.close()
        return cls(groups=groups)

    def save(self, path: Path):
        with h5py.File(str(path), 'w') as file:
            for group_name, measurement in self.groups.items():
                group = file.create_group(group_name)

                # Write dataset descriptions
                ds_descriptions = ", ".join(measurement.datasets.keys())
                group.attrs["dsDescription"] = ds_descriptions

                # Write datasets
                for i, (name, dataset) in enumerate(measurement.datasets.items()):
                    ds_name = f"ds{i + 1}"
                    group.create_dataset(ds_name, data=dataset)

                # Write metadata
                for attr_name, attr_value in measurement.meta_data.__dict__.items():
                    if attr_name == "md":
                        # Write md descriptions as an attribute
                        md_descriptions = ", ".join(measurement.meta_data.md.keys())
                        group.attrs["mdDescription"] = md_descriptions
                        for i, (md_key, md_value) in enumerate(measurement.meta_data.md.items()):
                            md_name = f"md{i + 1}"
                            try:
                                # Attempt to save as float if possible
                                group.attrs[md_name] = float(md_value)
                                print(md_name, group.attrs[md_name])
                            except ValueError:
                                group.attrs[md_name] = md_value
                    elif attr_name == "version":
                        group.attrs["thzVer"] = measurement.meta_data.version

                    elif attr_name in ["orcid", "user", "email", "institution"]:
                        continue
                    else:
                        if attr_value:  # Only write non-empty attributes
                            group.attrs[attr_name] = attr_value

                # Write user metadata in the format "ORCID/user/email/institution"
                user_info = "/".join([
                    measurement.meta_data.orcid,
                    measurement.meta_data.user,
                    measurement.meta_data.email,
                    measurement.meta_data.institution
                ])
                group.attrs["user"] = user_info
