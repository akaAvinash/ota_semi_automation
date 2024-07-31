class WiFiConstants:
    # SSID = "Guest"
    # PASSWORD = "BrokenWires@@2019"
    
    SSID = "ACT103699381413"
    PASSWORD = "23081207"

class RegistrationConstants:
    USERNAME = "acs-qa+test2@amazon.com"
    PASSWORD = "Test1234"

class WiFiCommands:
    SCAN = "adb shell ace mw wifi scan"
    GET_SCAN_RESULTS = "adb shell ace mw wifi get_scan_results"
    ADD_NETWORK = "adb shell ace mw wifi add_network ssid={ssid} psk={password}"
    GET_CONFIG = "adb shell ace mw wifi get_config"
    CONNECT_WIFI = "adb shell ace mw wifi connect {ssid}"
    SAVE_CONFIG = "adb shell ace mw wifi save_config"
    VALIDATE = "adb shell ace mw wifi get_net_state"

class RegistrationCommands:
    REGISTER_DEVICE = "adb shell ace mw map -u {username} -p {password}"
    VALIDATE_REGISTRATION = "adb shell ace mw map -y"

class SystemCommands:
    SHOW_OS_RELEASE = "adb shell vdcm get com.amazon.devconf/system/device-info/software-version"
    ENABLE_ALEXA = "adb shell vdcm set com.amazon.devconf/system/oobe/oobe-complete 'true'"
    ADB_DEVICES = "adb devices"
    FLASH = "python3 flashimage.py"
    DEVICE_NAME = "adb shell ace hal device_info cli -l -n"
    DEBUG_FOLDER = "adb push debug/ /etc/pkgmgrd/certs/debug/"
    SERVICE_CONFIG = "adb push service-configuration.conf /etc/pkgmgrd/"

class DeviceCommands:
    FLAG_440 = "adb shell idme dev_flags 0x440"
    FLAG_0 = "adb shell idme dev_flags 0"
    REBOOT = "adb shell reboot"
    FLAG_CHECK = "adb shell idme print | grep flags"
    BOOT_CONTROL = "adb shell boot_control_utility"
    SCREENSHOT_COMMAND = 'adb shell screenshooter -r /tmp/filename.png'
    PULL_SCREENSHOT = 'adb pull'

class AppCommands:
    PUSH_COMMAND = "adb push {local_path} {device_path}"
    INSTALL_COMMAND = "adb shell vpm install {device_path}"
    LIST_APPS_COMMAND = "adb shell vpm list apps"
    LAUNCH_COMMAND_PATTERN = "adb shell vlcm launch-app orpheus://com.amazon.systemtest.{app_name}.main"

class OOBECommands:
    USER_SETUP_COMPLETE = "adb shell ace hal kvs cli -s -k user_setup_complete -v 1"
    DCS_CONFIG = "adb shell vdcm set com.amazon.devconf/system/oobe/oobe-complete 'true'"
    HOME_SCREEN = "adb shell vpm set default com.amazon.category.launcher com.amazon.homelauncher.main"

class OTACommands:
    FORCE_SYNC_OTA = "adb shell ace mw ota forceSync"
    FORCE_UPDATE_OTA = "adb shell ace mw ota forceUpdate"
    START_OTA = "adb shell ace mw ota start"
    SHOW_OTA_STATUS = "adb shell ace mw ota show_status"
    OTA_LOG_COMMAND = "adb shell journalctl -f | grep ace_otad"
    
class Profiles:
    TV = "callie"
    MULTIMODAL = ("hypnos","galileo","baklava")