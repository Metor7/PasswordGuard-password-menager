import customtkinter
import os

import utils.UpdatesMenager as UpdatesMenager
from widgets.CTkLogsConsole import CTkConsole

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        os.system('cmd /c "cls"')

        self.title("PasswordGuard - password menager")
        self.geometry(f"{800}x{500}")
        self.resizable(False, False)
        self.iconbitmap(r"assets\images\icon.ico")

        self.console = CTkConsole(self)

        self.destination_folder = os.getcwd()
        #UpdatesMenager.update_app(download_repo_url='https://github.com/Metor7/Custom-Aslain-WoT-Modpack-update-server', destination_folder=self.destination_folder, installed_app_version_file='VERSION', server_version_path='https://raw.githubusercontent.com/Metor7/Custom-Aslain-WoT-Modpack-update-server/main/VERSION', console=self.console)
        UpdatesMenager._get_installed_version(installed_version_file='VERSION', console=self.console)
        UpdatesMenager._get_latest_version(version_file='')
if __name__ == "__main__":
    app = App()
    app.mainloop()
