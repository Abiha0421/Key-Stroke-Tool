

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


; --- Output EXE name ---
OutputBaseFilename=KeyStrokeTool_Installer

[Files]

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
