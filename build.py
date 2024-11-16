import os, sys
import shutil
import subprocess

msbuildPath = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\MSBuild\\Current\\Bin\\MSBuild.exe"
vcvars32Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars32.bat"
vcvars64Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars64.bat"


vcltlFile = "https://github.com/Chuyu-Team/VC-LTL5/releases/download/v5.0.9/VC-LTL-5.0.9-Binary.7z"
vcltlFileName = "VC-LTL-5.0.9-Binary.7z"
onnxruntimeFile = "https://github.com/RapidAI/OnnxruntimeBuilder/releases/download/1.14.1/onnxruntime-1.14.1-vs2019-static-mt.7z"
onnxruntimeFileName = "onnxruntime-1.14.1-vs2019-static-mt.7z"
opencvFile = "https://github.com/RapidAI/OpenCVBuilder/releases/download/4.7.0/opencv-4.7.0-windows-vs2019-mt.7z"
opencvFileName = "opencv-4.7.0-windows-vs2019-mt.7z"

mecabUrl = "https://github.com/HIllya51/mecab.git"
localeRemulatorUrl = "https://github.com/HIllya51/Locale_Remulator.git"
magpieUrl = "https://github.com/HIllya51/Magpie_CLI.git"
lunaOCRUrl = "https://github.com/HIllya51/LunaOCR.git"

zstdgit = "https://github.com/facebook/zstd.git"

rootDir = os.path.dirname(__file__)


def installVCLTL():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"curl -LO {vcltlFile}")
    subprocess.run(f"7z x {vcltlFileName} -oVC-LTL5")
    os.chdir("VC-LTL5")
    subprocess.run("cmd /c Install.cmd")


def buildMecabxp():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {mecabUrl}")
    os.chdir("mecab\\mecab\\src")
 
    with open("do.bat", "w") as ff:
         ff.write(
                rf"""
cmake -G "Visual Studio 16 2019" -A Win32 -T v141_xp -B ./build/
cmake --build ./build --config Release -j 14
"""
            ) 
    os.system(f"cmd /c do.bat")
    os.makedirs(f"{rootDir}/ALL/DLL32", exist_ok=True)
    shutil.move("build/Release/libmecab.dll", f"{rootDir}/ALL/DLL32")


def buildMecab():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {mecabUrl}")
    os.chdir("mecab\\mecab")

    os.makedirs(f"{rootDir}/ALL/DLL32", exist_ok=True)
    os.makedirs(f"{rootDir}/ALL/DLL64", exist_ok=True)
    subprocess.run(f'cmd /c "{vcvars32Path}" & call make.bat')
    shutil.move("src/libmecab.dll", f"{rootDir}/ALL/DLL32")

    subprocess.run(f'cmd /c "{vcvars64Path}" & call makeclean.bat & call make.bat')
    shutil.move("src/libmecab.dll", f"{rootDir}/ALL/DLL64")


def buildMagpie():
    os.chdir(rootDir + "\\temp")
    subprocess.run(f"git clone {magpieUrl}")
    os.chdir("Magpie_CLI")
    subprocess.run(f"git checkout origin/cli")
    subprocess.run(
        f'"{msbuildPath}" -restore -p:RestorePackagesConfig=true;Configuration=Release;Platform=x64;OutDir={os.getcwd()}\\publish\\x64\\ -t:Magpie_Core;Effects Magpie.sln'
    )
    os.makedirs(f"{rootDir}/ALL/Magpie", exist_ok=True)
    shutil.move("publish/x64/Magpie.Core.exe", f"{rootDir}/ALL/Magpie")
    shutil.move("publish/x64/effects", f"{rootDir}/ALL/Magpie")


if __name__ == "__main__":
    os.chdir(rootDir)

    os.makedirs("temp", exist_ok=True)
    installVCLTL()
    if sys.argv[1] == "mecab":

        buildMecab()
    elif sys.argv[1] == "mecab_xp":

        buildMecabxp()
    elif sys.argv[1] == "magpie":
        buildMagpie()
    os.chdir(rootDir)
    os.system(
        rf'"C:\Program Files\7-Zip\7z.exe" a -m0=LZMA -mx9 .\\{sys.argv[1]}.zip .\\ALL'
    )
