#define MyAppName "Centro de Solicitudes"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "JETELL"
#define MyAppURL "https://github.com/gustavo21franco-cell/centro-de-solicitudes"
#define MyAppExeName "Centro de Solicitudes.exe"

[Setup]
AppId={{A7B8C9D0-E1F2-4A5B-8C6D-123456789ABC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

DefaultDirName={autopf}\JETELL\Centro de Solicitudes
DefaultGroupName=JETELL\Centro de Solicitudes

OutputDir=instalador
OutputBaseFilename=Centro de Solicitudes Setup v{#MyAppVersion}

SetupIconFile=iconos\logo_instalador.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoCopyright=Copyright © 2026 JETELL

DisableProgramGroupPage=yes

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]

; ============================================================
; PROGRAMA PRINCIPAL
; ============================================================

Source: "dist\Centro de Solicitudes.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion

; ============================================================
; DATOS GEOGRÁFICOS
; ============================================================

Source: "DATOS\geografia_ecuador.json"; \
    DestDir: "{app}\DATOS"; \
    Flags: ignoreversion

; ============================================================
; VERSIÓN LOCAL
; ============================================================

Source: "DATOS\version_local.json"; \
    DestDir: "{app}\DATOS"; \
    Flags: ignoreversion skipifsourcedoesntexist

[Icons]

Name: "{autodesktop}\Centro de Solicitudes"; \
    Filename: "{app}\{#MyAppExeName}"

Name: "{autoprograms}\JETELL\Centro de Solicitudes"; \
    Filename: "{app}\{#MyAppExeName}"

[Run]

Filename: "{app}\{#MyAppExeName}"; \
    Description: "Ejecutar Centro de Solicitudes"; \
    Flags: nowait postinstall skipifsilent