import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEnginePage, QWebEngineProfile, QWebEngineScript

from njaXt import njaxt_ui, fuzzer_ui, payloads_ui
from njaXt import fuzzer
from njaXt.payloads import PAYLOADS


class PayloadsWidget(QtWidgets.QWidget, payloads_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.plainTextEdit.setPlainText(PAYLOADS)
        self.pushButton.clicked.connect(self.save_payloads)

    def save_payloads(self):
        global PAYLOADS
        PAYLOADS = self.plainTextEdit.toPlainText()
        self.close()


class FuzzerWidget(QtWidgets.QWidget, fuzzer_ui.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.data = {}
        self.pushButton.clicked.connect(self.handle_fuzz)

    def handle_fuzz(self):
        self.data["url"] = self.lineEdit.text()
        self.data["method"] = self.comboBox.currentText()
        self.data["headers"] = self.plainTextEdit.toPlainText()
        self.data["post_data"] = self.plainTextEdit_2.toPlainText() if self.data["method"] == "POST" else None
        self.close()

    def reset_widget(self):
        self.lineEdit.setText("")
        self.comboBox.setCurrentIndex(0)
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit_2.setPlainText("")
        self.data = {}

class Njaxt(QtWidgets.QMainWindow, njaxt_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fuzzer = None
        self.stopLoop = False
        self.fuzz_widget = FuzzerWidget()
        self.payload_widget = PayloadsWidget()
        self.init_webview()
        self.init_sigslot()
        self.show()

    def init_webview(self):
        self.webProfile = QWebEngineProfile(self.webView)
        self.webProfile.setHttpUserAgent(
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36")
        self.webProfile.setHttpAcceptLanguage("en-US,en;q=0.8")
        self.webProfile.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.set_scripts()
        self.webPage = QWebEnginePage(self.webProfile, self)

        self.webView.setPage(self.webPage)
        self.webView.loadProgress.connect(self.set_progress)
        self.webView.loadFinished.connect(lambda: self.lineEdit.setText(self.webView.url().toString()))

    def set_scripts(self):
        script = QWebEngineScript()
        script.setInjectionPoint(QWebEngineScript.DocumentCreation)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setSourceCode("""(function() {
                                    var _old_alert = window.alert;
                                    window.alert = function() {
                                        document.activeElement.innerHTML += "<br>alerting";
                                        _old_alert.apply(window,arguments);
                                        document.activeElement.innerHTML += "<br>done alerting<br>";
                                    };
                                })();
                             """
                             )
        self.webProfile.scripts().insert(script)

    def init_sigslot(self):
        self.lineEdit.returnPressed.connect(self.make_fuzzer)
        self.pushButton.clicked.connect(self.make_fuzzer)
        self.pushButtonReset.clicked.connect(self.handle_reset)

        self.actionAdvanced_Fuzzer.triggered.connect(self.show_fuzz)
        self.fuzz_widget.pushButton.clicked.connect(self.make_fuzzer)

        self.actionWordlist.triggered.connect(self.show_payloads)

    def set_progress(self, p):
        self.progressBar.setValue(p)

    def show_fuzz(self):
        self.fuzz_widget.show()

    def show_payloads(self):
        self.payload_widget.show()

    def make_fuzzer(self):
        if self.fuzz_widget.data:
            self.fuzzer = fuzzer.Fuzzer(self.fuzz_widget.data)
        else:
            self.fuzzer = fuzzer.Fuzzer({"url": self.lineEdit.text()})

        self.fuzz()

    def handle_reset(self):
        """
        Reset Fuzz Widget
        """
        self.fuzz_widget.reset_widget()
        """
        Reset Main Form
        """
        self.fuzzer = fuzzer.Fuzzer({"url": ""})
        self.init_webview()
        self.lineEdit.setText("")
        self.set_progress(0)

    def detect_xss(self, source):
        if "<br>alerting" in source:
            print(self.lineEdit.text())
            self.stopLoop = True

    def fuzz(self):
        loop = QEventLoop()
        for request in self.fuzzer.requests(PAYLOADS):
            self.webView.loadFinished.connect(loop.quit)
            self.webView.load(request)
            loop.exec()
            self.webView.page().toHtml(self.detect_xss)
            if self.stopLoop:
                break


def main():
    app = QtWidgets.QApplication(sys.argv)
    n = Njaxt()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
