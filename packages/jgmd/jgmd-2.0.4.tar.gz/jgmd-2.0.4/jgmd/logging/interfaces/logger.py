from ..loggingConsts import LogLevel
from ...util import ensureDirExists


class Logger:
    def __init__(
        self,
        logDirectory: str,
        fileName: str,
        logLevel: LogLevel,
        printToConsole: bool = True,
    ):
        ensureDirExists(logDirectory)
        self.filePath = f"{logDirectory}/{fileName}"
        self.logLevel: LogLevel = logLevel
        self.printToConsole: bool = printToConsole

    def clearLog(self):
        with open(self.filePath, "w") as file:
            pass
