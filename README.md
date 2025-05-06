# Time Attack Stopwatch
A PyQt5-based desktop application for timing multiple trials, ideal for speed-based challenges like timed tests and competitive tasks.
The app features a clean interface with a stopwatch, trial counter, countdown timer, and result logging, making it ideal for tracking performance across repeated attempts.
Features

Stopwatch Timer: Displays elapsed time in MM:SS.t format (minutes, seconds, tenths of a second) with real-time updates every 100ms.
Trial Management: Supports multiple trials (1 to 100) with a configurable trial count via a spin box. Tracks current trial number in a bold, square display box.
Countdown Timer: Initiates each trial with a 5-second countdown, enhancing readiness for timed challenges.
Next Trial Trigger: Record trial times using the "Next" button or by pressing the Enter key, with a visual flash effect on the button for feedback.
Result Logging: Displays trial times in a read-only text area, including labels and elapsed times. Calculates and shows the average time upon completion.
CSV Export: Saves trial results (labels, dates, and times) to a stopwatch_results.csv file for external analysis.
Label Editing: Allows post-trial renaming of trial labels through a dialog for customized result descriptions.
Reset Functionality: Resets the timer, trial count, and results with a single button, restoring the app to its initial state.
Keyboard Support: Enables recording trial times with the Enter key when the "Next" button is active, improving usability.
Responsive UI: Features a polished layout with aligned elements, tooltips (e.g., on the "Next" button), and focus management for seamless interaction.

Usage

Launch the app to see the main window with a stopwatch, trial counter, and control buttons.
Set the desired number of trials using the spin box (default: 3).
Click "Start" to begin the first trial, which triggers a 5-second countdown.
Press "Next" or the Enter key to record the current trial's time and proceed to the next trial.
After completing all trials, view results in the text area, including the average time.
Edit trial labels using the "Edit Labels" button or reset the app with the "Reset" button.
Results are automatically saved to stopwatch_results.csv in the working directory.

Requirements

Python 3.x
PyQt5 (pip install pyqt5)

Installation

Clone the repository:git clone https://github.com/yourusername/time-attack-stopwatch.git


Install dependencies:pip install pyqt5


Run the app:python Time_Attack_timer_v04.py



License
This project is licensed under the MIT License.
