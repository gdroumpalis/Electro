from PyQt5.QtWidgets import QAction, QPushButton, QAbstractButton


def connect(signal, method):
    signal.connect(method)
