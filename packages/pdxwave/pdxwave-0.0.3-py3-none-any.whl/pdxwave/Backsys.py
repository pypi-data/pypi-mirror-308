from SPNKit import *
import os
import time
import threading
import re
import requests


PORT = 8109
BYTES = 5242880


def get_ipv6_address():
    return requests.get("https://ifconfig.me").text


def create_file_directory():
    """Create the File directory if it does not exist."""
    if not os.path.exists("./File"):
        os.makedirs("./File")


def parse_pdxwave_file(text: str):
    """Parse the PDXWave file content."""
    text_splitted = text.split("\n")
    filename = text_splitted[0]
    parts = re.findall(
        r"Download: Part ([0-9]+) +([0-9a-f\:]+)", "\n".join(text_splitted[1:])
    )
    return filename, parts


def slice_bytes(data, n):
    """Slice data into chunks of size n."""
    return [data[i : i + n] for i in range(0, len(data), n)]


def handle_inbox():
    """Handle incoming requests and serve files."""
    sock = SPN_SOCK("::", PORT)
    sock.serving()

    while True:
        c_sock, addr = sock.accept()
        try:
            com = sock.receive_data(c_sock)
            if com[0] == "LOAD":
                filepath = os.path.normpath(com[1])
                if os.path.isfile(f"./File/{filepath}"):
                    with open(f"./File/{filepath}", "rb") as file:
                        data = SPN_DATA(file.read())
                        data.crypto()
                        sock.send_data(c_sock, data)
                else:
                    sock.send_data(c_sock, SPN_DATA(b"File not found"))
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            c_sock.close()


def fetch_data_from_outbox(addr, fname, partID):
    """Fetch data from the outbox given the address and part ID."""
    sock = SPN_SOCK(addr, PORT)
    sock.connect()
    sock.send_data(sock.sock, ["LOAD", f"{fname}.{partID}"])
    time.sleep(0.2)
    try:
        data = sock.receive_data(sock.sock)
        if data:
            data.crypto()
            return data.data
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None


def download_file(fname):
    """Download a file and merge its parts."""
    filename, id_and_address = parse_pdxwave_file(
        open(fname, "r", encoding="utf-8").read()
    )
    filename = os.path.basename(filename)

    downloaded = []

    print("DOWNLOAD")

    for partID, addr in id_and_address:
        data = fetch_data_from_outbox(addr, filename, partID)
        if data:
            path = f"./File/{filename}.{partID}"
            with open(path, "wb") as file:
                file.write(data)
            downloaded.append(path)
            print(f"    |__ {path}")
        else:
            print(f"    |__ [ Failed to download part {partID} from {addr} ]")

    with open(filename, "wb") as fp:
        print("\nMERGE")
        for downloaded_path in downloaded:
            print(f"    |__ {downloaded_path}")
            with open(downloaded_path, "rb") as file:
                fp.write(file.read())


def upload_file(fname: str):
    """Upload a file and create a .pdxwave"""

    addr = get_ipv6_address()

    splitted_file = slice_bytes(open(fname, "rb").read(), BYTES)
    filename = os.path.basename(fname)

    lines = [filename]
    for idx, item in enumerate(splitted_file):
        path = f"./File/{filename}.{idx+1}"
        with open(path, "wb") as file:
            file.write(item)
        lines.append(f"Download: Part {idx+1}        {addr}")
        print(f"[ OK ]        {path}")

    with open(f"{filename}.pdxwave", "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


# Ensure the file directory exists
create_file_directory()

# Fetch the default server address
threading.Thread(target=handle_inbox, daemon=True).start()