import sys      
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class HyperlinkLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet('font-size: 35px')
        self.setOpenExternalLinks(True)
        self.setParent(parent)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()

        linkTemplate = '<a target="_blank" href={0}>{1}</a>.<br/><br/>'

        label1 = HyperlinkLabel(self)
        label1.setText(linkTemplate.format('https://open5e.com/monsters/ancient-black-dragon', 'Open5e.com'))

        label2 = HyperlinkLabel(self)
        label2.setText(linkTemplate.format('https://Github.com', 'Click Me'))
        label2.move(100, 100)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())