import time
import pyfiglet
import os
import subprocess
from colorama import init, Fore
from tqdm import tqdm as pbar

init()

# Check if modules are already installed
try:
    import yt_dlp
    import colorama
    import tqdm
    import pyfiglet
except ImportError:
    # Installation of required modules and libraries
    subprocess.run('pip install yt-dlp', shell=True)
    subprocess.run('pip install colorama', shell=True)
    subprocess.run('pip install tqdm', shell=True)
    subprocess.run('pip install pyfiglet', shell=True)

# Check if aria2c is installed
try:
    subprocess.run('aria2c -v', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    aria2c_installed = True
except FileNotFoundError:
    aria2c_installed = False

    # Install aria2c based on the operating system
    if os.name == "posix":
        subprocess.run('sudo apt-get install aria2', shell=True)
    elif os.name == "nt":
        subprocess.run('pkg install aria2', shell=True)
    else:
        print(f"\n{Fore.RED}❌ Unsupported operating system.{Fore.RESET}")
        exit()
    
    print(f"\n{Fore.CYAN}✅ aria2c installed successfully.{Fore.RESET}")

def download_media(name, title, download_format='mp4'):
    if download_format not in ['mp4', 'mp3']:
        raise ValueError(f"\n{Fore.RED}❌ Invalid download format. Please choose 'mp4' or 'mp3'.{Fore.RESET}")
    
    system = os.name

    if system == "nt":
        output_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'PyMedia')
    elif system == "posix":
        output_folder = '/sdcard/PyMedia'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
    else:
        print(f"\n{Fore.RED}❌ Unsupported operating system.{Fore.RESET}")
        return
    
    search_query = f'ytsearch:{name} {title}'

    command = f'yt-dlp -x --audio-format mp3 --extract-audio ' if download_format == 'mp3' else 'yt-dlp '
    command += f'--output "{output_folder}/{title}.%(ext)s" --external-downloader aria2c --merge-output-format mp4 "{search_query}"'

    subprocess.run(command, shell=True)

def get_user_choice():
    clear_screen()
    
    def print_small_text(text):
        small_font = pyfiglet.Figlet(font='small')
        ascii_art = small_font.renderText(text)
        lines = ascii_art.split('\n')
        
        max_length = max(len(line) for line in lines)
        padding = (os.get_terminal_size().columns - max_length) // 2
        
        for line in lines:
            print(' ' * padding + line)

    text = "PyMedia"
    print_small_text(text)

    print("\n 🙋‍♂️ Welcome 🙋‍♀️")
    print(f"\n{Fore.CYAN} 1. Download Audio\n 2. Download Video\n 3. Quit{Fore.RESET}")
    return input("\n ➡️ Enter your choice 👇: ")

def clear_screen():
    subprocess.run('clear' if 'posix' in os.name else 'cls', shell=True)

def download_another():
    print(f"\n\n📌 {Fore.CYAN} DO YOU HAVE ANOTHER AUDIO OR VIDEO TO DOWNLOAD?")
    print(f"✅ 1. YES\n❌ 2. NO{Fore.RESET}")
    return input("\n🎯 Enter your choice: ")

while True:
    option = get_user_choice()

    if option == '1':
        name = input("\n👨‍🎤 Enter the artist name: ")
        title = input("\n🎧 Enter the title of the song: ")
        print(f"\n{Fore.GREEN}📥 Downloading audio...{Fore.RESET}")
        download_media(name, title, 'mp3')
        print(f"\n{Fore.GREEN}✅ Download complete!{Fore.RESET}")
        output_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'PyMedia') if os.name == "nt" else "/sdcard/PyMedia"
        print(f"\n💾 Media downloaded and saved on the Desktop as 'PyMedia'." if os.name == "nt" else "\n💾 Saved In The Location: /sdcard/PyMedia")
    elif option == '2':
        video_name = input("\n🎥 Enter the video name or title: ")
        print(f"\n{Fore.GREEN}📥 Downloading video...{Fore.RESET}")
        download_media(video_name, video_name, 'mp4')
        print(f"\n{Fore.GREEN}✅ Download complete!{Fore.RESET}")
        output_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'PyMedia') if os.name == "nt" else "/sdcard/PyMedia"
        print(f"\n💾 Media downloaded and saved on the Desktop as 'PyMedia'." if os.name == "nt" else "\n💾 Saved In The Location: /sdcard/PyMedia")
    elif option == '3':
        print(f"\n{Fore.YELLOW}⌛ Please wait...\n{Fore.RESET}")
        for _ in pbar(range(30), desc=" Exiting the program", bar_format="{l_bar}{bar}"):
            time.sleep(0.1)
        print(f"\n{Fore.YELLOW}✅ Program Exited\n{Fore.RESET}")
        break
    else:
        print(f"\n{Fore.RED}❌ Invalid option. Please choose '1', '2', or '3'.{Fore.RESET}")

    another_option = download_another()

    if another_option == '1':
        clear_screen()
    elif another_option == '2':
        print(f"\n{Fore.YELLOW}⌛ Please wait...\n{Fore.RESET}")
        for _ in pbar(range(30), desc=" Exiting the program", bar_format="{l_bar}{bar}"):
            time.sleep(0.1)
        print(f"\n{Fore.YELLOW}✅ Program Exited\n{Fore.RESET}")
        break
    else:
        print(f"\n{Fore.RED}❌ Invalid option. Please choose '1' or '2'.{Fore.RESET}")
