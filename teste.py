from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])
pb = QtWidgets.QProgressBar()
pb.show()
pb.setValue(10)
app.exec()