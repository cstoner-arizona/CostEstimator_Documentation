# Getting Started

It is recommended for development work to compile the Cura source code and work directly within Cura. This will allow most LSPs to capture Cura's API and the source code can be used as a direct reference to Cura's API.

(getting-started-cura-source)=
## Cura Source Installation

The source code for Cura needs to be downloaded and compiled for your system. The instructions to do so can be found on [Cura's Running from Source Docs](https://github.com/Ultimaker/Cura/wiki/Running-Cura-from-Source). 

I started by using VSCode which would require me to launch cura from terminal. But **now I did the few commands to get PyCharm working instead because it allows you to press the "Run" button and it launches Cura, its so much faster.**  You can find out how [here](https://github.com/Ultimaker/Cura/wiki/Getting-Started#developing-cura)

While it may be highly recommended you read through the entire GitHub Wiki as it can highlight some troubleshooting issues when attempting to install from source or install for your specific IDE, that takes to long, and I wouldnt do it personally. Here are my notes for installing on mac below to save you some time.
### My instal experience with Mac
Notes:
- Make sure you get cura 5.10 (not 5.10.0)
- I found when you clone cura it will create a directory inside the current directory. So I created my own "Cura-Root" in my Research folder, then went in there to clone it. It then created a "Cura" source code folder
- In Step 4. in the wiki I don't remember every running those commands in the 'Note on the execution virtual enviorment'
- After doing Step 3. on the wiki `conan install` you should be able to just do the steps below. And from now on, you should only have to do the steps below
1. `source build/generators/conanrun.sh`
2. `source cura_run_venv/bin/activate` 
3. `conda deactivate` (NOT REQUIRED ACTUALLY)
4. `python cura_app.py`




---

(getting-started-cura-standard)=
## Cura Standard Installation
