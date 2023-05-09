import uuid
from django.db import models

from users.models import User


class Friendship(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user_from = models.ForeignKey(
        User,
        related_name="outgoing_req",
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User,
        related_name="incoming_req",
        on_delete=models.CASCADE
    )
    request_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return str(self.id)
