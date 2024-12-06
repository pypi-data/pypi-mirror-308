from pydantic import BaseModel, validator, Extra
from typing import List, Dict, Any, ClassVar
import random
from ..predictors.predictors import SievePredictor, TemporalPredictor, ObjectPredictor

class State(BaseModel, extra=Extra.allow):
    """Base class to access inputs"""
    pass

class Sample(BaseModel):
    """
    A sample is a single input-output example in a dataset
    """
    input: State
    output: Any

    ALLOWED_INPUT_TYPES: ClassVar[List] = SievePredictor.ALLOWED_INPUT_TYPES
    ALLOWED_OUTPUT_TYPES: ClassVar[List] = SievePredictor.ALLOWED_OUTPUT_TYPES

        
class TemporalSample(Sample):
    """
    A temporal sample is a sample that has a temporal component
    """
    ALLOWED_INPUT_TYPES: ClassVar[List] = TemporalPredictor.ALLOWED_INPUT_TYPES 
    ALLOWED_OUTPUT_TYPES: ClassVar[List] = TemporalPredictor.ALLOWED_OUTPUT_TYPES

class ObjectSample(Sample):
    """
    An object sample is a sample that has a single object
    """
    ALLOWED_INPUT_TYPES: ClassVar[List] = ObjectPredictor.ALLOWED_INPUT_TYPES 
    ALLOWED_OUTPUT_TYPES: ClassVar[List] =ObjectPredictor.ALLOWED_OUTPUT_TYPES

class Dataset(BaseModel):
    """
    A dataset is a collection of samples. It is used to train a model
    """

    samples: List[Sample]
    batch_size: int = 1

    def iterate_batch(self):
        # Iterate over the dataset in batches
        for i in range(0, len(self.samples), self.batch_size):
            yield self.samples[i:i+self.batch_size]

    def iterate(self):
        # Iterate over the dataset one by one
        for sample in self.samples:
            yield sample

    def shuffle(self):
        # Shuffle the dataset
        random.shuffle(self.samples)
    
    def add_sample(self, sample: Sample):
        self.samples.append(sample)
    
    def add_samples(self, samples: List[Sample]):
        self.samples += samples

    def get_output_types(self):
        return set([s.get_output_type() for s in self.samples])

    def get_input_types(self):
        types = set()
        for sample in self.samples:
            types.update(sample.get_input_types())
        return types
    
    def split(self, ratio: float, shuffle: bool = True):
        # Split the dataset into two datasets
        if shuffle:
            self.shuffle()
        split_index = int(len(self.samples) * ratio)
        return Dataset(samples=self.samples[:split_index], batch_size=self.batch_size), Dataset(samples=self.samples[split_index:], batch_size=self.batch_size)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]

    def __iter__(self):
        return self.iterate
    
    def __add__(self, other: 'Dataset'):
        return Dataset(samples=self.samples + other.samples)

    def __iadd__(self, other: 'Dataset'):
        self.samples += other.samples
        return self

    def __repr__(self):
        return f"Dataset(samples={self.samples}, batch_size={self.batch_size})"

    def __str__(self):
        return f"Dataset(samples={self.samples}, batch_size={self.batch_size})"
    
    def __eq__(self, other: 'Dataset'):
        return self.samples == other.samples and self.batch_size == other.batch_size
    
    def __ne__(self, other: 'Dataset'):
        return not self.__eq__(other)

class TemporalDataset(Dataset):
    """
    A temporal dataset is a dataset that has a temporal component
    """
    samples: List[TemporalSample]

    def split(self, ratio: float, shuffle: bool = True):
        # Split the dataset into two datasets
        if shuffle:
            self.shuffle()
        split_index = int(len(self.samples) * ratio)
        return TemporalDataset(samples=self.samples[:split_index], batch_size=self.batch_size), TemporalDataset(samples=self.samples[split_index:], batch_size=self.batch_size)


class ObjectDataset(Dataset):
    """
    An object dataset is a dataset that has a single object
    """
    samples: List[ObjectSample]

    def split(self, ratio: float, shuffle: bool = True):
        # Split the dataset into two datasets
        if shuffle:
            self.shuffle()
        split_index = int(len(self.samples) * ratio)
        return ObjectDataset(samples=self.samples[:split_index], batch_size=self.batch_size), ObjectDataset(samples=self.samples[split_index:], batch_size=self.batch_size)
