import os
import configparser

def run(config: configparser.ConfigParser) -> None:
    SHADER_DIR: str = config["ext_shader_packager"]["./src/shaders"]

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