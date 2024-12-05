import os, sys
import shutil
import subprocess

vcvars32Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars32.bat"
vcvars64Path = "C:\\Program Files\\Microsoft Visual Studio\\2022\\Enterprise\\VC\\Auxiliary\\Build\\vcvars64.bat"


vcltlFile = "https://github.com/Chuyu-Team/VC-LTL5/releases/download/v5.0.9/VC-LTL-5.0.9-Binary.7z"
vcltlFileName = "VC-LTL-5.0.9-Binary.7z"

mecabUrl = "https://github.com/HIllya51/mecab.git"

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

if __name__ == "__main__":
    os.chdir(rootDir)

    os.makedirs("temp", exist_ok=True)
    installVCLTL()
    if sys.argv[1] == "mecab":

        buildMecab()
    elif sys.argv[1] == "mecab_xp":

        buildMecabxp()
    os.chdir(rootDir)
    os.system(
        rf'"C:\Program Files\7-Zip\7z.exe" a -m0=LZMA -mx9 .\\{sys.argv[1]}.zip .\\ALL'
    )
