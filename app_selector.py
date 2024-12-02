import winreg as reg
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QHBoxLayout, QListWidgetItem, QLineEdit, QFormLayout
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QSize
import os
import sys

def get_app_icon(exe_path):
    try:
        icon = QIcon(exe_path)
        if not icon.isNull():
            return icon
        return QIcon()  # Return a default icon if it fails
    except Exception as e:
        print(f"Error getting icon for {exe_path}: {e}")
        return QIcon()  # Return a default icon if it fails
    
def get_installed_apps_from_registry(custom_paths=None):
    print("Fetching installed apps from registry...")  # Checkpoint

    apps = []
    # Default registry paths
    registry_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\WOW6432Node"  # For 32-bit apps on 64-bit systems
    ]
    
    # Add custom paths if provided
    if custom_paths:
        registry_paths.extend(custom_paths)
    
    for path in registry_paths:
        try:
            reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, path)
            for i in range(0, reg.QueryInfoKey(reg_key)[0]):  # Iterate through subkeys
                subkey_name = reg.EnumKey(reg_key, i)
                try:
                    subkey = reg.OpenKey(reg_key, subkey_name)
                    display_name, _ = reg.QueryValueEx(subkey, "DisplayName")  # Get the display name
                    if display_name:
                        apps.append(display_name)
                except FileNotFoundError:
                    continue  # Skip if no valid "DisplayName" key exists
        except FileNotFoundError:
            continue  # Skip if the path doesn't exist
        
    print(f"Found {len(apps)} installed apps.")  # Checkpoint
    return apps

class ProductiveAppSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Productive Apps")
        self.setFixedSize(1200, 800)  # Increase window size for better viewing
        self.setStyleSheet("background-color: #F0F0F0;")  # Light gray background
        
        self.layout = QVBoxLayout()
        
        # Header label
        self.label = QLabel("Select Apps to mark as productive:")
        self.label.setFont(QFont("Arial", 16))
        self.label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        self.layout.addWidget(self.label)

        # Create a scrollable list widget to display all apps
        self.app_list_widget = QListWidget()
        self.app_list_widget.setSelectionMode(QListWidget.MultiSelection)  # Enable multi-selection
        self.app_list_widget.setIconSize(QSize(40, 40))  # Set larger icon size for visibility
        self.app_list_widget.setStyleSheet("background-color: white; border-radius: 5px; padding: 10px;")
        self.layout.addWidget(self.app_list_widget)

        # Custom path input field and button
        self.custom_path_input = QLineEdit(self)
        self.custom_path_input.setPlaceholderText("Enter custom registry path (optional)")
        self.custom_path_input.setStyleSheet("padding: 10px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.custom_path_input)

        # Load Button
        self.load_button = QPushButton("Load Apps with Custom Path")
        self.load_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px; margin-top: 10px;")
        self.load_button.clicked.connect(self.load_with_custom_path)
        self.layout.addWidget(self.load_button)

        # Save Button
        self.save_button = QPushButton("Save Selection")
        self.save_button.setStyleSheet("background-color: #007BFF; color: white; padding: 10px 20px; font-size: 16px; border-radius: 5px; margin-top: 20px;")
        self.save_button.clicked.connect(self.save_selection)
        self.layout.addWidget(self.save_button)

        # Add a horizontal layout to contain the main vertical layout
        container_layout = QHBoxLayout()
        container_layout.addLayout(self.layout)
        
        self.setLayout(container_layout)

        self.load_installed_apps()

    def load_installed_apps(self):
        """Load all installed apps from the registry and add them to the list widget."""
        print("Loading installed apps from the registry...")  # Checkpoint
        
        # Load apps with the default registry paths
        apps = get_installed_apps_from_registry()
        
        if not apps:
            print("No apps found!")  # Checkpoint if no apps were found
        else:
            print(f"Adding {len(apps)} apps to the list.")  # Checkpoint
        
        # Populate the list widget with app names and icons
        for app_name in apps:
            print(f"Adding app: {app_name}")  # Checkpoint
            item = QListWidgetItem(app_name)
            icon = get_app_icon(app_name)  # Get the icon for the app
            
            # Set the icon and name for each item in the list
            item.setIcon(icon)
            self.app_list_widget.addItem(item)

    def load_with_custom_path(self):
        """Load apps based on a custom registry path entered by the user."""
        custom_path = self.custom_path_input.text().strip()
        
        if custom_path:
            print(f"Loading apps from custom path: {custom_path}")  # Checkpoint
            apps = get_installed_apps_from_registry(custom_paths=[custom_path])
        else:
            print("Loading apps with default paths...")  # Checkpoint
            apps = get_installed_apps_from_registry()
        
        self.app_list_widget.clear()  # Clear previous list
        self.populate_app_list(apps)

    def populate_app_list(self, apps):
        """Populate the app list widget with app names and icons."""
        for app_name in apps:
            print(f"Adding app: {app_name}")  # Checkpoint
            item = QListWidgetItem(app_name)
            icon = get_app_icon(app_name)  # Get the icon for the app
            
            item.setIcon(icon)
            self.app_list_widget.addItem(item)
    
    def save_selection(self):
        selected_apps = [item.text() for item in self.app_list_widget.selectedItems()]
        
        if not selected_apps:
            print("No apps selected!")  # Checkpoint if no apps are selected
        
        # Save to a file
        with open("productive_apps.txt", "w") as f:
            for app in selected_apps:
                f.write(app + "\n")
        
        print(f"Saved productive apps: {selected_apps}") 
        self.close()

def run_app_selector():
    print("Starting the application...")  
    app = QApplication(sys.argv)
    window = ProductiveAppSelector()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app_selector()
