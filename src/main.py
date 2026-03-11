import os, yaml, time, datetime
from steam_web_api import Steam

ncache = {} #Define cache as a global variable

def wsafetext(text: str) -> str:
    """
    Remove the characters that Windows does not allow.

    input: original text, output: changed text
    """
    for i in range(len(illegal)):
        text = text.replace(illegal[i], "")

    return text

def wreptext(text: str) -> str:
    """
    Replaces the character(space) into specific character.

    input: original text, output: changed text
    """
    for i in range(len(space)):
        text = text.replace(space, space_alt)

    return text

def get_name(gameid: int) -> str:
    """
    Returns the game title in Steam. Uses the dictionary to cache.

    input: gameid, output: game title
    """
    if ncache.get(gameid) != None:
        game_name = ncache.get(gameid)
    else:
        appdata = steam.apps.get_app_details(gameid)
        game_name = wsafetext(appdata.get(gameid).get("data").get("name"))
        game_name = wreptext(game_name)
        ncache.update({gameid: game_name})

    return game_name

def id2code(filename: str) -> str:
    """
    Returns the changed filename.

    input: filename, output: (changed)filename
    """
    text = filename.split('_')
    id = get_name(text[0])
    result = id + "_" + text[1] + "_" + text[2]

    return result

def rename_files(path: str) -> None:
    """
    Change the file name and measures the time taken.
    
    input: file path, output: None
    """
    start_time = int(time.time())
    count = 0

    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        if filename.split("_")[0].isdigit():
            newname = id2code(filename)
            os.rename(filepath, os.path.join(path, id2code(filename)))

            count += 1
            print(f"{count}) {filename} -> {newname}")

    if count == 0:
        print("No files changed.")
        return

    time_spent = int(time.time()) - start_time
    formated_time = str(datetime.timedelta(seconds = time_spent))
    print(f"{count} file names changed! Time Spent: {formated_time}")

# Main
if __name__ == "__main__":
    with open("config.yml", "r") as file:
        config_var = yaml.safe_load(file)

    yml_api_key = config_var["steam_api_key"]
    yml_path = config_var["path"]
    illegal = config_var["remove_char"]
    space = config_var["replace_space"]
    space_alt = config_var["replace_value"]

    API_KEY = os.environ.get(str(yml_api_key))
    PATH = str(yml_path)
    steam = Steam(API_KEY)

    rename_files(PATH)
