import os
import platformdirs
import pathlib
import configparser


class NDenoiser_Settings:

    defaultSettings = {"output_path": "", "model_path": ""}
    DataPath = None
    ConfigPath = None
    config : configparser.ConfigParser = None

    def _CreateStatic():
        NDenoiser_Settings.DataPath = platformdirs.user_data_path("Neuroimage Denoiser")
        NDenoiser_Settings.ConfigPath = os.path.join(NDenoiser_Settings.DataPath, 'neurtorch_config.ini')
        NDenoiser_Settings.config = configparser.ConfigParser()
        NDenoiser_Settings.ReadConfig()

    def ReadConfig():
        NDenoiser_Settings.config.read(NDenoiser_Settings.ConfigPath)
        if "SETTINGS" not in NDenoiser_Settings.config.sections():
            NDenoiser_Settings.config.add_section("SETTINGS")
        for k,v in NDenoiser_Settings.defaultSettings.items():
            if not NDenoiser_Settings.config.has_option("SETTINGS", k):
                NDenoiser_Settings.config.set("SETTINGS", k, v)

        if not os.path.exists(NDenoiser_Settings.ConfigPath):
            NDenoiser_Settings.SaveConfig()

    def GetSettings(key: str) -> str|None:
        if not NDenoiser_Settings.config.has_option("SETTINGS", key):
            return None
        return NDenoiser_Settings.config.get("SETTINGS", key)
    
    def SetSetting(key: str, value: str, save:bool=False):
        NDenoiser_Settings.config.set("SETTINGS", key, value)
        if save:
            NDenoiser_Settings.SaveConfig()

    def SaveConfig():
        pathlib.Path(os.path.dirname(NDenoiser_Settings.ConfigPath)).mkdir(parents=True, exist_ok=True)
        with open(NDenoiser_Settings.ConfigPath, 'w') as configfile:
            NDenoiser_Settings.config.write(configfile)


NDenoiser_Settings._CreateStatic()