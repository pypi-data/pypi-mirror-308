import asyncio
import httpx
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class MonitorMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, webhook_url: str):
        super().__init__(app)
        self.webhook_url = webhook_url

    async def dispatch(self, request: Request, call_next):
        method = request.method
        response = await call_next(request)

        try:
        
            if response.status_code >= 400:
                request_data = {
                    "event_name": "Client Error" if response.status_code < 500 else "Server Error",
                    "message": f"""Method: {method}  ||  Path: {request.url.path}  ||  Status_Code: {response.status_code}""",
                    "username": "FastApi APM",
                    "status": "error"
                }
    
                # Send to webhook asynchronously without waiting
                asyncio.create_task(self._send_to_webhook(request_data))
        except Exception as e:
            # Handle unknown errors
            request_data = {
                    "event_name": "Client Error" if response.status_code < 500 else "Server Error",
                    "message": f"Unknown Server Error: {e}",
                    "username": "FastApi APM",
                    "status": "error"
                }
    
                # Send to webhook asynchronously without waiting
            asyncio.create_task(self._send_to_webhook(request_data))

        
        return response

    async def _send_to_webhook(self, data):
        async with httpx.AsyncClient() as client:
            try:
                await client.post(self.webhook_url, json=data)
            except httpx.RequestError as e:
                # Log error or handle failure
                print(f"Failed to send to webhook: {e}")
