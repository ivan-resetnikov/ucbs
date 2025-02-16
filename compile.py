# Closed-source Code License (CSCL)
# 
# Copyright (C) Ivan Reshetnikov - All Rights Reserved.
# 
# UNAUTHORIZED COPYING OF THIS SOFTWARE OR ITS SOURCE CODE, VIA ANY MEDIUM IS STRICTLY PROHIBITED.
# THE CONTENTS INSIDE THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL.
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# Written by Ivan Reshetnikov legal@ivan-reshetnikov.dev, February 2025.

import os
import subprocess
import glob
import time

from ansi import *

SOURCE_DIR = "./src"
BUILD_DIR = "./build/obj"
EXECUTABLE_PATH = "./build/bin/main.exe"
CLANG_PATH_PATH = "CLANG_PATH"
INCLUDE_DIR: str = "./include"
LIB_DIR: str = "./lib"
LINK_TARGETS: list[str] = ["glfw3dll"]
SHADER_DIR: str = "./src/shaders"

# Ensure dir tree
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(EXECUTABLE_PATH), exist_ok=True)

# Scan source & objects
source_files = glob.glob(os.path.join(SOURCE_DIR, "*.cpp")) + glob.glob(os.path.join(SOURCE_DIR, "*.c"))
object_files = [os.path.join(BUILD_DIR, os.path.splitext(os.path.basename(f))[0] + ".o") for f in source_files]

def needs_rebuild(src: str, obj: str) -> bool:
    return not os.path.exists(obj) or os.path.getmtime(src) > os.path.getmtime(obj)

# Shaders
shader_db: str = ""

shader_db += "// Auto generated file, changes will be overriden\n"
shader_db += "\n"
shader_db += "#pragma once\n"
shader_db += "\n"
shader_db += "namespace v13 {\n"
shader_db += "\tnamespace shader_db {\n"

for file_name in os.listdir(SHADER_DIR):
    # Optimize
    file_path: str = os.path.join(SHADER_DIR, file_name)

    file_content: str = ""
    with open(file_path, "r") as f:
        file_content = f.read()
    
    # Dump
    lines: list[str] = file_content.split("\n")
    
    shader_db += f"\t\tconst char* {file_name.replace(".", "_").upper()} = \n"
    for i, line in enumerate(lines):
        shader_db += f"\t\t\t\"{line}{ "\\0" if i == len(lines)-1 else "\\n" }\"\n"
    shader_db += "\t\t;\n\n"

shader_db += "\t} // namespace shader_db \n"
shader_db += "} // namespace v13\n"

with open("./src/shader_db.h", "w") as f:
    f.write(shader_db)

# Compile objects if needed
for source_path, object_path in zip(source_files, object_files):
    pair_need_rebuild: bool = needs_rebuild(source_path, object_path)

    object_dir: str = os.path.dirname(object_path)
    object_name: str = os.path.basename(object_path)

    if pair_need_rebuild:
        print(f"* {FG_WHITE_FAINT}{object_dir}/{RESET}{object_name} - {FG_YELLOW}out of date{RESET}, rebuilding")
        
        try:
            command_vector: list[str] = [CLANG_PATH, f"-I\"{INCLUDE_DIR}\"", "-c", source_path, "-o", object_path]
            command: str = " ".join(command_vector).replace("\\", "/")
            print(f"{FG_WHITE_FAINT}\t{command}{RESET}")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print(f"  {FG_RED}Compilation failed{RESET}")
    else:
        print(f"* {FG_WHITE_FAINT}{object_dir}/{RESET}{object_name} - {FG_GREEN}up to date{RESET}, skipping")

# Link EXECUTABLE_PATH if needed
EXECUTABLE_PATH_dir: str = os.path.dirname(EXECUTABLE_PATH)
EXECUTABLE_PATH_name: str = os.path.splitext(os.path.basename(EXECUTABLE_PATH))[0]
EXECUTABLE_PATH_extension: str = os.path.splitext(os.path.basename(EXECUTABLE_PATH))[1]

EXECUTABLE_PATH_exists: bool = os.path.exists(EXECUTABLE_PATH)
any_new_objects: bool = any(needs_rebuild(obj, EXECUTABLE_PATH) for obj in object_files)

if not EXECUTABLE_PATH_exists or any_new_objects:
    print(f"* {FG_WHITE_FAINT}{EXECUTABLE_PATH_dir}/{RESET}{EXECUTABLE_PATH_name}{FG_BLUE}{EXECUTABLE_PATH_extension}{RESET} - {FG_YELLOW}out of date{RESET}, linking")

    try:
        command_vector: list[str] = [CLANG_PATH, f"-I\"{INCLUDE_DIR}\"", f"-L\"{LIB_DIR}\"", "-fuse-ld=lld"] + object_files + ["-o", EXECUTABLE_PATH] + [f"-l{l}" for l in LINK_TARGETS]
        command: str = " ".join(command_vector).replace("\\", "/")
        print(f"{FG_WHITE_FAINT}\t{command}{RESET}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"  {FG_RED}Linking failed{RESET}")
else:
    print(f"* {FG_WHITE_FAINT}{EXECUTABLE_PATH_dir}/{RESET}{EXECUTABLE_PATH_name}{FG_BLUE}{EXECUTABLE_PATH_extension}{RESET} - {FG_GREEN}up to date{RESET}, skipping")

print(f"* Build complete")


