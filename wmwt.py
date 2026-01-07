import os
import platform
from colorama import init, Fore, Style
import psutil
import subprocess
import distro

init(autoreset=True)

user = os.environ.get("USER")
home = os.environ.get("HOME")
term = os.environ.get("TERM")
shell = os.environ.get("SHELL")
termprog = os.environ.get("TERM_PROGRAM")
os = platform.system()
kernver = platform.release()
cpu = platform.processor()
cpu_percent = psutil.cpu_percent(interval=0.5)

def bytes_to_gb(b):
    return b / (1024 ** 3)

mem = psutil.virtual_memory()

if os == "Darwin":
	type = "mac"
	macver = platform.mac_ver()[0]
	# i wish there was an easier way to pull off this bullshit.
	macOSversions = {
		"10.0": "Mac OS X Cheetah",
		"10.1": "Mac OS X Puma",
		"10.2": "Mac OS X Jaguar",
		"10.3": "Mac OS X Panther",
		"10.4": "Mac OS X Tiger",
	 	"10.5": "Mac OS X Leopard",
		"10.6": "Mac OS X Snow Leopard",
		"10.7": "Mac OS X Lion",
		"10.8": "OS X Mountain Lion",
		"10.9": "OS X Mavericks",
		"10.10": "OS X Yosemite",
		"10.11": "OS X El Capitan",
		"10.12": "macOS Sierra",
		"10.13": "macOS High Sierra",
		"10.14": "macOS Mojave",
		"10.15": "macOS Catalina",
		"11": "macOS Big Sur",
		"12": "macOS Monterey",
		"13": "macOS Ventura",
		"14": "macOS Sonoma",
		"15": "macOS Sequoia",
		"26": "macOS Tahoe"
	}
	parts = macver.split(".")
	lookup_key = parts[0] if parts[0] != "10" else f"{parts[0]}.{parts[1]}"
	os = macOSversions.get(lookup_key, "Unknown Mac system")
	cpu = subprocess.check_output(
		["sysctl", "-n", "machdep.cpu.brand_string"],
		text=True
	).strip()

if os == "Linux":
    type = "linux"
    os = distro.name()
    cpu = "Unknown CPU"
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    cpu = line.split(":", 1)[1].strip()
                    break
    except FileNotFoundError:
        pass

# handle shell
if shell in ("/bin/bash", "/usr/bin/bash"):
	shell = "Bash"
elif shell in ("/bin/zsh", "/usr/bin/zsh"):
	shell = "ZSh"
elif shell in ("/bin/sh", "/usr/bin/sh"):
	shell = "Bourne Shell"
elif shell in ("/bin/fish", "/usr/bin/fish", "/usr/local/bin/fish"):
	shell = "FiSH"

# handle term wowowow
if term == "xterm-kitty":
	term = "Kitty Terminal"
elif term == "xterm-ghostty":
	term = "Ghostty Terminal"
elif term == "xterm-256color":
	term = "XTerm 256 Color"
elif term == "xterm":
	term = "XTerm"
elif term == None:
	print("ERROR: Could not determine term!")
	term = "Undetermined"

# handle macOS terminal fuckery
if termprog == None:
	termprog = "no"
elif termprog == "Apple_Terminal":
	term = "macOS Terminal"

print()

if type == "mac":
	print("Hello, " + Fore.BLUE + user + Style.RESET_ALL + "! " + "You live at " + Fore.BLUE + home + Style.RESET_ALL + " on this " + Fore.RED + os + " " + macver + Style.RESET_ALL + " system.")
	print("You are using the " + Fore.RED + "Darwin " + kernver + Style.RESET_ALL + " kernel.")
else:
	print("Hello, " + Fore.BLUE + user + Style.RESET_ALL + "! " + "You live at " + Fore.BLUE + home + Style.RESET_ALL + " on this " + Fore.RED + os + " " + kernver + Style.RESET_ALL + " system.")

print("Your shell is " + Fore.CYAN + shell + Style.RESET_ALL + ", and your terminal is " + Fore.CYAN + term + Style.RESET_ALL + ".")

# system ifnormatiun
print()

print(
	f"Your CPU is "
	f"{Fore.GREEN}{cpu}{Style.RESET_ALL}, and around "
	f"{Fore.GREEN}{cpu_percent}%{Style.RESET_ALL} of its power is currently in use."
)

# memememory
print(
	f"You are currently using "
	f"{Fore.GREEN}{bytes_to_gb(mem.used):.2f} GB{Style.RESET_ALL} "
	f"out of "
	f"{Fore.GREEN}{bytes_to_gb(mem.total):.2f} GB{Style.RESET_ALL} "
	f"of memory. ({Fore.GREEN}{mem.percent}%{Style.RESET_ALL})"
)

print()
