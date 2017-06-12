from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon


class Previewer(QWidget):
    instance = 0
    def __init__(self, parent=None, index = -1):
        super(Previewer, self).__init__(parent)
        self.parent = parent
        self.index = index
        self.handle = QWebEngineView()
        self.handle.setGeometry(100, 100, 350, 400)
        self.handle.setWindowTitle("Helper")
        self.handle.setWindowIcon(QIcon('icon.png'))
        if self.index == 0:
            link = "help\\read_time.html"
        elif self.index == 1:
            link = "help\\set_time.html"
        elif self.index == 2:
            link = "help\\read_date.html"
        elif self.index == 3:
            link = "help\\set_date.html"
        elif self.index == 4:
            link = "help\\set_cursor.html"
        elif self.index == 5:
            link = "help\\char_input.html"
        elif self.index == 6:
            link = "help\\char_output.html"
        elif self.index == 7:
            link = "help\\disc_space.html"
        else:
            link = "help\\index.html"
        page = open(link, 'r').read()
        self.page = QWebEnginePage()
        self.page.setHtml(page)
        self.handle.setPage(self.page)
        self.handle.show()


    def zamknij(self):
        Previewer.instance -= 1
        self.handle.destroy()