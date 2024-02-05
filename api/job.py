from database import db
import uuid


class Job(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=str(uuid.uuid4()), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'status': self.status
        }