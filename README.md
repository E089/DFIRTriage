# DFIRTriage: Digital Forensics and Incident Response Triage Collector

A lightweight, powerful Python tool for collecting volatile and non-volatile forensic artifacts from a live Linux host. This tool is designed to be run quickly during an incident response, where it gathers essential data and packages it into a single, secure `.tar.gz` archive for offline analysis.

This project was built as a hands-on, portfolio-driven learning exercise.

## 🚀 Core Features

* **Fast & Focused:** Collects over 10 critical artifacts in seconds.
* **Configurable:** The `artifact_list.json` file makes it easy to add or remove collection commands.
* **Secure & Portable:** Packages all collected data into a single, timestamped `.tar.gz` archive and cleans up the raw files.
* **Robust:** Includes error handling for each command and a 30-second timeout to prevent hangs.

## 🛠️ How to Use

**Note:** This tool must be run with `sudo` (root) privileges to access protected system files and logs.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/E089/DFIRTriage.git](https://github.com/E089/DFIRTriage.git)
    cd DFIRTriage
    ```

2.  **Run the Collector:**
    The tool uses only standard Python libraries, so no installation is needed.
    ```bash
    sudo python3 -m dfirtriage.collector
    ```

3.  **Find Your Data:**
    The tool will create a `triage_output/` directory and place your final archive inside it.
    * **Example Output:** `triage_output/erica-Aspire-A514-55_20251107_110100.tar.gz`

## 📦 Artifacts Collected

This tool currently collects the following data:

* **`running_processes`**: Full list of all running processes (`ps auxwww`).
* **`active_network_connections`**: All active TCP/UDP connections and listening ports (`ss -tulpn`).
* **`open_files`**: A list of all files held open by processes (`lsof`).
* **`logged_in_users`**: Who is currently logged into the system (`w`).
* **`bash_history`**: Command history for all users, including `root`.
* **`authentication_logs`**: Login attempts, failures, and `sudo` usage (`/var/log/auth.log` & `/var/log/secure`).
* **`system_logs`**: General system activity logs (`/var/log/syslog`).
* **`cron_jobs`**: All scheduled tasks for all users and the system.
* **`system_configuration`**: Current kernel parameters (`sysctl -a`).
* **`temp_directories`**: File listings for common malware staging areas (`/tmp` & `/var/tmp`).

## 📝 Future Plans

* [ ] Add a `requirements.txt` file for future library management.
* [ ] Add support for Windows hosts.
* [ ] Implement remote collection capabilities.