"""
Database package initialization.

This package provides the DatabaseManager class that encapsulates
the PostgreSQL connection, session management, and database initialization.
"""

from .db import DatabaseManager

__all__ = ['DatabaseManager']
