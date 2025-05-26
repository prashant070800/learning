from django.contrib import admin
from .models import ExternalAPIRequestLog
from django import forms
from django.http import HttpResponseRedirect
from django.urls import path
import requests


# @admin.register(ExternalAPIRequestLog)
# class ExternalAPIRequestLogAdmin(admin.ModelAdmin):
#     list_display = ('url', 'response_status', 'created_at')
#     readonly_fields = ('url', 'request_headers', 'request_params', 'response_status', 'response_body', 'created_at')

class TriggerRequestForm(forms.Form):
    url = forms.URLField(label="API URL", initial="https://google.com")

@admin.register(ExternalAPIRequestLog)
class ExternalAPIRequestLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'response_status', 'created_at')
    readonly_fields = ('url', 'request_headers', 'request_params', 'response_status', 'response_body', 'created_at')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('trigger-request/', self.admin_site.admin_view(self.trigger_request), name='trigger-request'),
        ]
        return custom_urls + urls

    def trigger_request(self, request):
        if request.method == "POST":
            form = TriggerRequestForm(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                requests.get(url)  # <- Triggers monkey-patched version
                self.message_user(request, f"Requested {url}")
                return HttpResponseRedirect("../")
        else:
            form = TriggerRequestForm()

        from django.shortcuts import render
        return render(request, "admin/trigger_request.html", {"form": form})