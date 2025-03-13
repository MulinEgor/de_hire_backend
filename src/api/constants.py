"""Модуль для констант."""

# MARK: Security
AUTH_HEADER_NAME: str = "X-Authorization"
ALGORITHM: str = "HS256"

CORS_HEADERS: list[str] = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "X-Authorization",
]
CORS_METHODS: list[str] = [
    "GET",
    "POST",
    "OPTIONS",
    "DELETE",
    "PATCH",
    "PUT",
]
