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

import sys

import configparser
import importlib

import os
import subprocess
import glob
import time

from ansi import *
from log import *



class Extension:
    def __init__(self):
        self.config: configparser.ConfigParser = None
        self.inject_stages: list[str] = ""
        self.module = None


def main() -> None:
    # Ensure config
    config_path: str = sys.argv[-1]

    if len(config_path) == 1:
        log_error("Provided no config path argument")
        return

    if not os.path.exists(config_path):
        log_error("Provided config path does not exist")
        return
    
    if not config_path.endswith(".cfg"):
        log_error("Provided config path is not a config file (must end with .cfg)")
        return
    
    # Load config
    config = configparser.ConfigParser()
    config.read(config_path)

    CLANG_PATH = config["ucbs"]["clang_path"]

    SOURCE_DIR: str = config["ucbs"]["source_dir"]
    INTERMIDIATES_DIR: str = config["ucbs"]["intermidiates_dir"]
    EXECUTABLE_PATH = config["ucbs"]["executable_path"]

    INCLUDE_DIR: str = config["ucbs"]["include_dir"]
    LIB_DIR: str = config["ucbs"]["lib_dir"]

    EXTRA_LINK_TARGETS: list[str] = config["ucbs"]["extra_link_targets"].replace(" ", "").split(",")

    # Load extensions
    EXTENSIONS: list[str] = config["ucbs"]["extensions"].replace(" ", "").split(",")

    loaded_extensions: list[Extension] = []
    for extension_name in EXTENSIONS:
        extension: Extension = Extension()

        extension.config = configparser.ConfigParser()
        extension.config.read(f"./extensions/{extension_name}/extension.cfg")

        extension.inject_stages = extension.config["extension"]["inject_stages"]

        extension.module = importlib.import_module(f"extensions.{extension_name}.extension")

        loaded_extensions.append(extension)
        
    # Ensure dir tree
    os.makedirs(INTERMIDIATES_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(EXECUTABLE_PATH), exist_ok=True)

    # Scan source & objects
    source_files = glob.glob(os.path.join(SOURCE_DIR, "*.cpp")) + glob.glob(os.path.join(SOURCE_DIR, "*.c"))
    object_files = [os.path.join(INTERMIDIATES_DIR, os.path.splitext(os.path.basename(f))[0] + ".o") for f in source_files]

    def needs_rebuild(src: str, obj: str) -> bool:
        return not os.path.exists(obj) or os.path.getmtime(src) > os.path.getmtime(obj)

    for extention in loaded_extensions:
        if "BEFORE_COMPILATION_OF_INTEMIDIATES" in extention.inject_stages:
            extention.module.run(extension.config)
    
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

    # Link executable if needed
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


if __name__ == "__main__":
    main()
