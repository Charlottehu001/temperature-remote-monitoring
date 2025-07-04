import sys
import json
from datetime import datetime
from collections import deque
import csv
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QListWidgetItem, QVBoxLayout, QTableView, QHeaderView, QPushButton, QHBoxLayout, QSizePolicy, QFileDialog
from PySide6.QtCore import QThread, Signal, QTimer, QStringListModel, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPainter, QBrush, QColor, QPalette, QIcon
import paho.mqtt.client as mqtt
import sqlite3
from ui.Ui_Main import Ui_Form
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation

class TemperatureChart(FigureCanvas):
    def __init__(self, title, parent=None):
        self.fig = Figure(figsize=(8, 6), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.ax = self.fig.add_subplot(111)
        self.title = title
        
        # Data buffer, stores up to 512 data points
        self.data_buffer = deque(maxlen=512)
        self.time_buffer = deque(maxlen=512)
        
        # Detect system theme and apply styles
        self.apply_theme_style()
        
        # Adjust subplot parameters, increase margins to avoid label clipping
        self.fig.subplots_adjust(left=0.2, bottom=0.15, right=0.9, top=0.9)
        
        # Auto adjust layout
        self.fig.tight_layout(pad=2.0)
    
    def is_dark_theme(self):
        """Detect if system is using dark theme"""
        app = QApplication.instance()
        if app:
            palette = app.palette()
            # Check window background color brightness
            bg_color = palette.color(QPalette.ColorRole.Window)
            # Calculate brightness (0-255)
            brightness = (bg_color.red() * 0.299 + bg_color.green() * 0.587 + bg_color.blue() * 0.114)
            return brightness < 128  # If brightness < 128, consider it dark theme
        return False
    
    def apply_theme_style(self):
        """Apply chart styles based on system theme"""
        is_dark = self.is_dark_theme()
        
        if is_dark:
            # Dark theme styles
            bg_color = '#2b2b2b'  # Dark gray background
            text_color = 'white'
            line_color = 'white'
            grid_color = '#555555'
        else:
            # Light theme styles
            bg_color = 'white'
            text_color = 'black'
            line_color = 'black'
            grid_color = '#cccccc'
        
        # Set chart styles
        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)
        
        # Set title and labels
        self.ax.set_title(self.title, fontsize=8, color=text_color)
        self.ax.set_ylabel('Temperature (°C)', fontsize=8, color=text_color)
        
        # Set axis colors
        self.ax.tick_params(axis='both', which='major', labelsize=7, colors=text_color)
        self.ax.spines['bottom'].set_color(text_color)
        self.ax.spines['top'].set_color(text_color)
        self.ax.spines['right'].set_color(text_color)
        self.ax.spines['left'].set_color(text_color)
        
        # Set grid
        self.ax.set_ylim(0, 80)  # Set Y-axis default range 0-80
        self.ax.grid(True, alpha=0.3, color=grid_color)
        
        # Initialize empty line
        self.line, = self.ax.plot([], [], color=line_color, linewidth=2)
    
    def add_data_point(self, timestamp, temperature):
        """Add new data point"""
        self.time_buffer.append(timestamp)
        self.data_buffer.append(temperature)
        self.update_plot()
    
    def update_plot(self):
        """Update chart display"""
        if len(self.data_buffer) > 0:
            # Update line data
            self.line.set_data(list(self.time_buffer), list(self.data_buffer))
            
            # Auto adjust axis range
            if len(self.time_buffer) > 1:
                self.ax.set_xlim(min(self.time_buffer), max(self.time_buffer))
            
            # Y-axis maintains 0-80 range unless data exceeds range
            if len(self.data_buffer) > 0:
                data_min = min(self.data_buffer)
                data_max = max(self.data_buffer)
                y_min = min(0, data_min - 2)
                y_max = max(80, data_max + 2)
                self.ax.set_ylim(y_min, y_max)
            
            # Hide horizontal axis time display
            if len(self.time_buffer) > 1:
                self.ax.set_xticklabels([])  # Hide X-axis labels
            
            # Redraw chart
            self.draw()
    
    def clear_data(self):
        """Clear data buffer"""
        self.data_buffer.clear()
        self.time_buffer.clear()
        self.line.set_data([], [])
        self.ax.clear()
        
        # Reapply theme styles
        self.apply_theme_style()
        
        # Reapply layout adjustments
        self.fig.subplots_adjust(left=0.2, bottom=0.15, right=0.9, top=0.9)
        self.fig.tight_layout(pad=2.0)
        
        self.draw()

class DatabaseManager:
    def __init__(self, db_name='fire_records.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        self.connect()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fire_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                min_temp REAL NOT NULL,
                max_temp REAL NOT NULL,
                center_temp REAL NOT NULL,
                fire_detected BOOLEAN NOT NULL,
                mode TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        self.close()

    def log_fire_event(self, timestamp, min_temp, max_temp, center_temp, fire_detected, mode):
        self.connect()
        self.cursor.execute('''
            INSERT INTO fire_events (timestamp, min_temp, max_temp, center_temp, fire_detected, mode)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, min_temp, max_temp, center_temp, fire_detected, mode))
        self.conn.commit()
        self.close()

    def get_all_fire_events(self, fire_detected_filter=None):
        self.connect()
        query = 'SELECT id, timestamp, min_temp, max_temp, center_temp, fire_detected, mode FROM fire_events'
        params = []
        if fire_detected_filter is not None:
            query += ' WHERE fire_detected = ?'
            params.append(fire_detected_filter)
        query += ' ORDER BY id'
        self.cursor.execute(query, params)
        records = self.cursor.fetchall()
        self.close()
        return records

class MQTTClient(QThread):
    # Signal definitions
    message_received = Signal(str, str)  # topic, message
    connection_status = Signal(bool, str)  # connected, message
    
    def __init__(self):
        super().__init__()
        self.client = None
        self.is_connected = False
        self.subscriptions = set()
        
    def connect_to_broker(self, protocol, host, port, client_id, username, password):
        try:
            # 创建MQTT客户端
            if protocol in ['ws://', 'wss://']:
                self.client = mqtt.Client(client_id=client_id, transport="websockets")
            else:
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
            
            # 设置用户名和密码
            if username and password:
                self.client.username_pw_set(username, password)
            
            # 设置回调函数
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            # 连接到代理
            if protocol in ['mqtts://', 'wss://']:
                self.client.tls_set()
            
            self.client.connect(host, int(port), 60)
            self.client.loop_start()
            
        except Exception as e:
            self.connection_status.emit(False, f"Connection failed: {str(e)}")
    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            self.is_connected = True
            self.connection_status.emit(True, "Connected successfully")
            # Re-subscribe to all topics
            for topic in self.subscriptions:
                self.subscribe_topic(topic)
        else:
            self.is_connected = False
            self.connection_status.emit(False, f"Connection failed, error code: {reason_code}")
    
    def on_disconnect(self, client, userdata, disconnect_flags, reason_code, properties):
        self.is_connected = False
        self.connection_status.emit(False, "Connection disconnected")
    
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        message = msg.payload.decode('utf-8')
        self.message_received.emit(topic, message)
    
    def subscribe_topic(self, topic):
        if self.client and self.is_connected:
            self.client.subscribe(topic)
            self.subscriptions.add(topic)
            return True
        return False
    
    def publish_message(self, topic, message):
        if self.client and self.is_connected:
            self.client.publish(topic, message)
            return True
        return False
    
    def disconnect_from_broker(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

class MQTTDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Set window icon
        self.setWindowIcon(QIcon("ui/Logo.png"))
        
        # MQTT client
        self.mqtt_client = MQTTClient()
        self.mqtt_client.message_received.connect(self.on_message_received)
        self.mqtt_client.connection_status.connect(self.on_connection_status_changed)
        
        # Subscription list model
        self.subscription_model = QStandardItemModel()
        self.ui.listView_Subscription.setModel(self.subscription_model)
        
        # Topic dropdown model
        self.topic_model = QStringListModel()
        self.ui.comboBox_Subscription.setModel(self.topic_model)
        
        # Connect signals and slots
        self.setup_connections()
        
        # Load connection settings or set default values
        self.load_connection_settings()
        
        # Set English interface text
        self.setup_english_ui()
        
        # Set status indicator
        self.setup_state_widget()
        
        # Set database
        self.db_manager = DatabaseManager()
        self.db_manager.create_table()
        self.setup_record_table()
        self.load_fire_records()

        # Set temperature charts
        self.setup_temperature_charts()
        
        # Auto subscribe to default topics
        self.auto_subscribe_default_topics()
        
        # Monitor system theme changes (optional)
        self.setup_theme_monitoring()
    
    def setup_connections(self):
        # Connect button
        self.ui.pushButton_Open.clicked.connect(self.toggle_connection)
        
        # Add subscription button
        self.ui.pushButton_AddSubscription.clicked.connect(self.add_subscription)
        
        # Send button
        self.ui.pushButton_Send.clicked.connect(self.send_message)
        
        # Subscribe input box enter event
        self.ui.lineEdit_Subscription.returnPressed.connect(self.add_subscription)
        
        # Send text box enter event (Ctrl+Enter)
        self.ui.textEdit_Send.installEventFilter(self)
        
        # Page 2 configuration related signal slots
        self.ui.comboBox_model.currentIndexChanged.connect(self.on_config_changed)
        self.ui.doubleSpinBox_1.valueChanged.connect(self.on_config_changed)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.on_config_changed)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.on_config_changed)
        self.ui.doubleSpinBox_4.valueChanged.connect(self.on_config_changed)
        self.ui.doubleSpinBox_5.valueChanged.connect(self.on_config_changed)
    
    def load_connection_settings(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.ui.lineEdit_Address.setText(config.get('host', 'www.duruofu.top'))
                self.ui.lineEdit_2.setText(config.get('port', '1883'))
                self.ui.lineEdit_6.setText(config.get('client_id', 'PySide6_MQTT_Client'))
                self.ui.lineEdit_UserName.setText(config.get('username', 'admin'))
                self.ui.lineEdit_5.setText(config.get('password', '123456'))
        except (FileNotFoundError, json.JSONDecodeError):
            self.setup_default_values()

    def save_connection_settings(self):
        config = {
            'host': self.ui.lineEdit_Address.text(),
            'port': self.ui.lineEdit_2.text(),
            'client_id': self.ui.lineEdit_6.text(),
            'username': self.ui.lineEdit_UserName.text(),
            'password': self.ui.lineEdit_5.text(),
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)

    def setup_default_values(self):
        # Set default connection parameters
        self.ui.lineEdit_Address.setText("www.duruofu.top")
        self.ui.lineEdit_2.setText("1883")
        self.ui.lineEdit_6.setText("PySide6_MQTT_Client")
        self.ui.lineEdit_UserName.setText("admin")
        self.ui.lineEdit_5.setText("123456")
        
        # Set page 2 default values
        self.ui.comboBox_model.setCurrentIndex(0)  # Threshold mode
        self.ui.doubleSpinBox_1.setValue(35.0)
        self.ui.doubleSpinBox_2.setValue(0.8)
        self.ui.doubleSpinBox_3.setValue(45.0)
        self.ui.doubleSpinBox_4.setValue(0.6)
        self.ui.doubleSpinBox_5.setValue(60.0)
    
    def setup_english_ui(self):
        """Set English text for UI elements"""
        # Set window title
        self.setWindowTitle("Fire Detection")
        
        # Page 1 - MQTT connection configuration
        self.ui.groupBox_Port.setTitle("MQTT Connection Configuration")
        self.ui.label.setText("Server: ")
        self.ui.label_2.setText("Port: ")
        self.ui.label_ClientID.setText("Client ID:")
        self.ui.label_4.setText("Username: ")
        self.ui.label_PassWord.setText("Password: ")
        self.ui.pushButton_Open.setText("Connect")
        
        # Page 1 - Subscription list
        self.ui.groupBox_2.setTitle("Subscription List")
        self.ui.label_3.setText("Add Subscription:")
        self.ui.pushButton_AddSubscription.setText("Add")
        
        # Page 1 - Message sending
        self.ui.groupBox_4.setTitle("Message Send")
        self.ui.label_7.setText("Topic:")
        self.ui.pushButton_Send.setText("Send")
        
        # Page 1 - Message receiving
        self.ui.groupBox_3.setTitle("Message Receive")
        
        # Page 2 - Parameter configuration
        self.ui.groupBox_5.setTitle("Parameter Configuration")
        self.ui.label_6.setText("Mode:")
        self.ui.label_9.setText("Threshold 1:")
        self.ui.label_10.setText("Threshold 2:")
        self.ui.label_11.setText("Threshold 3:")
        self.ui.label_12.setText("Threshold 4:")
        self.ui.label_13.setText("Threshold 5:")
        
        # Set tab titles
        self.ui.tabWidget.setTabText(0, "Connection/Debug")
        self.ui.tabWidget.setTabText(1, "Info/Control")
        self.ui.tabWidget.setTabText(2, "Record")
        
        # Page 2 - Detection results
        self.ui.groupBox.setTitle("Detection Result")
        self.ui.label_14.setText("Min Temp:")
        self.ui.label_15.setText("Max Temp:")
        self.ui.label_16.setText("Center Temp:")
        
        # Page 2 - Real-time data
        self.ui.groupBox_6.setTitle("Real-time Data")
    
    def setup_state_widget(self):
        """Setup state indicator widget"""
        self.fire_detected = False
        self.ui.widget_state.paintEvent = self.paint_state_indicator
    
    def setup_record_table(self):
        self.record_model = QStandardItemModel(0, 7)
        self.record_model.setHorizontalHeaderLabels(['ID', 'Timestamp', 'Min Temp', 'Max Temp', 'Center Temp', 'Fire Detected', 'Mode'])
        self.ui.tableView.setModel(self.record_model)
        self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableView.verticalHeader().setVisible(False)

        # Add buttons
        button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear Table")
        self.filter_fire_button = QPushButton("Filter Fire Events")
        self.show_all_button = QPushButton("Show All")
        self.export_button = QPushButton("Export to CSV")

        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.filter_fire_button)
        button_layout.addWidget(self.show_all_button)
        button_layout.addWidget(self.export_button)

        # Get the layout of tab_3 and add the button layout
        tab_layout = self.ui.tab_3.layout()
        if tab_layout:
            tab_layout.addLayout(button_layout)

        # Connect buttons to slots
        self.clear_button.clicked.connect(self.clear_table)
        self.filter_fire_button.clicked.connect(self.filter_fire_events)
        self.show_all_button.clicked.connect(self.show_all_records)
        self.export_button.clicked.connect(self.export_to_csv)

    def load_fire_records(self, fire_detected_filter=None):
        records = self.db_manager.get_all_fire_events(fire_detected_filter)
        self.record_model.setRowCount(0)
        for row_data in records:
            items = []
            for i, field in enumerate(row_data):
                item = QStandardItem()
                if i == 5:  # fire_detected column
                    is_fire = bool(field)
                    item.setText("Yes" if is_fire else "No")
                    item.setForeground(QBrush(QColor("red")) if is_fire else QBrush(QColor("green")))
                else:
                    item.setText(str(field))
                item.setTextAlignment(Qt.AlignCenter)
                items.append(item)
            self.record_model.appendRow(items)

    def clear_table(self):
        self.db_manager.connect()
        self.db_manager.cursor.execute('DELETE FROM fire_events')
        self.db_manager.conn.commit()
        self.db_manager.close()
        self.load_fire_records()

    def filter_fire_events(self):
        self.load_fire_records(fire_detected_filter=True)

    def show_all_records(self):
        self.load_fire_records()

    def export_to_csv(self):
        records = self.db_manager.get_all_fire_events()
        if not records:
            QMessageBox.information(self, "Info", "No data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write header
                    header = [self.record_model.horizontalHeaderItem(i).text() for i in range(self.record_model.columnCount())]
                    writer.writerow(header)
                    # Write data
                    writer.writerows(records)
                QMessageBox.information(self, "Success", "Data exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export data: {e}")

    def setup_temperature_charts(self):
        """Setup temperature charts for the three widgets"""
        # Create three temperature charts
        self.chart_min_temp = TemperatureChart("Min Temperature", self.ui.widget_chart1)
        self.chart_max_temp = TemperatureChart("Max Temperature", self.ui.widget_chart2)
        self.chart_center_temp = TemperatureChart("Center Temperature", self.ui.widget_chart3)
        
        # Set layout for each widget and add charts
        layout1 = QVBoxLayout(self.ui.widget_chart1)
        layout1.addWidget(self.chart_min_temp)
        layout1.setContentsMargins(0, 0, 0, 0)
        self.ui.widget_chart1.setLayout(layout1)
        
        layout2 = QVBoxLayout(self.ui.widget_chart2)
        layout2.addWidget(self.chart_max_temp)
        layout2.setContentsMargins(0, 0, 0, 0)
        self.ui.widget_chart2.setLayout(layout2)
        
        layout3 = QVBoxLayout(self.ui.widget_chart3)
        layout3.addWidget(self.chart_center_temp)
        layout3.setContentsMargins(0, 0, 0, 0)
        self.ui.widget_chart3.setLayout(layout3)
    
    def setup_theme_monitoring(self):
        """Setup theme monitoring (optional feature)"""
        # Create timer to periodically check theme changes
        self.theme_timer = QTimer()
        self.theme_timer.timeout.connect(self.check_theme_change)
        self.theme_timer.start(5000)  # Check every 5 seconds
        
        # Record current theme state
        self.current_dark_theme = self.chart_min_temp.is_dark_theme()
    
    def check_theme_change(self):
        """Check if theme has changed"""
        new_dark_theme = self.chart_min_temp.is_dark_theme()
        if new_dark_theme != self.current_dark_theme:
            self.current_dark_theme = new_dark_theme
            self.refresh_chart_themes()
    
    def refresh_chart_themes(self):
        """Refresh theme styles for all charts"""
        self.chart_min_temp.apply_theme_style()
        self.chart_max_temp.apply_theme_style()
        self.chart_center_temp.apply_theme_style()
        
        # Redraw charts
        self.chart_min_temp.draw()
        self.chart_max_temp.draw()
        self.chart_center_temp.draw()
    
    def paint_state_indicator(self, event):
        """Paint state indicator on widget_state"""
        painter = QPainter(self.ui.widget_state)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget dimensions
        rect = self.ui.widget_state.rect()
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        radius = min(center_x, center_y) - 5
        
        # Set color and text based on fire detection status
        if self.fire_detected:
            color = QColor(220, 80, 80)  # Soft red
            text = "FIRE"
        else:
            color = QColor(80, 200, 80)  # Soft green
            text = "NORMAL"
        
        # Draw circular background
        painter.setBrush(QBrush(color))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
        
        # Draw text
        painter.setPen(QColor(255, 255, 255))  # White text
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)
        
        # Calculate text position (centered)
        text_rect = painter.fontMetrics().boundingRect(text)
        text_x = center_x - text_rect.width() // 2
        text_y = center_y + text_rect.height() // 4
        
        painter.drawText(text_x, text_y, text)
        painter.end()
    
    def handle_detection_data(self, message):
        """Handle detection data messages"""
        try:
            data = json.loads(message)
            current_time = datetime.now()
            
            # Update temperature display and chart data
            if "tMin" in data:
                temp_min = float(data['tMin'])
                self.ui.label__MinTemp.setText(f"{temp_min:.1f}°C")
                self.chart_min_temp.add_data_point(current_time, temp_min)
            
            if "tMax" in data:
                temp_max = float(data['tMax'])
                self.ui.label_MaxTemp.setText(f"{temp_max:.1f}°C")
                self.chart_max_temp.add_data_point(current_time, temp_max)
            
            if "tCenter" in data:
                temp_center = float(data['tCenter'])
                self.ui.label_CenterTemp.setText(f"{temp_center:.1f}°C")
                self.chart_center_temp.add_data_point(current_time, temp_center)
            
            # Update fire detection status
            if "fireDetected" in data:
                new_fire_state = bool(data["fireDetected"])
                timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
                mode = self.ui.comboBox_model.currentText()
                self.db_manager.log_fire_event(timestamp, temp_min, temp_max, temp_center, new_fire_state, mode)
                self.load_fire_records()
                self.fire_detected = new_fire_state
                self.ui.widget_state.update()  # Trigger redraw
            
            self.append_received_message("Detection Data", "Temperature and fire detection data updated", "blue")
            
        except json.JSONDecodeError:
            self.append_received_message("Error", "Detection data message format error", "red")
        except Exception as e:
            self.append_received_message("Error", f"Error processing detection data: {str(e)}", "red")
    
    def eventFilter(self, obj, event):
        # Handle Ctrl+Enter to send message
        if obj == self.ui.textEdit_Send:
            if event.type() == event.Type.KeyPress:
                if event.key() == 16777220 and event.modifiers() == 67108864:  # Ctrl+Enter
                    self.send_message()
                    return True
        return super().eventFilter(obj, event)
    
    def toggle_connection(self):
        """Toggle MQTT connection status"""
        if not self.mqtt_client.is_connected:
            self.connect_to_mqtt()
        else:
            self.disconnect_from_mqtt()
    
    def connect_to_mqtt(self):
        """Connect to MQTT broker"""
        # Get connection parameters
        protocol = self.ui.comboBox_Protocol.currentText()
        address = self.ui.lineEdit_Address.text().strip()
        port = self.ui.lineEdit_2.text().strip()
        client_id = self.ui.lineEdit_6.text().strip()
        username = self.ui.lineEdit_UserName.text().strip()
        password = self.ui.lineEdit_5.text().strip()
        
        # Validate input
        if not address or not port:
            QMessageBox.warning(self, "Warning", "Please enter server address and port")
            return
        
        if not client_id:
            QMessageBox.warning(self, "Warning", "Please enter client ID")
            return
        
        try:
            port = int(port)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Port must be a number")
            return
        
        # Connect to MQTT broker
        self.mqtt_client.connect_to_broker(protocol, address, port, client_id, username, password)
    
    def disconnect_from_mqtt(self):
        """Disconnect from MQTT"""
        self.mqtt_client.disconnect_from_broker()
    
    def on_connection_status_changed(self, connected, message):
        if connected:
            self.ui.pushButton_Open.setText("Disconnect")
            self.append_received_message("System", message, "green")
            # 保存连接设置
            self.save_connection_settings()
            # 连接成功后自动订阅默认主题
            self.auto_subscribe_default_topics()
        else:
            self.ui.pushButton_Open.setText("Connect")
            self.append_received_message("System", message, "red")
    
    def add_subscription(self):
        topic = self.ui.lineEdit_Subscription.text().strip()
        if not topic:
            QMessageBox.warning(self, "Warning", "Please enter subscription topic")
            return
        
        if not self.mqtt_client.is_connected:
            QMessageBox.warning(self, "Warning", "Please connect to MQTT broker first")
            return
        
        # Check if already subscribed
        for i in range(self.subscription_model.rowCount()):
            if self.subscription_model.item(i).text() == topic:
                QMessageBox.information(self, "Info", "This topic is already subscribed")
                return
        
        # Subscribe to topic
        if self.mqtt_client.subscribe_topic(topic):
            # Add to subscription list
            item = QStandardItem(topic)
            self.subscription_model.appendRow(item)
            
            # Add to send topic dropdown
            topics = self.topic_model.stringList()
            if topic not in topics:
                topics.append(topic)
                self.topic_model.setStringList(topics)
            
            # Clear input box
            self.ui.lineEdit_Subscription.clear()
            
            self.append_received_message("System", f"Subscribed to topic: {topic}", "blue")
        else:
            QMessageBox.warning(self, "Warning", "Subscription failed, please check connection status")
    
    def send_message(self):
        topic = self.ui.comboBox_Subscription.currentText()
        message = self.ui.textEdit_Send.toPlainText().strip()
        
        if not topic:
            QMessageBox.warning(self, "Warning", "Please select a topic to send")
            return
        
        if not message:
            QMessageBox.warning(self, "Warning", "Please enter message to send")
            return
        
        if not self.mqtt_client.is_connected:
            QMessageBox.warning(self, "Warning", "Please connect to MQTT broker first")
            return
        
        # Send message
        if self.mqtt_client.publish_message(topic, message):
            self.append_received_message("Sent", f"Topic: {topic}\nContent: {message}", "purple")
            self.ui.textEdit_Send.clear()
        else:
            QMessageBox.warning(self, "Warning", "Send failed, please check connection status")
    
    def on_message_received(self, topic, message):
        if not message:
            return
        self.append_received_message("Received", f"Topic: {topic}\nContent: {message}", "black")
        
        # Handle configuration update messages
        if topic == "/ESP32/config_update":
            self.handle_config_update(message)
        # Handle detection data messages
        elif topic == "/ESP32/detection_data":
            self.handle_detection_data(message)
    
    def append_received_message(self, msg_type, content, color="black"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"<span style='color: {color};'>[{timestamp}] [{msg_type}] {content}</span><br>"
        
        # Check message buffer length limit (max 1024 messages)
        current_text = self.ui.textEdit_Received.toPlainText()
        lines = current_text.split('\n')
        
        # If exceeds 1024 messages, delete oldest messages
        if len(lines) >= 1024:
            # Keep the latest 1023 messages, leaving space for new message
            lines_to_keep = lines[-1023:]
            self.ui.textEdit_Received.clear()
            for line in lines_to_keep:
                if line.strip():  # Only add non-empty lines
                    self.ui.textEdit_Received.append(line)
        
        self.ui.textEdit_Received.append(formatted_message)
    
    def auto_subscribe_default_topics(self):
        """Auto subscribe to default topics"""
        if not self.mqtt_client.is_connected:
            return
            
        default_topics = ["/ESP32/detection_data", "/ESP32/config_update"]
        
        for topic in default_topics:
            # Check if already subscribed
            already_subscribed = False
            for i in range(self.subscription_model.rowCount()):
                if self.subscription_model.item(i).text() == topic:
                    already_subscribed = True
                    break
            
            if not already_subscribed:
                if self.mqtt_client.subscribe_topic(topic):
                    # Add to subscription list
                    item = QStandardItem(topic)
                    self.subscription_model.appendRow(item)
                    
                    # Add to send topic dropdown
                    topics = self.topic_model.stringList()
                    if topic not in topics:
                        topics.append(topic)
                        self.topic_model.setStringList(topics)
                    
                    self.append_received_message("System", f"Auto subscribed to topic: {topic}", "blue")
    
    def on_config_changed(self):
        """Send configuration when parameters change"""
        if not self.mqtt_client.is_connected:
            return
            
        config_data = {
            "measurement_mode": self.ui.comboBox_model.currentIndex() + 1,  # Send 1-4
            "threshold_1": self.ui.doubleSpinBox_1.value(),
            "threshold_2": self.ui.doubleSpinBox_2.value(),
            "threshold_3": self.ui.doubleSpinBox_3.value(),
            "threshold_4": self.ui.doubleSpinBox_4.value(),
            "threshold_5": self.ui.doubleSpinBox_5.value()
        }
        
        config_json = json.dumps(config_data)
        
        if self.mqtt_client.publish_message("/ESP32/config", config_json):
            self.append_received_message("Config Sent", f"Topic: /ESP32/config\nContent: {config_json}", "orange")
    
    def handle_config_update(self, message):
        """Handle device configuration update messages"""
        try:
            config_data = json.loads(message)
            
            # Update interface control values
            if "measurement_mode" in config_data:
                # Receive 1-4 values, convert to 0-3 index
                mode_index = int(config_data["measurement_mode"]) - 1
                if 0 <= mode_index <= 3:  # Ensure index is within valid range
                    self.ui.comboBox_model.setCurrentIndex(mode_index)
            
            if "threshold_1" in config_data:
                self.ui.doubleSpinBox_1.setValue(float(config_data["threshold_1"]))
            
            if "threshold_2" in config_data:
                self.ui.doubleSpinBox_2.setValue(float(config_data["threshold_2"]))
            
            if "threshold_3" in config_data:
                self.ui.doubleSpinBox_3.setValue(float(config_data["threshold_3"]))
            
            if "threshold_4" in config_data:
                self.ui.doubleSpinBox_4.setValue(float(config_data["threshold_4"]))
            
            if "threshold_5" in config_data:
                self.ui.doubleSpinBox_5.setValue(float(config_data["threshold_5"]))
            
            self.append_received_message("Config Update", "Device configuration synced to interface", "green")
            
        except json.JSONDecodeError:
            self.append_received_message("Error", "Configuration update message format error", "red")
        except Exception as e:
            self.append_received_message("Error", f"Error processing configuration update: {str(e)}", "red")
    
    def closeEvent(self, event):
        # Disconnect MQTT connection when closing
        if self.mqtt_client.is_connected:
            self.mqtt_client.disconnect_from_broker()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon("ui/Logo.png"))
    
    window = MQTTDemo()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
