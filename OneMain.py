#!/usr/bin/python3
"""
Задача: Написать приложение, отображающее подключенные USB устройства
"""
#!/usr/bin/env python3
import select, sys, logging, threading, time
import usb1 as usb
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


# Разобратся с рефактором

# Главное окно
class Window(QMainWindow):
    def __init__(self,*args, **kwargs):
        super(Window,self).__init__(*args, **kwargs)
        self.setWindowTitle("USBChecker")
        self.resize(781, 383)
        self.menuBar = self.menuBar()
        self.create_widgets()
        # self.grid_picture()
        # main()
        # self.infinity_loop()
        # Настройка цвета

        self.setStyleSheet("""
            QMenuBar {
                background-color: #000000;
                color: #b8c9b1;
                border: 1px solid #000;
            }

            QMenuBar::item {
                background-color: #000000;
                color: #b8c9b1;
            }

            QMenuBar::item::selected {
                background-color: #000000;
            }
            QMenu {
                background-color: #000000;
                color: #b8c9b1;
                border: 1px solid #000;
            }

            QMenu::item::selected {
                background-color: #3c3d3c;
            }
            QMainWindow {
                background-color: #000000;
            }
            QPushButton {
                background-color: white
            }
        """)

        # Главное меню
        first_menu = self.menuBar.addMenu('Главное')
        options_menu = self.menuBar.addMenu('Настройки')
        help_menu = self.menuBar.addMenu('Помощь')

        # Подменю 1
        new_scan = QAction('Новое сканирование', self)
        new_scan.setShortcut("Ctrl+N")
        first_menu.addAction(new_scan)
        # Запускается цикл, не крашит, но меню неактивны.
        new_scan.triggered.connect(self.infinity_loop)

        exit_action = QAction('Выход', self)
        exit_action.setShortcut('Ctrl+X')
        exit_action.triggered.connect(lambda: QApplication.quit())

        first_menu.addAction(exit_action)

        # Под-подменю 2
        filter_menu = options_menu.addMenu('Фильтр')
        port_number_action = QAction('Номер порта', self)
        product_identification_action = QAction('Идентификатор продукта устройства', self)
        vendor_identification_action = QAction('Идентификатор поставщика продукта', self)
        device_class_action = QAction('Класс устройства', self)
        number_bus_action = QAction('Номер шины устройства', self)
        address_bus_action = QAction('Адрес шины устройства', self)

        # Добавление кнопки
        filter_menu.addAction(port_number_action)
        filter_menu.addAction(product_identification_action)
        filter_menu.addAction(vendor_identification_action)
        filter_menu.addAction(device_class_action)
        filter_menu.addAction(number_bus_action)
        filter_menu.addAction(address_bus_action)

        # Подменю 3
        doc_help_menu = QAction('Помощь', self)
        doc_help_menu.setShortcut('F1')
        help_menu.addAction(doc_help_menu)

        # self.infinity_loop()

    # Cоздаем кнопку сканирование
    def create_widgets(self):
        scan_btn = QPushButton("Сканирование", self)
        scan_btn.setGeometry(50, 90, 140, 40)
        # Единоразовый вызов цикла
        scan_btn.clicked.connect(self.check)

        other_picture = QWidget()
        other_picture.setGeometry(100, 100, 100, 100)
        other_picture.show()


    # Функция под вопросом.
    def clicked_btn(self):
        self.label.setText("Hello")

    # Функция закрытия окна
    def close_window(self):
        self.close()

    # Вызов итератора подключенных устройств по usb ( вывод в консоле) Думаю как выкатить в менюху
    def check(self):
        all_device_set = set()
        upgrade_all_device_set = set()
        check_device_set = set()

        time.sleep(1)

        with usb.USBContext() as context:

                # Получаем список всех подключенных устройств
            usb_device_list = context.getDeviceList()

                # Список с информации по каждому устройству
            for device in usb_device_list:
                all_device_set = {device}
                # Поверхностное копироние
                upgrade_all_device_set = set(all_device_set)
                # Разность множеств.
                check_device_set = all_device_set.difference(upgrade_all_device_set)

                print(check_device_set)

                for upgrade_device_in_check in check_device_set:
                    print("\n", upgrade_device_in_check, (" Разность множеств\n").upper())

            for device_in_set in all_device_set:
                try:

                        # Если устройство не опознанно возврат VID и PID
                    if device_in_set.open().getASCIIStringDescriptor(device_in_set.getManufacturerDescriptor()) is None:
                        print('Вендор', device_in_set.getVendorID())
                    if device_in_set.open().getASCIIStringDescriptor(device_in_set.getProductDescriptor()) is None:
                        print('Продукт', device_in_set.getProductDescriptor())

                        # print('Номер порта: {}\n'.format(device_in_set.getPortNumber()), \
                        #       'Идентификатор  устройства: {}\n'.format(device_in_set.getProductID()), \
                        #       'Расшифровка полученного: {}\n'.format(device_in_set.getProductDescriptor()), \
                        #       'Тип устройства: {}\n'.format(
                        #           device_in_set.open().getASCIIStringDescriptor(device_in_set.getProductDescriptor())), \
                        #       'Расшифровка полученного: {}\n'.format(device_in_set.getManufacturerDescriptor()), \
                        #       'Производитель: {}\n'.format(
                        #           device_in_set.open().getASCIIStringDescriptor(device_in_set.getManufacturerDescriptor())), \
                        #       'Идентификатор производителя : {}\n'.format(device_in_set.getVendorID()), \
                        #       'Номер шины устройства: {}\n'.format(device_in_set.getBusNumber()), \
                        #       'Адрес шины устройства: {}\n'.format(device_in_set.getDeviceAddress()), \
                        #       '-' * 80,
                        #       # 'test message: {}\n'.format(device_in_set.getStringDescriptor())
                        #       )

                except Exception:
                    pass




        # что-то надо вернуть
        # return check_device_set()

    # Бесконечный цикл обработки потока.
    def infinity_loop(self):
        # Цикл потока
        while True:
            format = "%(asctime)s: %(message)s"
            logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

            threads_one = list()

            for index in range(1):
                # logging.info("Основной : создать и запустить поток %d.", index)
                first_thread = threading.Thread(target=Window.check, args=(index,))
                threads_one.append(first_thread)
                # Контроль процесса
                QApplication.processEvents()
                first_thread.start()

            for index, thread in enumerate(threads_one):
                # logging.info("Основной : перед присоединением к потоку %d.", index)
                thread.join()
                # logging.info("Основной  : поток %d выполнен", index)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
