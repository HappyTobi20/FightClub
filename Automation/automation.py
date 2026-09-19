import argparse
import os
import shutil
import subprocess
from enum import Enum


class Platform(Enum):
    X64 = "x64"
    WIN32 = "Win32"


class Configuration(Enum):
    Debug = "Debug"
    Release = "Release"


class Action(Enum):
    CLEAN = "clean"
    GENERATE = "generate"
    BUILD_DEBUG = "build_debug"
    BUILD_RELEASE = "build_release"
    CLANG_FORMAT = "clang_format"


##################### manual configuration ####################

class Config:
    BUILD_FOLDER = "build"
    CMAKE_GENERATOR = "Visual Studio 17 2022"
    PLATFORM = Platform.X64
    FRESH = True
    CLEAN = True
    VERBOSE = False
    SOURCE_DIR = "Source"

###############################################################


def remove_build_folder():
    if os.path.exists(Config.BUILD_FOLDER):
        shutil.rmtree(Config.BUILD_FOLDER)
        print(f"Removed {Config.BUILD_FOLDER} folder.")
    else:
        print(f"{Config.BUILD_FOLDER} folder does not exist.")


def get_generate_command(configuration: Configuration):
    flags = {
        "generator": f'-G "{Config.CMAKE_GENERATOR}"',
        "platform": f"-A {Config.PLATFORM.value}",
        "fresh": "--fresh" if Config.FRESH else "",
    }
    return f'cmake .. {flags["generator"]} {flags["platform"]} {flags["fresh"]} -DCMAKE_BUILD_TYPE={configuration.value}'


def get_build_command(configuration: Configuration):
    flags = {
        "clean_first": "--clean-first" if Config.CLEAN else "",
        "verbose": "--verbose" if Config.VERBOSE else "",
    }
    return f'cmake --build . {flags["clean_first"]} {flags["verbose"]} --config {configuration.value}'


def run_command(command):
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def generate_project_files(configuration: Configuration):
    if not os.path.exists(Config.BUILD_FOLDER):
        os.makedirs(Config.BUILD_FOLDER)
        print(f"Created {Config.BUILD_FOLDER} folder.")

    os.chdir(Config.BUILD_FOLDER)
    command = get_generate_command(configuration)
    print(f"Generating project files with command: {command}")

    ok = run_command(command)
    os.chdir("..")

    if ok:
        print(f"Project files generated successfully for {configuration.value}.")
    else:
        print(f"Failed to generate project files for {configuration.value}.")


def build_project(configuration: Configuration):
    if not os.path.exists(Config.BUILD_FOLDER):
        print(f"{Config.BUILD_FOLDER} folder does not exist. Please generate project files first.")
        return

    os.chdir(Config.BUILD_FOLDER)
    command = get_build_command(configuration)
    print(f"Building with command: {command}")

    ok = run_command(command)
    os.chdir("..")

    if ok:
        print(f"Project built successfully in {configuration.value} mode.")
    else:
        print(f"Failed to build project in {configuration.value} mode.")


def get_source_files(source_dir, extensions):
    source_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                source_files.append(os.path.join(root, file))
    return source_files


def run_clang_format(source_dir):
    extensions = ['.cpp', '.h', '.hpp']
    format_sources = get_source_files(source_dir, extensions)

    if not format_sources:
        print(f'No source files found in {source_dir}.')
        return

    command = ['clang-format', '-i'] + format_sources
    if run_command(command):
        print('Clang-format successfully applied.')
    else:
        print('Error running clang-format.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CMake Automation Script")
    parser.add_argument("action", type=Action, choices=list(Action), help="Action to perform")
    args = parser.parse_args()
    selected_action = args.action

    actions = {
        Action.CLEAN: remove_build_folder,
        Action.GENERATE: lambda: generate_project_files(Configuration.Debug),
        Action.BUILD_DEBUG: lambda: build_project(Configuration.Debug),
        Action.BUILD_RELEASE: lambda: build_project(Configuration.Release),
        Action.CLANG_FORMAT: lambda: run_clang_format(Config.SOURCE_DIR),
    }

    if selected_action in actions:
        actions[selected_action]()
    else:
        print(f"Action '{selected_action}' is not implemented.")