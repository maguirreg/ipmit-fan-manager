# Fan Manager

The **Fan Manager** is a Python script that helps manage the fan speed of a system based on CPU temperature. It provides a flexible way to control fan speeds according to temperature thresholds. The script uses IPMI (Intelligent Platform Management Interface) through the `ipmitool` command-line utility.

## Features

- Automatically adjusts fan speed based on CPU temperature.
- Supports manual control mode with customizable temperature thresholds.
- Logging of temperature and fan speed changes.

## Prerequisites

Before using this script, make sure you have the following prerequisites:

1. Python installed (Python 3 recommended).
2. `ipmitool` utility installed on your system.

## Install and Execution

1. Clone this repository to your local machine or download the script.

2. Ensure that `ipmitool` is installed on your system. You can check if it exists by running:

   ```bash
   ipmitool -V
   ```

   If it's not installed, you can usually install it using your system's package manager.

3. Run the script with the following command:

   ```bash
   python fan_manager.py
   ```

## Run as a Service

1. Clone this repository to your local machine using the same steps as described above.

2. Locate the `fan-manager.service` file in the repository directory.

3. Copy the `fan-manager.service` file to the `systemctl` service directory. You can typically find this directory at `/etc/systemd/system/`. Use the `sudo` command for copying to ensure proper permissions:

   ```bash
   sudo cp fan-manager.service /etc/systemd/system/
   ```

4. Copy the `fan-manager.py` file to a location like `/opt/fan-manager/fan-manager.py` and modify the path in the service file if needed. After copying the service file, execute the following command to reload the systemd daemon and recognize the new service:

    ```bash
    sudo systemctl daemon-reload
    ```

5. Now, you can start the `fan-manager` service using the following command:

    ```bash
    sudo systemctl start fan-manager.service
    ```

6. To enable the `fan-manager` service to start automatically at boot, use the following command:

    ```bash
    sudo systemctl enable fan-manager.service
    ```

7. You can check the status of the service to ensure it's running as expected:

    ```bash
    sudo systemctl status fan-manager.service
    ```

Now, the fan-manager script will run as a service, automatically adjusting fan speeds based on CPU temperature. You can manage the service using standard systemd commands, such as start, stop, restart, and enable.

Remember to customize the service configuration according to your setup if necessary.

## Usage

- The script will monitor CPU temperature and adjust fan speed accordingly.
- You can switch between manual and automatic fan control modes based on the temperature threshold.
- Log entries will be written to the specified log file.

## Custom Temperature Mapping

You can customize the temperature-speed mapping by editing the `tempMap` variable in the script. It maps CPU temperatures to fan speeds in hexadecimal format.

## Tested On

- DELL R720
- DELL R720XD
- DELL R730XD

## License

This script is provided under the [GNU General Public License](LICENSE).

## Author

- Original Idea and Implementation done by [lvlegab1te](https://github.com/lvlegab1te/Fan-Manager)
- Adapted and Documented by [maguirreg](https://github.com/maguirreg/ipmit-fan-manager)

## Acknowledgments

- [Intelligent Platform Management Interface (IPMI)](https://en.wikipedia.org/wiki/Intelligent_Platform_Management_Interface)

Feel free to modify and adapt this script according to your needs. If you encounter any issues or have suggestions for improvements, please open an issue in this repository.

Happy cooling!
