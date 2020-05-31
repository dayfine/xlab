# See https://github.com/apache/beam/blob/master/sdks/python/apache_beam/io/mongodbio.py
import dataclasses
from typing import Dict, List, Optional, Union

import apache_beam as beam
from apache_beam.transforms import ptransform
from apache_beam.io import mongodbio

from xlab.data.converters import mongo as mongo_converter

asdict = dataclasses.asdict


@dataclasses.dataclass(frozen=True)
class MongoOptionBase:
    uri: str = 'mongodb://localhost:27017'
    db: str = 'xlab'
    coll: str = 'data_entries'
    extra_client_params: Optional[Dict] = None


@dataclasses.dataclass(frozen=True)
class MongoReadOption(MongoOptionBase):
    # A `bson.SON` object specifying elements which must be present for a
    # document to be included in the result set
    filter: Optional[Dict] = None
    # A list of field names that should be returned in the result set or a dict
    # specifying the fields to include or exclude
    projection: Optional[Union[List[str], Dict]] = None


@dataclasses.dataclass(frozen=True)
class MongoWriteOption(MongoOptionBase):
    batch_size: int = 100


@ptransform.ptransform_fn
def ReadDataFromMongoDB(pbegin: beam.pvalue.PBegin, option: MongoReadOption):
    print(option)
    return (pbegin \
        | 'ReadFromMongoDB' >> mongodbio.ReadFromMongoDB(**asdict(option))
        | 'ToDataEntry' >> beam.Map(mongo_converter.from_mongo_doc))


@ptransform.ptransform_fn
def WriteDataToMongoDB(inputs: beam.pvalue.PCollection,
                       option: MongoWriteOption):
    return (inputs \
        | 'FromDataEntry' >> beam.Map(mongo_converter.to_mongo_doc)
        | 'WriteToMongoDB' >> mongodbio.WriteToMongoDB(**asdict(option)))
