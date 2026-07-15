; Inno Setup script for KronoCTF.
; Build the app first:  pyinstaller KronoCTF.spec   (produces ..\dist\KronoCTF\)
; Then compile this in the Inno Setup IDE (Build > Compile) or:  iscc installer\KronoCTF.iss
; Output:  installer\Output\KronoCTF-Setup.exe

[Setup]
AppName=KronoCTF
AppVersion=1.0
AppPublisher=KronoCTF
DefaultDirName={autopf}\KronoCTF
DefaultGroupName=KronoCTF
DisableProgramGroupPage=yes
; Per-user install: no admin prompt, installs under the user's profile.
PrivilegesRequired=lowest
OutputBaseFilename=KronoCTF-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
; Package the whole PyInstaller onedir output.
Source: "..\dist\KronoCTF\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\KronoCTF"; Filename: "{app}\KronoCTF.exe"
Name: "{group}\Uninstall KronoCTF"; Filename: "{uninstallexe}"
Name: "{userdesktop}\KronoCTF"; Filename: "{app}\KronoCTF.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\KronoCTF.exe"; Description: "Launch KronoCTF now"; Flags: nowait postinstall skipifsilent
