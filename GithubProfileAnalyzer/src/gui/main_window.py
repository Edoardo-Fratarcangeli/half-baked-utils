import os
import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QDialog, QFormLayout,
    QSpinBox
)
from PyQt5.QtCore import Qt

from ..client import GitHubClient
from ..analysis import process_profile_data
from ..utils.pdf_exporter import generate_pdf
from ..utils.git_helper import get_user_info, get_git_token
from .components import AnalysisChartCanvas

class SettingsDialog(QDialog):
    def __init__(self, parent=None, name="", site="", target="", threshold=3):
        super().__init__(parent)
        self.setWindowTitle("Analysis Settings")
        self.setModal(True)
        self.resize(800, 200)

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.name_input = QLineEdit(name)
        self.site_input = QLineEdit(site)
        self.target_input = QLineEdit(target)
        self.threshold_input = QSpinBox()
        self.threshold_input.setRange(0, 100)
        self.threshold_input.setValue(threshold)
        self.threshold_input.setSuffix("%")

        form_layout.addRow("Author Name:", self.name_input)
        form_layout.addRow("Website:", self.site_input)
        form_layout.addRow("Target Role:", self.target_input)
        form_layout.addRow("Others Threshold:", self.threshold_input)

        layout.addLayout(form_layout)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def get_values(self):
        return (
            self.name_input.text().strip(),
            self.site_input.text().strip(),
            self.target_input.text().strip(),
            self.threshold_input.value()
        )

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GitHub Developer Profile Analyzer")

        # Attempt to get token from Env or Git Credential
        self.token = os.getenv("GITHUB_TOKEN") or get_git_token()
        
        if not self.token:
            QMessageBox.warning(
                self, "Warning",
                "No GitHub Token found (Env or Git Credential).\n"
                "Analysis might fail without a configured token."
            )

        self.client = GitHubClient(self.token) if self.token else None
        self.df = None
        self.commit_total = 0

        # Settings storage
        self.author_name = ""
        self.author_site = ""
        self.target_role = ""
        self.threshold = 3

        self._build_ui()
        self._prefill_settings()

    def _build_ui(self):
        layout = QVBoxLayout()

        # --- Top Bar: Settings + URL Input ---
        top_bar = QHBoxLayout()

        # Settings Button
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setToolTip("Settings (Author, Target Role)")
        self.settings_btn.clicked.connect(self.open_settings)
        top_bar.addWidget(self.settings_btn)

        # URL Input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter GitHub URL (e.g. https://github.com/torvalds)")
        top_bar.addWidget(self.url_input)

        layout.addLayout(top_bar)

        # --- Action Buttons ---
        buttons = QHBoxLayout()

        self.analyze_btn = QPushButton("Analyze Profile")
        self.analyze_btn.clicked.connect(self.analyze)

        self.export_btn = QPushButton("Export PDF")
        self.export_btn.clicked.connect(self.export_pdf)
        self.export_btn.setEnabled(False)

        buttons.addWidget(self.analyze_btn)
        buttons.addWidget(self.export_btn)

        layout.addLayout(buttons)

        # Summary
        self.summary_label = QLabel("No profile analyzed")
        layout.addWidget(self.summary_label)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Language", "Bytes", "Percentage"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        layout.addWidget(self.table)

        # Chart
        self.chart = AnalysisChartCanvas()
        layout.addWidget(self.chart)

        self.setLayout(layout)

    def _prefill_settings(self):
        """Pre-load settings from local git config"""
        info = get_user_info()
        self.author_name = info["name"] if info["name"] else ""
        self.author_site = info["email"] if info["email"] else "" # Use email as fallback for site
        # Target role defaults to empty

    def open_settings(self):
        dialog = SettingsDialog(
            self, 
            name=self.author_name, 
            site=self.author_site, 
            target=self.target_role,
            threshold=self.threshold
        )
        if dialog.exec_() == QDialog.Accepted:
            self.author_name, self.author_site, self.target_role, self.threshold = dialog.get_values()

    def analyze(self):
        if not self.client:
             QMessageBox.critical(self, "Token Error", "Token not configured. Cannot analyze.")
             return

        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a URL or username.")
            return

        # Extract username from URL
        username = url
        if "github.com/" in url:
            try:
                username = url.split("github.com/")[-1].strip("/")
            except IndexError:
                pass
        
        # Check if settings are adequately filled (optional, but good for PDF)
        # We allow analyzing without them, but maybe warn? 
        # Requirement said: "l'autore della ricerca non si deve vedere nalla gui, ma solo in impostazioni"
        # So we just use what we have.

        try:
            raw = self.client.fetch_profile(username)
        except Exception as e:
            QMessageBox.critical(self, "API Error", str(e))
            return

        self.df, self.commit_total = process_profile_data(raw)

        if self.df is None or self.df.empty:
            QMessageBox.warning(self, "No Useful Data", "Empty profile or data error")
            return

        # Update labels
        display_target = self.target_role if self.target_role else "N/A"
        display_author = self.author_name if self.author_name else "Guest"
        
        self.summary_label.setText(
            f"Analysis of {username} (by {display_author}) | Target: {display_target} | Commit: {self.commit_total}"
        )

        self.table.setRowCount(len(self.df))
        for row, (_, r) in enumerate(self.df.iterrows()):
            self.table.setItem(row, 0, QTableWidgetItem(r["language"]))
            self.table.setItem(row, 1, QTableWidgetItem(str(int(r["bytes"]))))
            self.table.setItem(
                row, 2, QTableWidgetItem(f"{r['percentage']:.2f}%")
            )

        self.chart.plot_languages(self.df, username, threshold=self.threshold)
        self.export_btn.setEnabled(True)

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "", "PDF (*.pdf)"
        )
        if not path:
            return

        tmp_chart = "chart_tmp.png"
        self.chart.save_png(tmp_chart)
        
        # Determine username again (store it?)
        # For simplicity, re-extract or store in analyze.
        # Let's just re-extract from UI or better, store `current_username`
        # But `self.chart` has the username context mostly.
        # Let's re-extract since `analyze` does it simply.
        url = self.url_input.text().strip()
        username = url
        if "github.com/" in url:
             username = url.split("github.com/")[-1].strip("/")

        data = {
            'name': self.author_name,
            'site': self.author_site,
            'username': username,
            'target': self.target_role,
            'commit_total': self.commit_total,
            'df': self.df,
            'threshold': self.threshold
        }

        try:
            generate_pdf(data, tmp_chart, path)
            QMessageBox.information(self, "PDF Created", "Export completed successfully")
        except Exception as e:
             QMessageBox.critical(self, "Export Error", str(e))
        finally:
            if os.path.exists(tmp_chart):
                os.remove(tmp_chart)
