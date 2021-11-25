from PyQt5.QtWidgets import QApplication, QStackedWidget
from mainWindows import getStarted
from PyQt5.QtGui import QIcon
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    startWindow = getStarted(widget)
    widget.addWidget(startWindow)
    widget.setFixedHeight(400)
    widget.setFixedWidth(700)
    widget.setWindowIcon(QIcon('Ui/Images/icon.png'))
    widget.setWindowTitle('CVC')

    widget.show()
    sys.exit(app.exec_())