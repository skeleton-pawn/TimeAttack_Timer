import sys
import csv
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QSpinBox, QTextEdit, QHBoxLayout, QInputDialog, QFrame
)
# Make sure Qt is imported
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime

class StopwatchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint) # Keep the window on top
        self.setWindowTitle("Time Attack Stopwatch-v1.1")
        self.resize(420, 420)
        self.init_ui()
        self.reset_all()
        self.countdown_timer = QTimer(self)
        self.countdown_seconds = 0

    def init_ui(self):
        layout = QVBoxLayout()

        # Top section with timer and trial box
        top_layout = QHBoxLayout()
        
        # Timer display
        self.time_label = QLabel("00:00.0")
        self.time_label.setStyleSheet("font-size: 34px; text-align: center;")
        top_layout.addWidget(self.time_label)
        
        # Trial number box - square shape
        self.trial_box = QLabel("#1")
        self.trial_box.setAlignment(Qt.AlignCenter)
        self.trial_box.setFixedSize(60, 60)  # Fixed square size
        self.trial_box.setStyleSheet("""
            background-color: black;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 5px;
            qproperty-alignment: AlignCenter;
        """)
        self.trial_box.setFrameStyle(QFrame.Box)
        top_layout.addWidget(self.trial_box)

        top_layout.setAlignment(self.trial_box, Qt.AlignLeft) # center Qt.AlignCenter if you want to move it to the right just delete this line
        
        layout.addLayout(top_layout)

        input_layout = QHBoxLayout()
        self.trial_input = QSpinBox()
        self.trial_input.setRange(1, 100)
        self.trial_input.setValue(3)
        input_layout.addWidget(QLabel("Trials:"))
        input_layout.addWidget(self.trial_input)
        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.toggle_stopwatch)
        button_layout.addWidget(self.start_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.record_trial)
        self.next_button.setToolTip("Press Enter key") # Hint shown on hover
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_all)
        button_layout.addWidget(self.reset_button)

        layout.addLayout(button_layout)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("font-size: 18px; text-align: left;")
        layout.addWidget(self.result_area)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

    def keyPressEvent(self, event):
        """Handles key press events for the window."""
        # Check if the pressed key is Enter (Return) or the numpad Enter
        # Also check if the 'Next' button is currently enabled
        if (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter) and self.next_button.isEnabled():
            self.record_trial() # Call the same function as clicking the Next button
        else:
            # Important: Pass the event to the parent class's handler
            # if it's not the key we're interested in, or if the button is disabled.
            super().keyPressEvent(event)

    def toggle_stopwatch(self):
        if not self.running:
            self.reset_all()
            self.total_trials = self.trial_input.value()
            self.current_trial = 1
            self.update_trial_box()  # Update the trial box to show #1
            self.prepare_next_trial()  # Use countdown before first trial
            self.start_button.setText("End")
        else:
            self.finish_trials()
            self.start_button.setText("Start")

    def start_stopwatch(self):
        self.reset_all()
        self.total_trials = self.trial_input.value()
        self.running = True
        self.current_trial = 1
        self.update_trial_box()  # Update the trial box to show #1
        self.start_time = time.time()
        self.timer.start(100)
        self.result_area.append(f"Trial {self.current_trial} running...")
        self.next_button.setEnabled(True)
        self.trial_input.setEnabled(False)

    def update_time(self):
        if self.running:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            tenths = int((elapsed * 10) % 10)
            self.time_label.setText(f"{minutes:02}:{seconds:02}.{tenths}")

    def update_trial_box(self):
        """Updates the trial box to show the current trial number."""
        self.trial_box.setText(f"#{self.current_trial}")

    def flash_next_button(self):
        self.next_button.setStyleSheet("background-color: yellow; font-weight: bold;")
        QTimer.singleShot(200, lambda: self.next_button.setStyleSheet(""))

    def record_trial(self):
        if not self.running:
            return

        elapsed = time.time() - self.start_time
        default_label = f"Trial {self.current_trial}"
        self.labels.append(default_label)
        self.trials.append(elapsed)
        self.result_area.append(f"{default_label}: {elapsed:.2f} sec")

        if self.current_trial >= self.total_trials:
            self.finish_trials()
        else:
            self.current_trial += 1
            self.update_trial_box()  # Update the trial box with the new number
            self.prepare_next_trial()

    def prepare_next_trial(self):
        self.running = False
        self.next_button.setEnabled(False)
        self.start_button.setEnabled(False)
        self.countdown_seconds = 5
        self.result_area.append(f"starts in: {self.countdown_seconds}")
        self.timer.stop()
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.countdown_timer.start(1000)

    def update_countdown(self):
        self.countdown_seconds -= 1

        # Get current text and remove the last line
        cursor = self.result_area.textCursor()
        cursor.movePosition(cursor.End)
        cursor.select(cursor.LineUnderCursor)
        cursor.removeSelectedText()

        # Remove any extra newlines that might be created
        text = self.result_area.toPlainText().rstrip()
        self.result_area.setPlainText(text)

        if self.countdown_seconds > 0:
            # Show the new countdown number
            self.result_area.append(f"{self.countdown_seconds}")
        else:
            self.countdown_timer.stop()
            self.result_area.append("START!")
            self.running = True
            self.start_time = time.time()
            self.result_area.append(f"Trial {self.current_trial} running...")
            self.timer.start(100)
            self.next_button.setEnabled(True)
            self.start_button.setEnabled(True)
            # Ensure the main window has focus to capture key events after countdown
            self.setFocus()

    def finish_trials(self):
        self.running = False
        self.timer.stop()
        if hasattr(self, 'countdown_timer') and self.countdown_timer.isActive():
            self.countdown_timer.stop()

        self.result_area.append("--- Trials completed ---")

        if self.trials:
            avg_time = sum(self.trials) / len(self.trials)
            self.result_area.append(f"Average time: {avg_time:.2f} sec")

        self.save_to_csv()

        self.start_button.setText("Start")
        self.next_button.setEnabled(False)
        self.trial_input.setEnabled(True)

    def reset_all(self):
        self.timer.stop()
        if hasattr(self, 'countdown_timer') and self.countdown_timer.isActive():
            self.countdown_timer.stop()
        self.running = False
        self.trials = []
        self.labels = []
        self.current_trial = 1
        self.update_trial_box()  # Reset the trial box to show #1
        self.time_label.setText("00:00.0")
        self.result_area.clear()

        self.start_button.setText("Start")
        self.start_button.setEnabled(True)  # Enable the start button
        self.next_button.setEnabled(False)
        self.trial_input.setEnabled(True)
        # Set focus to the main window on reset
        self.setFocus()

    def save_to_csv(self):
        try:
            current_date = datetime.now().strftime("%y-%m-%d")
            with open("stopwatch_results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Label", "Date", "time(s)"])
                for label, t in zip(self.labels, self.trials):
                    writer.writerow([label, current_date, f"{t:.2f}"])
            self.result_area.append("Results saved to stopwatch_results.csv")
        except Exception as e:
            self.result_area.append(f"Error saving results: {str(e)}")

    def refresh_result_area(self):
        self.result_area.clear()
        for label, t in zip(self.labels, self.trials):
            self.result_area.append(f"{label}: {t:.2f} sec")

        if self.labels and not self.running:
            self.result_area.append("--- Trials completed ---")
            avg_time = sum(self.trials) / len(self.trials)
            self.result_area.append(f"Average time: {avg_time:.2f} sec")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StopwatchApp()
    win.show()
    # Ensure the window has focus when it starts
    win.setFocus()
    sys.exit(app.exec_())