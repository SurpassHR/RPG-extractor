# coding: utf-8
import sys
import platform

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ..gui_template.app.common.application import SingletonApplication
from ..gui_template.app.view.appFluentWindow import AppFluentWindow


def _setAppAttrs():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)


def _isWindows11OrHigher():
    if sys.platform.startswith("win"):
        versionInfo = platform.version()
        # win11 intern version number starts from 10.0.22000
        if (
            int(versionInfo.split(".")[0]) >= 10
            and int(versionInfo.split(".")[2]) >= 22000
        ):
            return True
    return False


def _platformSettings(window: AppFluentWindow):
    window.setMicaEffectEnabled(True if _isWindows11OrHigher() else False)
    if sys.platform == "darwin":
        from AppKit import NSApplication

        NSApplication.sharedApplication()


def startApp():
    _setAppAttrs()

    app = SingletonApplication(sys.argv, "DownloadXiaoeknowVideo")

    # set your window title here
    window = AppFluentWindow(window_title="Change Me!")
    _platformSettings(window=window)
    window.show()

    app.exec()
