from pydantic import BaseModel


class BaseChart(BaseModel):
    """Base class for all charts that allows dictionary usage."""

    def to_dict(self):
        try:
            return {d: value for d, value in zip(getattr(self, "x"), getattr(self, "y"))}
        except AttributeError:
            return self.model_dump()

    def __getitem__(self, item):
        return self.to_dict()[item]

    def values(self):
        return self.to_dict().values()

    def keys(self):
        return self.to_dict().keys()

    def items(self):
        return self.to_dict().items()

    def __iter__(self):
        return iter(self.to_dict())

    def __len__(self):
        return len(self.to_dict())
