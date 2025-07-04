# Application Layer Software Deployment Guide

This application layer software is a desktop application developed based on Python and PyQt5, designed for real-time monitoring, data visualization, and historical record queries.

## Deployment Steps

1.  **Environment Preparation and Dependency Installation**

    First, please ensure that Python 3.x environment is installed on your computer. Then, you need to install the required dependency libraries for this application, mainly including `paho-mqtt`, `PyQt5`, and `pyqtgraph`. You can install these libraries through package management tools (such as pip).

2.  **UI File Conversion**

    The graphical user interface of this application is designed using Qt Designer, with source files in `.ui` format. Before running the main program, you need to convert this `.ui` file to Python code. This can be accomplished through the `pyuic5` tool, which will convert the `ui/Main.ui` file to `ui/Ui_Main.py`.

3.  **Run the Program**

    After completing the above preparations, you can directly run the `main.py` file to start the application.

## Function Verification

After the program starts, you can perform the following operations to verify its functionality:

*   **Connection Configuration**: In the "Connection/Debug" tab, enter your MQTT Broker's address, port, and client ID, then click the "Connect" button to establish a connection with the server.
*   **Data Display**: After successful connection, switch to the "Info/Control" tab, where you will see real-time updated temperature data (minimum, maximum, center temperature) and fire status indicator lights.
*   **Real-time Charts**: The charts at the bottom of this page will display temperature data change curves in real-time, helping you intuitively understand temperature trends.
*   **Historical Records**: In the "Record" tab, you can view detailed records of all historical fire events. These records support sorting by ID and can be exported as CSV files for further analysis.
*   **Message Debugging**: If debugging is needed, the "Connection/Debug" tab will display all received raw MQTT messages and allow you to manually publish messages to specified topics.

Through the above steps, you can successfully deploy and run this application layer software, achieving comprehensive monitoring and management of the fire alarm system.