from backend.models.base_model import BaseModel


class Review(BaseModel):
    table_name = "review"

    def __init__(self, request_id=None, text=None,
                 rating=None, **kwargs):
        super().__init__(**kwargs)
        self.request_id = request_id
        self.text = text
        self.rating = rating

    def save(self) -> int:
        return self.db.execute(
            """INSERT INTO review (request_id, text, rating)
               VALUES (?, ?, ?)""",
            (self.request_id, self.text, self.rating)
        )
