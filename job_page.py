from PyQt6.QtWidgets import (
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QHeaderView, QMessageBox
)
import job_db_functions as jf
from forms import JobForm
import mysql.connector

class JobPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Top buttons
        button_layout = QHBoxLayout()
        add_job_btn = QPushButton("Add Job")
        jobs_in_progress_btn = QPushButton("Jobs in Progress")
        completed_jobs_btn = QPushButton("Completed Jobs")
        finish_job_btn = QPushButton("Finish a Job")
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_main_page)

        for btn in [add_job_btn, jobs_in_progress_btn, completed_jobs_btn, finish_job_btn]:
            btn.setFixedHeight(100)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 20px;
                background-color: #D37F3A;
                color: white;
                border: 2px solid #8E5724;
                font-weight: bold;
            """)

        add_job_btn.clicked.connect(self.add_job)
        jobs_in_progress_btn.clicked.connect(self.show_jobs_in_progress_page)
        completed_jobs_btn.clicked.connect(self.show_completed_jobs_page)
        finish_job_btn.clicked.connect(self.show_finish_job_page)

        button_layout.addWidget(add_job_btn)
        button_layout.addWidget(jobs_in_progress_btn)
        button_layout.addWidget(completed_jobs_btn)
        button_layout.addWidget(finish_job_btn)
        self.layout.addWidget(back_button)
        self.layout.addLayout(button_layout)

        # Job table
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(9)
        self.job_table.setHorizontalHeaderLabels(["Job ID", "Vehicle ID", "Technician ID", "Job Type", "Start Date", "End Date", "Job Amount", "Hours", "Status"])
        self.job_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.job_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.job_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with jobs
        self.populate_jobs()

    def populate_jobs(self):
        self.job_table.setRowCount(0)
        try:
            rows = jf.read_technicians()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.job_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.job_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def add_job(self):
        form = JobForm(self)  # Using JobForm for job data input
        if form.exec():
            job_data = form.get_job_data()
            jf.add_job(job_data['plate_num'], job_data['problem_description'], job_data['start_date'])
            self.populate_jobs()

    def show_jobs_in_progress_page(self):
        jobs_in_progress_page = JobsInProgressPage(self.main_app, self)
        self.main_app.stack.addWidget(jobs_in_progress_page)
        self.main_app.stack.setCurrentWidget(jobs_in_progress_page)

    def show_completed_jobs_page(self):
        completed_jobs_page = CompletedJobsPage(self.main_app, self)
        self.main_app.stack.addWidget(completed_jobs_page)
        self.main_app.stack.setCurrentWidget(completed_jobs_page)

    def show_finish_job_page(self):
        finish_job_page = FinishJobPage(self.main_app, self)
        self.main_app.stack.addWidget(finish_job_page)
        self.main_app.stack.setCurrentWidget(finish_job_page)

    def show_main_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.main_page)

class JobsInProgressPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_job_page)
        self.layout.addWidget(back_button)

        # Job table
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(7)
        self.job_table.setHorizontalHeaderLabels(["Customer Name", "Vehicle Make", "Plate Number", "Problem Description", "Start Date", "Hours", "Job Amount"])
        self.job_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.job_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.job_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with jobs in progress
        self.populate_jobs_in_progress()

    def populate_jobs_in_progress(self):
        self.job_table.setRowCount(0)
        try:
            rows = jf.view_jobs_in_progress()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.job_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.job_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def show_job_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.job_page)

class CompletedJobsPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_job_page)
        self.layout.addWidget(back_button)

        # Job table
        self.job_table = QTableWidget()
        self.job_table.setColumnCount(8)
        self.job_table.setHorizontalHeaderLabels(["Customer Name", "Vehicle Make", "Plate Number", "Problem Description", "Start Date", "End Date", "Job Amount", "Hours"])
        self.job_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.job_table.horizontalHeader().setStretchLastSection(True)

        self.layout.addWidget(self.job_table)
        self.layout.setStretch(1, 1)  # Ensure the table occupies the remaining space

        # Populate table with completed jobs
        self.populate_completed_jobs()

    def populate_completed_jobs(self):
        self.job_table.setRowCount(0)
        try:
            rows = jf.view_jobs_completed()
            if rows:
                for row_index, row_data in enumerate(rows):
                    self.job_table.insertRow(row_index)
                    for column_index, data in enumerate(row_data):
                        self.job_table.setItem(row_index, column_index, QTableWidgetItem(str(data)))
        except mysql.connector.Error as e:
            print(f"Database error: {e}")

    def show_job_page(self):
        self.main_app.stack.setCurrentWidget(self.main_app.job_page)

class FinishJobPage(QWidget):
    def __init__(self, main_app, parent=None):
        super().__init__(parent)
        self.main_app = main_app
        self.layout = QVBoxLayout(self)

        # Back button
        back_button = QPushButton("🔙 Back")
        back_button.setFixedHeight(50)
        back_button.setStyleSheet("""
            font-size: 18px;
            padding: 10px;
            background-color: #D37F3A;
            color: white;
            border: 2px solid #8E5724;
            font-weight: bold;
        """)
        back_button.clicked.connect(self.show_job_page)
        self.layout.addWidget(back_button)

        # Job form to finish job
        finish_job_form = JobForm(self)
        if finish_job_form.exec():
            job_data = finish_job_form.get_job_data()
            try:
                jf.finish_job(
                    plate_num=job_data['plate_num'],
                    problem_description=job_data['problem_description'],
                    Technician_assigned=job_data['technician'],
                    end_date=job_data['end_date'],
                    new_status=job_data['status']
                )
                QMessageBox.information(self, "Success", "Job marked as finished!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to finish job: {e}")

