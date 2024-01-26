import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QRadioButton, QTextEdit

class StartupWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Welcome to Sunstorm-GUI")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Add a label with the welcome message
        welcome_label = QLabel("Made by UnknownCoder13 with love :)")
        layout.addWidget(welcome_label)

        # Add a button to open the main GUI
        thank_you_button = QPushButton("Thank You!")
        layout.addWidget(thank_you_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect the "Thank You!" button to the openMainGUI function
        thank_you_button.clicked.connect(self.openMainGUI)

    def openMainGUI(self):
        self.main_window = SunstormGUI()
        self.main_window.show()
        self.close()

class SunstormGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sunstorm-GUI")
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.ipsw_label = QLabel("IPSW Path:")
        self.ipsw_path = QLineEdit()
        self.browse_ipsw_button = QPushButton("Browse")

        self.blob_label = QLabel("Blob Path:")
        self.blob_path = QLineEdit()
        self.browse_blob_button = QPushButton("Browse")

        self.kpp_checkbox = QCheckBox("KPP")

        self.boardconfig_label = QLabel("BoardConfig:")
        self.boardconfig = QLineEdit()

        self.identifier_label = QLabel("Identifier:")
        self.identifier = QLineEdit()
        self.identifier.setDisabled(True)  # Disabled by default

        self.legacy_checkbox = QCheckBox("Legacy")

        self.skip_baseband_checkbox = QCheckBox("Skip Baseband")

        self.command_output = QTextEdit()
        self.command_output.setReadOnly(True)

        self.restore_radio = QRadioButton("Restore")
        self.boot_radio = QRadioButton("Boot")

        self.execute_button = QPushButton("Execute")

        # Layout setup
        layout = QVBoxLayout()

        ipsw_layout = QHBoxLayout()
        ipsw_layout.addWidget(self.ipsw_label)
        ipsw_layout.addWidget(self.ipsw_path)
        ipsw_layout.addWidget(self.browse_ipsw_button)

        blob_layout = QHBoxLayout()
        blob_layout.addWidget(self.blob_label)
        blob_layout.addWidget(self.blob_path)
        blob_layout.addWidget(self.browse_blob_button)

        command_layout = QHBoxLayout()
        command_layout.addWidget(self.restore_radio)
        command_layout.addWidget(self.boot_radio)

        layout.addLayout(ipsw_layout)
        layout.addLayout(blob_layout)
        layout.addWidget(self.kpp_checkbox)
        layout.addLayout(command_layout)
        layout.addWidget(self.boardconfig_label)
        layout.addWidget(self.boardconfig)
        layout.addWidget(self.identifier_label)
        layout.addWidget(self.identifier)
        layout.addWidget(self.legacy_checkbox)
        layout.addWidget(self.skip_baseband_checkbox)
        layout.addWidget(self.execute_button)
        layout.addWidget(self.command_output)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect buttons to functions
        self.browse_ipsw_button.clicked.connect(self.browseIPSW)
        self.browse_blob_button.clicked.connect(self.browseBlob)
        self.execute_button.clicked.connect(self.executeCommand)
        self.restore_radio.toggled.connect(self.toggleIdentifier)

    def browseIPSW(self):
        ipsw_path, _ = QFileDialog.getOpenFileName(self, "Select IPSW File", "", "IPSW Files (*.ipsw);;All Files (*)")
        if ipsw_path:
            self.ipsw_path.setText(ipsw_path)

    def browseBlob(self):
        blob_path, _ = QFileDialog.getOpenFileName(self, "Select Blob File", "", "Blob Files (*.shsh);;All Files (*)")
        if blob_path:
            self.blob_path.setText(blob_path)

    def toggleIdentifier(self, checked):
        # Enable Identifier if Boot is selected, disable if Restore is selected
        self.identifier.setDisabled(checked)

    def executeCommand(self):
        ipsw_path = self.ipsw_path.text()
        blob_path = self.blob_path.text()
        kpp_option = "-kpp" if self.kpp_checkbox.isChecked() else ""
        boardconfig = self.boardconfig.text()
        legacy_option = "--legacy" if self.legacy_checkbox.isChecked() else ""
        skip_baseband_option = "--skip-baseband" if self.skip_baseband_checkbox.isChecked() else ""
        command = ""

        if self.restore_radio.isChecked():
            command = f"sudo python3 sunstorm.py -i \"{ipsw_path}\" -t \"{blob_path}\" -r -d \"{boardconfig}\" {kpp_option} {skip_baseband_option} {legacy_option}"
        elif self.boot_radio.isChecked():
            identifier = self.identifier.text()
            command = f"sudo python3 sunstorm.py -i \"{ipsw_path}\" -t \"{blob_path}\" -b -d \"{boardconfig}\" -id \"{identifier}\" {kpp_option} {skip_baseband_option} {legacy_option}"

        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            self.command_output.setPlainText(result)

            # Check if the command is a "Boot" command and display a success message
            if "Boot" in command:
                self.command_output.setPlainText("Boot files created successfully!")

        except subprocess.CalledProcessError as e:
            self.command_output.setPlainText(f"Command failed with error:\n{e.output}")

def main():
    app = QApplication(sys.argv)

    # Create the startup window and show it
    startup_window = StartupWindow()
    startup_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
