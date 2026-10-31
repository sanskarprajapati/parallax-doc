# Script and voice

## Length

About 2.3 words a second at a documentary pace before pauses. 60 s holds 125-140 words;
the D-Day script is 133 words and its take ran 72 s before fitting. `fit_voice.py`
refuses a tempo change outside 0.85-1.25: past that, cut words.

## Shape

The style suits an argument, not a list:

1. The accepted story in two or three lines, said respectfully.
2. The turn: "That's not in question. What is in question is..."
3. The reality, one claim per scene, each with a concrete anchor the camera can show (a
   place, a date, a document, a number).
4. A last line that reframes the first, held at least 2 s before the end.

## Writing for the voice and the screen

- Spell numbers the way they are read: "nineteen forty-four", "sixteen days".
- Each scene needs a word to land its typed line on. Write the emphasis lines into the
  script as the words the narrator says, then type them on that word.
- Fact-check every claim before showing the script. Prefer the softer true version
  ("most German soldiers killed died fighting the Soviet Union") to a sharper statistic
  you cannot source.

## Voice

Any single take of the whole script works. Options:

- ElevenLabs (Eleven v3): a mature documentary narrator, stability about 0.5, speed 1.0.
  An audio tag like `[serious]` at the start sets the read. It costs credits: confirm
  first.
- Free and local: `npx hyperframes tts script.txt -v bm_george -o take.wav` (Kokoro;
  British male). Flatter, but fine for drafts.
- The person's own recording.

One voice for the whole film. If you are rebuilding a reference whose narrator you can't
use, re-voice the whole film rather than switching voices partway.

Then: `fit_voice.py <dir> take.mp3 60` writes `assets/vo/vo.m4a` (exact length) and
`assets/vo/words.json`. Every scene's text start comes from words.json.
