import ctypes
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

APP_TITLE = "DESTINY OPTIMIZER"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


class DestinyOptimizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x620")
        self.minsize(820, 560)
        self.configure(bg="#101418")
        self.running = False

        self._build_ui()
        self.log("Ready. For best results, run this app as Administrator.")
        if not is_admin():
            self.log("WARNING: Not running as Administrator. Some actions may fail.")

    def _build_ui(self):
        header = tk.Frame(self, bg="#101418")
        header.pack(fill="x", padx=18, pady=(16, 8))

        title = tk.Label(
            header,
            text="DESTINY OPTIMIZER",
            font=("Segoe UI", 26, "bold"),
            fg="#00ff88",
            bg="#101418",
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            header,
            text="Ultimate Gaming Performance Tool",
            font=("Segoe UI", 11),
            fg="#b8c7d1",
            bg="#101418",
        )
        subtitle.pack(anchor="w")

        body = tk.Frame(self, bg="#101418")
        body.pack(fill="both", expand=True, padx=18, pady=10)

        buttons_frame = tk.Frame(body, bg="#101418")
        buttons_frame.pack(side="left", fill="y", padx=(0, 14))

        self.output = scrolledtext.ScrolledText(
            body,
            bg="#0b0f13",
            fg="#d9f7e8",
            insertbackground="#d9f7e8",
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
        )
        self.output.pack(side="right", fill="both", expand=True)

        actions = [
            ("Kill Gameloop Processes", self.kill_gameloop, "safe"),
            ("Remove Gameloop Completely", self.remove_gameloop, "danger"),
            ("Clean System (Safe)", self.clean_system, "safe"),
            ("Network Boost (Low Ping)", self.network_boost, "restart"),
            ("Fix Windows Errors", self.fix_windows, "restart"),
            ("MAX FPS Mode", self.max_fps, "restart"),
            ("RAM Optimization", self.ram_optimization, "safe"),
            ("Disable Heavy Services", self.disable_services, "danger"),
            ("PRO Gaming Boost", self.pro_gaming_boost, "restart"),
            ("FULL BOOST", self.full_boost, "danger"),
        ]

        for text, command, kind in actions:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                width=30,
                height=2,
                font=("Segoe UI", 10, "bold"),
                fg="white",
                bg=self._button_color(kind),
                activebackground="#00aa66",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
            )
            btn.pack(pady=5, fill="x")

        bottom = tk.Frame(self, bg="#101418")
        bottom.pack(fill="x", padx=18, pady=(0, 14))

        tk.Button(
            bottom,
            text="Restart as Administrator",
            command=self.restart_as_admin,
            font=("Segoe UI", 10, "bold"),
            bg="#2d89ef",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left")

        tk.Button(
            bottom,
            text="Clear Log",
            command=lambda: self.output.delete("1.0", tk.END),
            font=("Segoe UI", 10),
            bg="#2b3138",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="left", padx=8)

        tk.Button(
            bottom,
            text="Exit",
            command=self.destroy,
            font=("Segoe UI", 10),
            bg="#3b1f24",
            fg="white",
            relief="flat",
            padx=12,
            pady=8,
            cursor="hand2",
        ).pack(side="right")

    @staticmethod
    def _button_color(kind):
        return {
            "safe": "#145c3f",
            "restart": "#725800",
            "danger": "#8a2635",
        }.get(kind, "#145c3f")

    def log(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.update_idletasks()

    def confirm(self, title, msg):
        return messagebox.askyesno(title, msg, icon="warning")

    def restart_as_admin(self):
        if is_admin():
            messagebox.showinfo("Administrator", "The app is already running as Administrator.")
            return
        try:
            params = " ".join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            self.destroy()
        except Exception as exc:
            messagebox.showerror("Error", f"Could not restart as Administrator:\n{exc}")

    def run_commands(self, title, commands, needs_admin=True):
        if self.running:
            messagebox.showwarning("Busy", "Another action is already running.")
            return
        if needs_admin and not is_admin():
            if not self.confirm("Administrator Recommended", "This action may need Administrator permissions. Continue anyway?"):
                return

        self.running = True
        self.log("\n" + "=" * 70)
        self.log(f"Starting: {title}")
        self.log("=" * 70)

        def worker():
            for cmd in commands:
                self.log(f"> {cmd}")
                try:
                    p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
                    if p.stdout.strip():
                        self.log(p.stdout.strip())
                    if p.stderr.strip():
                        self.log("ERROR: " + p.stderr.strip())
                    self.log(f"Exit code: {p.returncode}")
                except Exception as exc:
                    self.log(f"FAILED: {exc}")
            self.log(f"Finished: {title}")
            self.log("Restart Windows if the action changed network, power, services, or registry settings.")
            self.running = False

        threading.Thread(target=worker, daemon=True).start()

    def kill_gameloop(self):
        commands = [
            "taskkill /f /im androidemulator.exe",
            "taskkill /f /im aow_exe.exe",
            "taskkill /f /im QMEmulatorService.exe",
            "taskkill /f /im adb.exe",
            "taskkill /f /im GameLoader.exe",
            "net stop aow_drv",
            "net stop QMEmulatorService",
        ]
        self.run_commands("Kill Gameloop Processes", commands)

    def remove_gameloop(self):
        if not self.confirm("Remove Gameloop", "This will delete Gameloop/Tencent folders and registry keys. Continue?"):
            return
        commands = [
            r'rd /s /q "C:\Program Files\txgameassistant"',
            r'rd /s /q "C:\ProgramData\Tencent"',
            r'rd /s /q "%USERPROFILE%\AppData\Local\Tencent"',
            r'rd /s /q "%USERPROFILE%\AppData\Roaming\Tencent"',
            r'reg delete "HKCU\Software\Tencent" /f',
            r'reg delete "HKLM\SOFTWARE\WOW6432Node\Tencent" /f',
        ]
        self.run_commands("Remove Gameloop Completely", commands)

    def clean_system(self):
        commands = [
            r'del /q /f /s "%TEMP%\*"',
            r'for /d %x in ("%TEMP%\*") do rd /s /q "%x"',
            r'del /q /f /s "C:\Windows\Temp\*"',
            r'for /d %x in ("C:\Windows\Temp\*") do rd /s /q "%x"',
            r'del /q /f /s "%LOCALAPPDATA%\NVIDIA\DXCache\*"',
            r'del /q /f /s "%LOCALAPPDATA%\NVIDIA\GLCache\*"',
        ]
        self.run_commands("Clean System", commands)

    def network_boost(self):
        commands = [
            "ipconfig /flushdns",
            "netsh winsock reset",
            "netsh int ip reset",
            "netsh interface tcp set global autotuninglevel=normal",
            "netsh interface tcp set global rss=enabled",
        ]
        self.run_commands("Network Boost", commands)

    def fix_windows(self):
        commands = [
            "sfc /scannow",
            "DISM /Online /Cleanup-Image /RestoreHealth",
        ]
        self.run_commands("Fix Windows Errors", commands)

    def max_fps(self):
        commands = [
            "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61",
            "powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61",
            r'reg add "HKCU\System\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 0 /f',
        ]
        self.run_commands("MAX FPS Mode", commands)

    def ram_optimization(self):
        commands = [r'del /q /f /s "%TEMP%\*"']
        self.run_commands("RAM Optimization", commands, needs_admin=False)

    def disable_services(self):
        if not self.confirm("Disable Services", "This disables SysMain, DiagTrack, and Windows Search. Continue?"):
            return
        commands = [
            "sc stop SysMain",
            "sc config SysMain start= disabled",
            "sc stop DiagTrack",
            "sc config DiagTrack start= disabled",
            "sc stop WSearch",
            "sc config WSearch start= disabled",
        ]
        self.run_commands("Disable Heavy Services", commands)

    def pro_gaming_boost(self):
        if not self.confirm("PRO Gaming Boost", "This changes DNS and network stack settings. Continue?"):
            return
        commands = [
            r'netsh interface ip set dns name="Wi-Fi" static 8.8.8.8',
            r'netsh interface ip add dns name="Wi-Fi" 8.8.4.4 index=2',
            r'netsh interface ip set dns name="Ethernet" static 8.8.8.8',
            r'netsh interface ip add dns name="Ethernet" 8.8.4.4 index=2',
            "ipconfig /flushdns",
            "netsh winsock reset",
            "netsh int ip reset",
            "netsh int tcp set heuristics disabled",
            "netsh int tcp set global rss=enabled",
            "netsh int tcp set global autotuninglevel=normal",
            r'reg add "HKCU\System\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
        ]
        self.run_commands("PRO Gaming Boost", commands)

    def full_boost(self):
        if not self.confirm("FULL BOOST", "This runs almost all actions including remove Gameloop and disable services. Continue?"):
            return
        commands = []
        commands += [
            "taskkill /f /im androidemulator.exe",
            "taskkill /f /im aow_exe.exe",
            "taskkill /f /im QMEmulatorService.exe",
            "taskkill /f /im adb.exe",
            "taskkill /f /im GameLoader.exe",
            "net stop aow_drv",
            "net stop QMEmulatorService",
        ]
        commands += [
            r'rd /s /q "C:\Program Files\txgameassistant"',
            r'rd /s /q "C:\ProgramData\Tencent"',
            r'rd /s /q "%USERPROFILE%\AppData\Local\Tencent"',
            r'rd /s /q "%USERPROFILE%\AppData\Roaming\Tencent"',
            r'reg delete "HKCU\Software\Tencent" /f',
            r'reg delete "HKLM\SOFTWARE\WOW6432Node\Tencent" /f',
        ]
        commands += [
            r'del /q /f /s "%TEMP%\*"',
            r'del /q /f /s "C:\Windows\Temp\*"',
            "ipconfig /flushdns",
            "netsh winsock reset",
            "netsh int ip reset",
            "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61",
            "powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61",
            r'reg add "HKCU\System\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f',
            r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f',
            "sc stop SysMain",
            "sc config SysMain start= disabled",
            "sc stop DiagTrack",
            "sc config DiagTrack start= disabled",
            "sc stop WSearch",
            "sc config WSearch start= disabled",
        ]
        self.run_commands("FULL BOOST", commands)


if __name__ == "__main__":
    app = DestinyOptimizerGUI()
    app.mainloop()
