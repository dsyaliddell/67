from backend.models.base_model import BaseModel


class Event(BaseModel):
    table_name = "event"

    def __init__(self, name=None, date=None, place=None,
                 description=None, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.date = date
        self.place = place
        self.description = description

    def save(self) -> int:
        return self.db.execute(
            """INSERT INTO event (name, date, place, description)
               VALUES (?, ?, ?, ?)""",
            (self.name, self.date, self.place, self.description)
        )
