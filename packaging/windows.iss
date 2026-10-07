#define AppName "Meridian Clock"
#define AppVersion "0.2.0"
[Setup]
AppId={{48283815-F885-421C-B4B4-1391C3E9085D}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=Hachimi Moonlight
DefaultDirName={localappdata}\Programs\MeridianClock
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
OutputDir=..\dist\installer
OutputBaseFilename=MeridianClock-Setup-{#AppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
LicenseFile=..\LICENSE
UninstallDisplayIcon={app}\MeridianClock.exe
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked
[Files]
Source: "..\dist\MeridianClock\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\MeridianClock.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\MeridianClock.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\MeridianClock.exe"; Description: "Launch Meridian Clock"; Flags: nowait postinstall skipifsilent
