from PyQt5 import QtWidgets, QtCore
import sys
import pandas as pd

class GymApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Create layout
        layout = QtWidgets.QVBoxLayout()
        
        # Fitness Level selection
        self.level_label = QtWidgets.QLabel("Select Fitness Level:")
        self.level_combo = QtWidgets.QComboBox()
        self.level_combo.addItems(["Beginner", "Intermediate"])
        layout.addWidget(self.level_label)
        layout.addWidget(self.level_combo)
        
        # Exercise Type selection
        self.type_label = QtWidgets.QLabel("Select Exercise Type:")
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Strength", "Stretching"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        
        # Body Part selection
        self.body_label = QtWidgets.QLabel("Select Body Parts:")
        self.body_list = QtWidgets.QListWidget()
        self.body_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        body_parts = dataset['BodyPart'].fillna('').unique().tolist()
        self.body_list.addItems(body_parts)
        layout.addWidget(self.body_label)
        layout.addWidget(self.body_list)
        
        # Equipment selection
        self.equipment_label = QtWidgets.QLabel("Select Equipment:")
        self.equipment_list = QtWidgets.QListWidget()
        self.equipment_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        equipments = dataset['Equipment'].fillna('').unique().tolist()
        equipments = [str(equipment) for equipment in equipments]
        self.equipment_list.addItems(equipments)
        layout.addWidget(self.equipment_label)
        layout.addWidget(self.equipment_list)
        
        # Submit button
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.filter_exercises)
        layout.addWidget(self.submit_button)
        
        # Results
        self.results = QtWidgets.QTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)
        
        # Set layout
        self.setLayout(layout)
        self.setWindowTitle('Gym Exercise Filter')
        self.setGeometry(300, 300, 400, 500)
        
    def filter_exercises(self):
        level = self.level_combo.currentText()
        exercise_type = self.type_combo.currentText()
        
        selected_body_parts = [item.text() for item in self.body_list.selectedItems()]
        selected_equipments = [item.text() for item in self.equipment_list.selectedItems()]
        
        # Filter based on level, type, and selected equipment
        filtered = dataset[
            (dataset['Level'] == level) &
            (dataset['Type'] == exercise_type) &
            (dataset['Equipment'].isin(selected_equipments))
        ]
        
        self.results.clear()
        if not filtered.empty:
            for body_part in selected_body_parts:
                part_filtered = filtered[filtered['BodyPart'] == body_part].head(3)
                if not part_filtered.empty:
                    self.results.append(f"Exercises for {body_part}:\n")
                    for index, row in part_filtered.iterrows():
                        self.results.append(f"Title: {row['Title']}\nDescription: {row['Desc']}\n")
                else:
                    self.results.append(f"No exercises found for {body_part} with the selected criteria.\n")
        else:
            self.results.append("No exercises found for the selected criteria.")

if __name__ == '__main__':
    # Load the dataset
    file_path = 'input/megaGymDataset.csv'  # Update with your file path
    dataset = pd.read_csv(file_path)
    
    app = QtWidgets.QApplication(sys.argv)
    gym_app = GymApp()
    gym_app.show()
    sys.exit(app.exec_())
