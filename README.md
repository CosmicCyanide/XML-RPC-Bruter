API Security Analyzer

API Security Analyzer is an advanced XML-RPC login brute-force tool designed for penetration testers and red teamers. It uses proxy rotation and asynchronous requests to perform login attempts on XML-RPC interfaces, allowing for stealthy brute-forcing. It supports different proxy types and automatic retries with flexible configurations.
Features

    Asynchronous Login Attempts: Quickly brute-force API endpoints using asynchronous HTTP requests.
    Proxy Support: Supports rotating HTTP, HTTPS, SOCKS4, and SOCKS5 proxies during login attempts.
    Configurable Usernames and Passwords: Load lists of usernames and passwords from files.
    Automatic Scheme Detection: Automatically detects and adds the appropriate scheme (http://, socks5://) to proxies if missing.
    Logging: Detailed logging of attempts, including successes and errors.
    Progress Tracking: Real-time progress tracking using the tqdm progress bar.
    Flexible Configuration: Configure delays, proxy usage, stop on success, and more via JSON configuration files.
    Multithreading Support: Runs multiple attempts concurrently for better efficiency.

Installation
Requirements

Ensure you have Python 3.8 or later installed. The following packages are required:

    aiohttp: For asynchronous HTTP requests.
    aiohttp_socks: To enable support for SOCKS proxies.
    tqdm: For progress tracking.
    xmlrpc.client: To communicate with XML-RPC APIs.

To install the required packages, run:

pip install aiohttp aiohttp_socks tqdm

Clone the Repository

Clone the repository to your local machine:

git clone https://github.com/your-username/api-security-analyzer.git
cd api-security-analyzer

Proxy List Format

Create a proxy list file with the following format:

plaintext

104.248.59.38:80
37.120.133.137:3128
193.34.95.110:8080
106.45.221.168:3256

The script will automatically add http:// if no scheme is provided.
Usage
1. Configuration File

You need to create a JSON configuration file to specify the options for the tool. Here is an example config.json file:

{
    "url": "http://example.com/xmlrpc.php",
    "username_file": "usernames.txt",
    "password_file": "passwords.txt",
    "proxy_file": "proxies.txt",
    "log_file": "brute_force.log",
    "log_level": "INFO",
    "delay": 0.5,
    "stop_on_success": true,
    "username_mode": "constant",
    "constant_username": "admin"
}

    url: The target XML-RPC API endpoint.
    username_file: Path to the file containing a list of usernames (optional if constant_username is set).
    password_file: Path to the file containing a list of passwords.
    proxy_file: Path to the file containing proxies.
    log_file: Path to the log file for storing results and errors.
    log_level: Logging level (e.g., INFO, DEBUG).
    delay: Time to wait between attempts (in seconds).
    stop_on_success: Stop brute-force once a successful login is found (true or false).
    username_mode: Set to constant to use a single username, or file to load usernames from the username_file.
    constant_username: If username_mode is constant, specify the constant username here.

2. Usernames and Passwords File

You also need to create files containing usernames and passwords. Here’s an example for usernames:

usernames.txt

admin
user
test

passwords.txt

123456
password
iloveyou
qwerty

3. Running the Script

Run the tool by specifying the configuration file:

python xmlrpc_bruteforce.py config.json

4. Output

    The script will output login attempts and results to the console and log file.
    It will also track progress using tqdm, so you can monitor the brute-force process in real-time.
    Successful logins will be highlighted in green, and errors will be displayed in red.

Example Output

yaml

2024-09-20 12:45:22,230 - INFO - Loaded configuration from config.json.
2024-09-20 12:45:22,250 - INFO - Loaded proxies from proxies.txt.
Brute-Force Progress:  25%|██████████████████▍                      |  2500/10000 [00:30<02:00,  20attempt/s]
Success: admin:password through http://104.248.59.38:80

License

This project is licensed under the MIT License. See the LICENSE file for more information.
Customization Options

Feel free to tweak the tool as per your needs:

    Custom Headers: Add custom headers to bypass protections like rate-limiting or to disguise your requests.
    Rate Limiting: Use the delay setting to slow down brute-force attempts and avoid detection.
    Stop Conditions: Set stop_on_success to true to immediately halt when a successful login is found.

Happy testing! If you encounter any issues or want to contribute, feel free to create an issue or pull request on GitHub.
