import yaml
import os
import random

OBSIDIAN_LEARN_PATH = "/home/b/MEGA/Obsidian/Zettelkasten/FrequentWordsLearning/Data"
TEMPLATE = "assets/vocab_template.md"
NR_OF_SKELETON_FILES_DESIRED = 20
WORD_FILE = "assets/en_1000.txt"
USED_WORD_STORE = "data/used_words.txt"
from datetime import datetime

def main():
    # create learn path if not exists
    if not os.path.exists(OBSIDIAN_LEARN_PATH):
        os.makedirs(OBSIDIAN_LEARN_PATH)
    # same with used_word_store
    if not os.path.exists(USED_WORD_STORE):
        with open(USED_WORD_STORE, 'w') as file:
            file.write("")
    # if there are less than 20 files in the path who have the property "q-type: todo", fill up (as opposed to "q-type: todo-done")
    md_files_in_path = [f for f in os.listdir(OBSIDIAN_LEARN_PATH) if f.endswith('.md')]
    md_files_todo = [f for f in md_files_in_path if is_todo_file(f)]
    print("nr of todo files:", len(md_files_todo))

    fill_up_with_files(NR_OF_SKELETON_FILES_DESIRED-len(md_files_todo))


def is_todo_file(f):
    with open(os.path.join(OBSIDIAN_LEARN_PATH, f), 'r') as file:
        content = file.read()
        if "q-type: todo" in content:
            if not "q-type: todo-done" in content:
                return True
        return False

def fill_up_with_files(nr_files):
    for i in range(nr_files):
        word = get_random_word()
        print("word:", word)
        # make file based on word (filename = word), content-wise copy the template
        with open(TEMPLATE, 'r') as file:
            template = file.read()
        template = template.replace("$DATE", datetime.now().strftime("%d.%m.%Y"))
        template = template.replace("$WORD", word)
        # save
        with open(os.path.join(OBSIDIAN_LEARN_PATH, word + ".md"), 'w') as file:
            file.write(template)


def get_random_word():
    with open(WORD_FILE, 'r') as file:
        words = file.readlines()
    with open(USED_WORD_STORE, 'r') as file:
        used_words = file.readlines()
    used_words = [w.strip() for w in used_words]
    words = [w.strip() for w in words]
    for w in used_words:
        if w in words:
            words.remove(w)
    word = random.choice(words)
    with open(USED_WORD_STORE, 'a') as file:
        file.write(word + "\n")
    return word
        

if __name__ == "__main__":
    main()