import yaml
import os
import random

OBSIDIAN_LEARN_PATH = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWords"

def main():
    # create learn path if not exists
    if not os.path.exists(OBSIDIAN_LEARN_PATH):
        os.makedirs(OBSIDIAN_LEARN_PATH)
    # if there are less than 20 files in the path who have the property "q-type: todo", fill up (as opposed to "q-type: todo-done")
    md_files_in_path = [f for f in os.listdir(OBSIDIAN_LEARN_PATH) if f.endswith('.md')]
    md_files_todo = [f for f in md_files_in_path if is_todo_file(f)]
    print("nr of todo files:", len(md_files_todo))


def is_todo_file(f):
    with open(os.path.join(OBSIDIAN_LEARN_PATH, f), 'r') as file:
        content = file.read()
        if "q-type: todo" in content:
            if not "q-type: todo-done" in content:
                return True
        return False


if __name__ == "__main__":
    main()