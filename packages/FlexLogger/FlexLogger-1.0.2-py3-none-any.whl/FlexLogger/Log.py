from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class SyslogLevel(Enum):
    """
    SYSLOG Levels Codes (0 to 7):

    0 - **Emergency**: The system is unusable. This is the most severe log level, indicating a catastrophic failure (e.g., system crash).

    1 - **Alert**: Action must be taken immediately. Critical conditions that require urgent attention.

    2 - **Critical**: Critical conditions that may affect the operation of the system, but not as dire as an alert.

    3 - **Error**: Error conditions that indicate problems, but may not necessarily stop the system from functioning.

    4 - **Warning**: Warning conditions that may or may not affect the normal operation of the system.

    5 - **Notice**: Normal but significant conditions that are informative and may require monitoring.

    6 - **Informational**: Informational messages that provide general system operation details.

    7 - **Debug**: Detailed debugging messages used for troubleshooting.
    """
    EMERGENCY: int = 0
    ALERT: int = 1
    CRITICAL: int = 2
    ERROR: int = 3
    WARNING: int = 4
    NOTICE: int = 5
    INFORMATIONAL: int = 6
    DEBUG: int = 7


class Classification(Enum):
    RUN_OK: tuple[str, str, SyslogLevel] = ("Run", "✅Success", SyslogLevel.INFORMATIONAL)
    RUN_FAIL: tuple[str, str, SyslogLevel] = ("Run", "❌Failed", SyslogLevel.ERROR)
    REMINDER_RUN: tuple[str, str, SyslogLevel] = ("Reminder", "Reminder cycle executed", SyslogLevel.INFORMATIONAL)
    REMINDER_ALERT: tuple[str, str, SyslogLevel] = ("Reminder", "⭐Reminder Sent", SyslogLevel.NOTICE)
    MYSQL_CONNECTION_OK: tuple[str, str, SyslogLevel] = ("MySQL", "✅Connection Success", SyslogLevel.INFORMATIONAL)
    MYSQL_CONNECTION_FAIL: tuple[str, str, SyslogLevel] = ("MySQL", "❌Connection Failed", SyslogLevel.ERROR)
    POSTGRESQL_CONNECTION_OK: tuple[str, str, SyslogLevel] = ("PostgreSQL", "✅Connection Success", SyslogLevel.INFORMATIONAL)
    POSTGRESQL_CONNECTION_FAIL: tuple[str, str, SyslogLevel] = ("PostgreSQL", "❌Connection Failed", SyslogLevel.ERROR)
    SQLSERVER_CONNECTION_OK: tuple[str, str, SyslogLevel] = ("MS SQL Server", "✅Connection Success", SyslogLevel.INFORMATIONAL)
    SQLSERVER_CONNECTION_FAIL: tuple[str, str, SyslogLevel] = ("MS SQL Server", "❌Connection Failed", SyslogLevel.ERROR)
    WEB_SCRAPING_OK: tuple[str, str, SyslogLevel] = ("Web Scraping", "✅Scraping Finished", SyslogLevel.INFORMATIONAL)
    WEB_SCRAPING_FAIL: tuple[str, str, SyslogLevel] = ("Web Scraping", "❌Scraping Failed", SyslogLevel.ERROR)
    CONTENT_CHANGES_VERIFIED: tuple[str, str, SyslogLevel] = ("Content", "Verified for Changes", SyslogLevel.INFORMATIONAL)
    CONTENT_UPDATED: tuple[str, str, SyslogLevel] = ("Content", "⭐New Content Detected", SyslogLevel.NOTICE)
    CONTENT_UNCHANGED: tuple[str, str, SyslogLevel] = ("Content", "Content Unchanged", SyslogLevel.INFORMATIONAL)


@dataclass
class Log:
    """
    A class to represent a log entry in a system.

    Args:
        id (int): Unique identifier for the log entry.
        datetime (datetime): Date and time when the log entry was created.
        application (str): The name of the application generating the log.
        source (str): The source of the log entry (e.g., host or network).
        title (str): A brief title describing the log entry.
        category (str): The primary category of the log entry.
        category2 (str): A secondary category for finer granularity.
        contents (str): Detailed content of the log entry.
        SYSLOG_LEVELS_code (SyslogLevel): The represented the syslog level (severity of the log).
    """

    id: int = field(init=False)
    datetime: datetime = field(init=False)
    application: str
    source: str
    title: str
    category: str
    category2: str
    contents: Optional[str] = None
    SYSLOG_LEVELS_code: Optional[SyslogLevel] = None
