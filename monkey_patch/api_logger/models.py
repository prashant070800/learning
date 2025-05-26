from django.db import models

class ExternalAPIRequestLog(models.Model):
    url = models.URLField()
    request_headers = models.JSONField(null=True, blank=True)
    request_params = models.JSONField(null=True, blank=True)
    response_status = models.IntegerField()
    response_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.response_status}"
