import sys
import io
from PyQt5.QtCore import QObject, pyqtSignal


class LogSignal(QObject):
    """Signal để gửi log message từ bất kỳ thread nào đến GUI"""
    message = pyqtSignal(str)


class GuiLogHandler(io.TextIOBase):
    """
    Custom output stream để redirect print() vào GUI log panel.
    Hoạt động như một proxy giữa stdout và Qt signal.
    """
    
    def __init__(self, signal: LogSignal, original_stdout):
        super().__init__()
        self.signal = signal
        self.original_stdout = original_stdout
    
    def write(self, text: str):
        if text.strip():  # Bỏ qua empty lines
            self.signal.message.emit(text)
        # Vẫn ghi ra console gốc để debug
        if self.original_stdout:
            self.original_stdout.write(text)
        return len(text)
    
    def flush(self):
        if self.original_stdout:
            self.original_stdout.flush()


# Global signal instance để sử dụng trong toàn app
log_signal = LogSignal()


def redirect_stdout_to_gui():
    """
    Redirect stdout để tất cả print() statements đều được gửi vào GUI.
    Trả về LogSignal để connect với GUI widget.
    """
    handler = GuiLogHandler(log_signal, sys.stdout)
    sys.stdout = handler
    return log_signal


def restore_stdout():
    """Khôi phục stdout gốc"""
    if isinstance(sys.stdout, GuiLogHandler):
        sys.stdout = sys.stdout.original_stdout
