import base64
import random
from pathlib import Path

txt_data = "The_warden_only_speaks_Java."
encoded_data = base64.b64encode(txt_data.encode()).decode()  # the encoding is just for fun

folder_path = Path.home() / "Documents" / "KronoCTF"
folder_path.mkdir(parents=True, exist_ok=True)

random_number_list = list(range(1, 11001))
random.shuffle(random_number_list)

for number in random_number_list:
    try:
        content = txt_data if number == 10935 else encoded_data
        with open(folder_path / f"Krono{number}.txt", "x") as file:
            file.write(content)
    except FileExistsError:
        print("That file already exists")


