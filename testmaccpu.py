import subprocess

cpu = subprocess.check_output(
    ["sysctl", "-n", "machdep.cpu.brand_string"],
    text=True
).strip()

print(cpu)

