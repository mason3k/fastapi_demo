import csv
from contextlib import suppress
from dataclasses import dataclass, field
from itertools import count, dropwhile
from pathlib import Path
from typing import ClassVar
from collections.abc import Generator

from .model import HotSauce


@dataclass
class MockDb:
    SRC_FILE: ClassVar[Path] = Path(__file__).parent / "data.csv"
    items_by_id: dict[int, HotSauce] = field(init=False)
    id_generator: Generator = field(init=False)

    def __post_init__(self):
        self.items_by_id = self._load_data()
        self.id_generator = dropwhile(lambda x: x in self.items_by_id, count(start=1))

    def _load_data(self) -> dict[int, HotSauce]:
        with self.SRC_FILE.open() as f:
            items = {}
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                with suppress(Exception):
                    id_, *fields = row
                    items[int(id_)] = HotSauce(**dict(zip(HotSauce.model_fields, fields)))
            return items

    def add(self, sauce: HotSauce, sauce_id: int | None = None):
        if sauce_id is None:
            sauce_id = next(self.id_generator)
        if self.items_by_id.get(sauce_id):
            raise ValueError(f"Error: id {sauce_id} is already in use")
        self.items_by_id[sauce_id] = sauce
