"""Handlers package that aggregates routers."""

from .admin.router import router as admin_router

__all__ = [
    "admin_router",
]


