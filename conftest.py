# Example of how those lines should sit in your actual function
from appium.options.android import UiAutomator2Options

options = UiAutomator2Options()
options.app_package = "com.andersenlab.easyfin"
options.app_activity = "com.andersenlab.easyfin.presentation.activity.MainActivity"
options.app = "C:/Users/n.krotsik/Desktop/EasyFin-Android/easy-fin-android/app/build/outputs/apk/debug/app-debug.apk"