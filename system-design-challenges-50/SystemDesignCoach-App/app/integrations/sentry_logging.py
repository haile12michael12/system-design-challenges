import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from typing import Literal
import os

class SentryLogger:
    def __init__(self):
        sentry_dsn = os.getenv("SENTRY_DSN")
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                integrations=[
                    FastApiIntegration(),
                ],
                traces_sample_rate=1.0,
            )
            
    @staticmethod
    def capture_exception(exception: Exception):
        """
        Capture and send exception to Sentry
        """
        sentry_sdk.capture_exception(exception)
        
    @staticmethod
    def capture_message(message: str, level: Literal["fatal", "critical", "error", "warning", "info", "debug"] = "info"):
        """
        Capture and send message to Sentry
        """
        sentry_sdk.capture_message(message, level=level)
        
    @staticmethod
    def add_user_context(user_id: int, username: str):
        """
        Add user context to Sentry events
        """
        sentry_sdk.set_user({
            "id": user_id,
            "username": username
        })
        
    @staticmethod
    def add_request_context(method: str, url: str, headers: dict):
        """
        Add request context to Sentry events
        """
        sentry_sdk.set_context("request", {
            "method": method,
            "url": url,
            "headers": headers
        })