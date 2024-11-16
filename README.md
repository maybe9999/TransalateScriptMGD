<h1> Translator MGD</h1>

<h2> Description </h2>
Translate the dialogues stored in Json. The script excludes and does not modify any other data stored in the .json other than dialogs(Not 100% tested).


<h2> Usage notes:</h2>

1) Install:
"""
pip install googletrans==4.0.0rc1
"""
2) Windows: Open CMD and run "chcp 65001" in the console.

3) Run "getSpecialWord.py". This will generate a txt file needed for text filtering.

4) Start the translation by running "Translate.py". (It will only translate x-Events for now, the translation library may generate errors).

5) Check if everything was translated correctly by running "isTranslated.py".


<h2> Solutions to problem with googletrans:</h2>
When translating, an error is sometimes generated due to the googletrans library.

Error: 'NoneType' object is not iterable

Solutions: 
- https://github.com/ssut/py-googletrans/issues/260#issuecomment-751521801   (This works for me so far)

```
Replace this line 222 of googletrans/client.py with this

try:
    translated_parts = list(map(lambda part: TranslatedPart(part[0], part[1] if len(part) >= 2 else []), parsed[1][0][0][5]))
except TypeError: # because of the gender-specific translate results
    translated_parts = [ TranslatedPart(parsed[1][0][1][0], [parsed[1][0][0][0], parsed[1][0][1][0]]) ]
```

Related:
- https://github.com/ssut/py-googletrans/issues/278
- https://github.com/hhhwwwuuu/BackTranslation/issues/1




<h2> Negative points: </h2>

- It takes approximately 8-12 hours to translate all of X Events. (Needs optimization)</br>

- There are certain dialogues that due to errors in the code or translation errors, not everything is translated and remains as it was originally.</br>

<h2> Solutions</h2>

- Instead of translating dialogue by dialogue, you can translate groups of dialogues (It would greatly optimize the time required), I will implement it later. </br>

- A script to analyze dialogs that remain the same between the translated file and the original. if a == b: print("Translation error"), Those specific parts would be translated.</br>



Any suggestion, collaboration or constructive comment is welcome. If you see any flaws or where there is point for improvement, please comment...

