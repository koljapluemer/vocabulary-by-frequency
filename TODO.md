- autofill skeleton notes after editing
    - auto-alias target and native
    - add missing sibling/parent stuff
- what to do with overlaps, such as "I create 'buy' as a sibling of 'spend' and later its in the frequency list but with as 'buying' or some shit"
    - maybe after all ad in all the words, but only make some todos
    - or just deal with rectifying it, it's all language work after all...
- check if drawing is eventually bothering to get extracted
    - same with pronunciation apparently...
- build a kind of intepreter for these search-and-replaces from templates (like $FILE) — they're entirely predictable (at least so far, wait for shit like "lets have 3 wrong images")
- find a way to balance exercise types: some stuff (imagine per-letter cloze) can delete thousands of exercises everytime, drawing based is much rarer... (especially when drawings aren't detected lol)


- add more types by writing functions akin to `def generate_exercises_sentence_prompt_double(vocabs):` and then adding them like `exercises.update(generate_native_to_target(vocabs))`


- clean up all the print bs