from backend.models.base_model import BaseModel


class Status(BaseModel):
    table_name = "status"

    def __init__(self, name=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
