import platform

def get_pc_model():
    system = platform.system()

    try:
        if system == "Windows":
            import subprocess
            result = subprocess.run(["wmic", "csproduct", "get", "name"], capture_output=True, text=True)
            return result.stdout.splitlines()[1].strip()
        elif system == "Linux":
            with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                return f.read().strip()
        elif system == "Darwin": # macos
            import subprocess
            result = subprocess.run(["sysctl", "-n", "hw.model"], capture_output=True, text=True)
            return result.stdout.strip()
    except Exception:
        return "CONTACT DEV WITH ERRCODE: pc_model_threw_exception_unsupported_platform"