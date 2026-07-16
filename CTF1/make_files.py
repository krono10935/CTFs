import base64
import random
from pathlib import Path

txt_data = "The_warden_only_speaks_Java."
encoded_data = base64.b64encode(txt_data.encode()).decode()  # the encoding is just for fun

FOLDER_PATH = Path.home() / "Documents" / "KronoCTF"

# The one file that holds the real plaintext password.
SPECIAL_NUMBER = 10935
GOAL_FILE = FOLDER_PATH / f"Krono{SPECIAL_NUMBER}.txt"


def is_generated():
    return GOAL_FILE.exists()


def generate():
    FOLDER_PATH.mkdir(parents=True, exist_ok=True)

    random_number_list = list(range(1, 11001))
    random.shuffle(random_number_list)

    for number in random_number_list:
        content = txt_data if number == SPECIAL_NUMBER else encoded_data
        try:
            with open(FOLDER_PATH / f"Krono{number}.txt", "x") as file:
                file.write(content)
        except FileExistsError:
            pass

    return FOLDER_PATH


def ensure_generated():
    """Generate the files only if they aren't already there."""
    if not is_generated():
        generate()
    return FOLDER_PATH


if __name__ == "__main__":
    generate()
