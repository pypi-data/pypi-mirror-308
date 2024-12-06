"""
This package holds some functions to run on Windows to interact with the registry.
"""

__all__ = ["install_baguette_file_format", "remove_baguette_file_format"]




def install_baguette_file_format():
    """
    This function enables the BAGUETTE (.bag) file format for the current user.
    """
    import winreg
    from pathlib import Path
    from sys import executable
    from baguette.setup.preferences import preferences_dir, global_preferences_dir
    print("Opening main key")
    classes_root_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes")
    winreg.SetValue(classes_root_key, "Baguette.File", winreg.REG_SZ, "Baguette File")
    print("Creating ProgID key")
    ProgId = winreg.CreateKey(classes_root_key, "Baguette.File")
    winreg.SetValue(ProgId, "FriendlyTypeName", winreg.REG_SZ, "Baguette File")
    winreg.SetValue(ProgId, "InfoTip", winreg.REG_SZ, "Contains all the information about the execution report of a program, all well-organized.")
    winreg.SetValue(ProgId, "DefaultIcon", winreg.REG_SZ, f"{global_preferences_dir / "baguette.ico"}") 
    print("Creating Shell/Interact/Command key")
    ShellCommand = winreg.CreateKey(ProgId, r"shell\Interact")
    winreg.SetValue(ShellCommand, "command", winreg.REG_SZ, f'''"{executable}" -m baguette.open "%1" "%*"''')
    print("Creating Shell/Visualize/Command key")
    ShellCommand = winreg.CreateKey(ProgId, r"shell\Visualize")
    winreg.SetValue(ShellCommand, "command", winreg.REG_SZ, f'''"{Path(executable).with_name("pythonw.exe")}" -m baguette.open "%1" gephi''')
    print("Creating Shell/Bake/Command key")
    ShellCommand = winreg.CreateKey(ProgId, r"shell\Bake")
    winreg.SetValue(ShellCommand, "command", winreg.REG_SZ, f'''"{Path(executable).with_name("python.exe")}" -m baguette.open "%1" bake''')
    print("Creating Shell/Toast/Command key")
    ShellCommand = winreg.CreateKey(ProgId, r"shell\Toast")
    winreg.SetValue(ShellCommand, "command", winreg.REG_SZ, f'''"{Path(executable).with_name("python.exe")}" -m baguette.open "%1" toast''')
    print("Setting default action")
    winreg.SetValue(ProgId, "shell", winreg.REG_SZ, f'''Interact''')
    print("Creating Extention key")
    winreg.SetValue(classes_root_key, ".bag", winreg.REG_SZ, "Baguette.File")
    ShellCommand.Close()
    ProgId.Close()
    classes_root_key.Close()





def remove_baguette_file_format():
    """
    This function enables the BAGUETTE (.bag) file format for the current user.
    """
    import winreg
    classes_root_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Classes")
    winreg.DeleteKey(classes_root_key, "Baguette.File")
    winreg.DeleteKey(classes_root_key, ".bag")