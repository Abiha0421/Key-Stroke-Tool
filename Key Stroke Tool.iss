

; ================================
; Inno Setup Script for Key Stroke Tool
; Author: Abiha
; Version: 1.0
; ================================

[Setup]
AppName=Key Stroke Tool
AppVersion=1.0
AppPublisher=Abiha
AppPublisherURL=https://example.com
DefaultDirName={autopf}\Key Stroke Tool
DefaultGroupName=Key Stroke Tool
UninstallDisplayIcon={app}\Key Stroke Tool.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
DisableWelcomePage=no
LicenseFile=C:\Users\BT\Desktop\Keystroke Tool\license.txt
InfoBeforeFile=C:\Users\BT\Desktop\Keystroke Tool\README.md

; --- Output EXE name ---
OutputBaseFilename=KeyStrokeTool_Installer

[Files]
; --- Main Executable ---
Source: "C:\Users\BT\Desktop\Keystroke Tool\dist\Key Stroke Tool.exe"; DestDir: "{app}"; Flags: ignoreversion

; --- Documentation ---
Source: "C:\Users\BT\Desktop\Keystroke Tool\READMe.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\BT\Desktop\Keystroke Tool\license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu Shortcut
Name: "{group}\Key Stroke Tool"; Filename: "{app}\Key Stroke Tool.exe"

; Desktop Shortcut (user can choose)
Name: "{commondesktop}\Key Stroke Tool"; Filename: "{app}\Key Stroke Tool.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
; Launch program after installation
Filename: "{app}\Key Stroke Tool.exe"; Description: "Launch Key Stroke Tool"; Flags: nowait postinstall skipifsilent
