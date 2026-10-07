from backend.models.base_model import BaseModel


class Request(BaseModel):
    table_name = "request"

    def __init__(self, user_id=None, event_id=None,
                 status_id=1, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.event_id = event_id
        self.status_id = status_id

    def save(self) -> int:
        request_id = self.db.execute(
            """INSERT INTO request (user_id, event_id, status_id)
               VALUES (?, ?, ?)""",
            (self.user_id, self.event_id, self.status_id)
        )
        self.id = request_id
        return request_id

    @classmethod
    def get_by_user(cls, user_id: int):
        """Все заявки конкретного пользователя с названиями статусов."""
        db = Database()
        return db.fetch_all(
            """SELECT r.id, e.name AS event_name, e.date,
                      e.place, s.name AS status_name,
                      r.created_at
               FROM request r
               JOIN event e ON r.event_id = e.id
               JOIN status s ON r.status_id = s.id
               WHERE r.user_id = ?
               ORDER BY r.created_at DESC""",
            (user_id,)
        )

    @classmethod
    def get_all_with_details(cls):
        """Все заявки всех пользователей (для администратора)."""
        db = Database()
        return db.fetch_all(
            """SELECT r.id, u.login, u.email, e.name AS event_name,
                      e.date, e.place, s.name AS status_name,
                      r.created_at
               FROM request r
               JOIN user u ON r.user_id = u.id
               JOIN event e ON r.event_id = e.id
               JOIN status s ON r.status_id = s.id
               ORDER BY r.created_at DESC"""
        )

    @classmethod
    def update_status(cls, request_id: int, status_id: int) -> bool:
        db = Database()
        db.execute(
            "UPDATE request SET status_id = ? WHERE id = ?",
            (status_id, request_id)
        )
        return True
