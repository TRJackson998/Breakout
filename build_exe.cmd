@REM Use PyInstaller to build 
@REM `--noconfirm` Replace output directory without asking for confirmation
@REM `-F` Create a one-file bundled executable. (Does not rely on environment folder)
@REM `--name breakout` Name to assign to the bundled app
@REM `--specpath .\build` Folder to store the generated spec file
@REM `--noconsole` Windows and Mac OS X: do not provide a console window for standard i/o. On Mac OS this also triggers building a Mac OS .app bundle.
@REM `--distpath .` Where to put the bundled app
call poetry run pyinstaller .\breakout\__main__.py --noconfirm -F --name breakout --specpath .\build --noconsole --distpath . --add-data ".\..\breakout\textures\*:textures"
pause