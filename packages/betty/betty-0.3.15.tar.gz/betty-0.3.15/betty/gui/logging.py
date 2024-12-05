"""
Provide logging for the Graphical User Interface.
"""

import logging

from PyQt6.QtCore import QObject, pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from typing_extensions import override

from betty.gui.text import Text


class LogRecord(Text):
    """
    Show a single log record.
    """

    _LEVELS = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
        logging.NOTSET,
    ]

    _formatter = logging.Formatter()

    def __init__(self, record: logging.LogRecord):
        super().__init__(self._formatter.format(record))
        self.setProperty("level", self._normalize_level(record.levelno))

    def _normalize_level(self, record_level: int) -> int:
        for level in self._LEVELS:
            if record_level >= level:
                return level
        return logging.NOTSET


class LogRecordViewer(QWidget):
    """
    Show log records.
    """

    def __init__(self):
        super().__init__()
        self._log_record_layout = QVBoxLayout()
        self.setLayout(self._log_record_layout)

    def log(self, record: logging.LogRecord) -> None:
        """
        Add the log record to be shown.
        """
        self._log_record_layout.addWidget(LogRecord(record))


class _LogRecordViewerHandlerObject(QObject):
    """
    Provide a signal for logging handlers to log records to a LogRecordViewer in the main (GUI) thread.
    """

    log = pyqtSignal(logging.LogRecord)

    def __init__(self, viewer: LogRecordViewer):
        super().__init__()
        self.log.connect(  # type: ignore[call-arg]
            viewer.log,
            Qt.ConnectionType.QueuedConnection,
        )


class LogRecordViewerHandler(logging.Handler):
    """
    A logging handler that forwards all records to a :py:class:`betty.gui.logging.LogRecordViewer`.
    """

    log = pyqtSignal(logging.LogRecord)

    def __init__(self, viewer: LogRecordViewer):
        super().__init__()
        self._object = _LogRecordViewerHandlerObject(viewer)

    @override
    def emit(self, record: logging.LogRecord) -> None:
        self._object.log.emit(record)
