from django.db import models


class Message(models.Model):

    room_name = models.CharField(max_length=100, default="general")
    username = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def to_dict(self):
        return {
            "username": self.username,
            "message": self.message,
            "timestamp": self.timestamp.isoformat() + "Z"
        }

