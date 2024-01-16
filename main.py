import json, os, sys, requests, json
from colorama import Fore

pkg_list_url = "https://easy.kotelek.dev/packages"
# pkg_list_url = "http://localhost/easy-pm-api/packages/"
easy_ver = "1.1"
easy_location = f"{os.getenv('SystemDrive')}\\Windows\\System32"

def download_package(pkg_url, pkg_name, pkg_install_script):
    print(f"{Fore.MAGENTA}› {Fore.RESET}Downloading...")
    response = requests.get(pkg_url)

    if response.status_code == 200:
        with open(f"{pkg_name}.exe", "wb") as file:
            file.write(response.content)
        print(f"{Fore.GREEN}✔ {Fore.RESET}Package has been successfully downloaded.")
        print(f"{Fore.MAGENTA}› {Fore.RESET}Installing...")
        try:
            os.system(pkg_install_script)
            print(f"{Fore.GREEN}✔ {Fore.RESET}Package has been successfully installed.\n")
        except:
            print(f"{Fore.RED}✘ {Fore.RESET}Failed to install the package.\n")
    else:
        print(f"{Fore.RED}✘ {Fore.RESET}Failed to download the package. Status code: {response.status_code}\n")
        
def upgrade_package(pkg_url, pkg_name, pkg_install_script):
    print(f"{Fore.MAGENTA}› {Fore.RESET}Downloading...")
    response = requests.get(pkg_url)

    if response.status_code == 200:
        with open(f"{pkg_name}.exe", "wb") as file:
            file.write(response.content)
        print(f"{Fore.GREEN}✔ {Fore.RESET}Package has been successfully downloaded.")
        print(f"{Fore.MAGENTA}› {Fore.RESET}Updating...")
        try:
            os.system(pkg_install_script)
            print(f"{Fore.GREEN}✔ {Fore.RESET}Package has been successfully updated.\n")
        except:
            print(f"{Fore.RED}✘ {Fore.RESET}Failed to update the package.\n")
    else:
        print(f"{Fore.RED}✘ {Fore.RESET}Failed to download the package. Status code: {response.status_code}\n")
        
def uninstall_package(pkg_uninstall_script):
    print(f"{Fore.MAGENTA}› {Fore.RESET}Uninstalling...")
    try:
        os.system(pkg_uninstall_script)
        print(f"{Fore.GREEN}✔ {Fore.RESET}Package has been successfully uninstalled.\n")
    except:
        print(f"{Fore.RED}✘ {Fore.RESET}Failed to uninstall the package.\n")

def install(pkg_name):
    try:
        response = requests.get(pkg_list_url)
        response.raise_for_status()
        pkg_list = response.json()

        if("error" in pkg_list):
            print(f"{Fore.RED}✘ {Fore.RESET}Package does not exist.\n")
        else:
            if pkg_name in pkg_list["packages"]:
                pkg = pkg_list["packages"][pkg_name]
                
                if "pkg_url" in pkg:
                    pkg_url = pkg["pkg_url"]
                    pkg_install_script = pkg["install_script"]
                    download_package(pkg_url, pkg_name, pkg_install_script)

                    # Update easy.config.json with the installed package information
                    with open(f"{easy_location}\\easy.config.json", "r") as file:
                        pkgs_file = json.load(file)

                    pkg_version = pkg.get("version", "unknown")
                    pkgs_file["packages"][pkg_name] = pkg_version

                    with open(f"{easy_location}\\easy.config.json", "w") as file:
                        json.dump(pkgs_file, file, indent=2)

                else:
                    print(f"{Fore.RED}✘ {Fore.RESET}Incorrect package data.\n")
            else:
                print(f"{Fore.RED}✘ {Fore.RESET}Package does not exist.\n")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error during HTTP request: {e}\n")
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error decoding JSON: {e}\n")
    except Exception as e:
        print(f"{Fore.RED}✘ {Fore.RESET}An error occurred: {e}\n")
        
def upgrade(pkg_name):
    try:
        response = requests.get(pkg_list_url)
        response.raise_for_status()
        pkg_list = response.json()

        if("error" in pkg_list):
            print(f"{Fore.RED}✘ {Fore.RESET}Package does not exist.\n")
        else:
            if pkg_name in pkg_list["packages"]:
                pkg = pkg_list["packages"][pkg_name]
                
                if "pkg_url" in pkg:
                    pkg_url = pkg["pkg_url"]
                    pkg_install_script = pkg["install_script"]
                    upgrade_package(pkg_url, pkg_name, pkg_install_script)
                else:
                    print(f"{Fore.RED}✘ {Fore.RESET}Incorrect package data.\n")
            else:
                print(f"{Fore.RED}✘ {Fore.RESET}Package does not exist.\n")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error during HTTP request: {e}\n")
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error decoding JSON: {e}\n")
    except Exception as e:
        print(f"{Fore.RED}✘ {Fore.RESET}An error occurred: {e}\n")
        
def uninstall(pkg_name):
    try:
        response = requests.get(pkg_list_url)
        response.raise_for_status()
        pkg_list = response.json()
        
        with open(f"{easy_location}\\easy.config.json", "r") as file:
            pkgs_file = json.load(file)
        
        if pkg_name in pkgs_file["packages"]:
            pkg = pkg_list["packages"][pkg_name]
            
            if "uninstall_script" in pkg:
                uninstall_package(pkg["uninstall_script"])
            else: 
                print(f"{Fore.RED}✘ {Fore.RESET}Incorrect package data.\n")
        else:
            print(f"{Fore.RED}✘ {Fore.RESET}Package is not installed.\n")
            
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error during HTTP request: {e}\n")
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error decoding JSON: {e}\n")
    except Exception as e:
        print(f"{Fore.RED}✘ {Fore.RESET}An error occurred: {e}\n")
    
def update_easy():
    try:
        response = requests.get(pkg_list_url)
        response.raise_for_status()
        pkg_list = response.json()

        pkg = pkg_list["packages"]["easy"]
            
        pkg_url = pkg["pkg_url"]
        pkg_install_script = pkg["install_script"]
        print(f"{Fore.MAGENTA}› {Fore.RESET}Downloading...")
        
        response = requests.get(pkg_url)

        if response.status_code == 200:
            with open(f"easy-update.exe", "wb") as file:
                file.write(response.content)
            print(f"{Fore.GREEN}✔ {Fore.MAGENTA}easy{Fore.RESET} package been successfully downloaded.")
            print(f"{Fore.MAGENTA}› {Fore.RESET}Updating...")
            try:
                os.system(pkg_install_script)
                print(f"{Fore.GREEN}✔ {Fore.MAGENTA}easy{Fore.RESET} has been successfully updated.\n")
            except:
                print(f"{Fore.RED}✘ {Fore.RESET}Failed to update easy.\n")
        else:
            print(f"{Fore.RED}✘ {Fore.RESET}Failed to download easy package. Status code: {response.status_code}\n")

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error during HTTP request: {e}\n")
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}✘ {Fore.RESET}Error decoding JSON: {e}\n")
    except Exception as e:
        print(f"{Fore.RED}✘ {Fore.RESET}An error occurred: {e}\n")
        
def get_easy_ver():
    return easy_ver

def check_updates():
    ujson = requests.get(pkg_list_url).json()
    if float(ujson["easy_version"]) > float(get_easy_ver()):
        return True, ujson["easy_version"]
    else: 
        return False, get_easy_ver()
        
def info():
    print(f"easy (r) Package Manager v{get_easy_ver()}\n")
    if check_updates()[0]:
        new_ver = check_updates()[1]
        print(f"{Fore.GREEN}ℹ️{Fore.RESET}Update Found!")
        print(f"{Fore.MAGENTA}v{get_easy_ver()} {Fore.RESET}-> {Fore.GREEN}{new_ver}")
        print(f"{Fore.RESET}update using: {Fore.MAGENTA}easy update{Fore.RESET}\n")
    print(f"usage: {Fore.MAGENTA}easy [<command>] [<options>]{Fore.RESET}")
    print(f"For command list: {Fore.MAGENTA}easy help{Fore.RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        info()
    else:
        command = sys.argv[1]
        if command == "update":
            print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
            update_easy()
        elif command == "info":
            info()
        elif command == "help":
            print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
            print(f"usage: {Fore.MAGENTA}easy [<command>] [<options>]{Fore.RESET}")
            print("\ncommand list:")
            commands = [
                {"name": "update", "description": "                  update easy"},
                {"name": "upgrade [<package>]", "description": "     update package"},
                {"name": "info", "description": "                    get information about easy"},
                {"name": "help", "description": "                    get commands list"},
                {"name": "version", "description": "                 get easy version"},
                {"name": "install [<package>]", "description": "     install package"},
                {"name": "uninstall [<package>]", "description": "   uninstall package"}
            ]
            for command in commands:
                print(f"{Fore.MAGENTA + command['name'] + Fore.RESET + command['description']}")
            print('')
        elif command in ["version", "ver", "v", "--version", "--ver", "--v"]:
            print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
            if check_updates()[0]:
                new_ver = check_updates()[1]
                print(f"{Fore.GREEN}ℹ️{Fore.RESET}Update Found!")
                print(f"{Fore.MAGENTA}v{get_easy_ver()} {Fore.RESET}-> {Fore.GREEN}{new_ver}")
                print(f"{Fore.RESET}update using: {Fore.MAGENTA}easy update{Fore.RESET}\n")
        elif command == "install":
            if(len(sys.argv) > 2):
                print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                package_name = sys.argv[2]
                install(package_name)
            else:
                print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                print(f"{Fore.RED}✘ {Fore.RESET}Provide a package name!")
        elif command == "upgrade":
            if(len(sys.argv) > 2):
                print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                package_name = sys.argv[2]
                upgrade(package_name)
            else:
                print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                print(f"{Fore.RED}✘ {Fore.RESET}Provide a package name!")
        elif command == "uninstall":
            if(len(sys.argv) > 2):
                if(sys.argv[2] == "easy"):
                    print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                    print(f"{Fore.GREEN}ℹ️{Fore.RESET}To uninstall {Fore.MAGENTA}easy{Fore.RESET} check out our repo:")
                    print("https://github.com/xKotelek/easy\n")
                else:
                    print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                    package_name = sys.argv[2]
                    uninstall(package_name)
            else:
                print(f"easy (r) Package Manager {Fore.MAGENTA}v{get_easy_ver()}{Fore.RESET}\n")
                print(f"{Fore.RED}✘ {Fore.RESET}Provide a package name!")
        else:
            info()