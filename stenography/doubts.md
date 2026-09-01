# doubts.md

## python_script.py

### 0. The UTF-8 decode error is about bytes, not about paths (python_script.py - Comment 0)

#### User's Discovery/Doubt:
> 0. For what I understand this script is run in the terminal and `json_path`
> is the argument that follows with the file name with the metadata. As I used
> ```bash
> python_script.py .\metadatos.json
> ```
>
> and they're both in the same folder this should work, but it tells me that
> "[+] Pista de acceso reconstruida: Error durante la reconstrucción: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"

#### Verdict:
Partly correct - the `sys.argv` reading is right, but the belief that a correctly resolved path implies a successful read is false; `encoding='utf-8'` is a second, independent assertion about the file's bytes, and this file's bytes are UTF-16LE.

#### Explanation:
Two hypotheses are folded into this note, and separating them is the whole lesson.

The first is that `sys.argv[1]` carries the filename and that same-folder placement makes the path resolve. That holds exactly as written, and it is why the error was misleading: the path *did* resolve. `open()` found the file, obtained a handle, and returned without complaint. A path problem would have raised `FileNotFoundError`.

The second, unstated, is that a successful open means a successful read. It does not. `open(path, 'r', encoding='utf-8')` does two separate things: it opens a byte stream, and it attaches a decoder that will be applied later. The decoder never inspects the file at open time. The `UnicodeDecodeError` is therefore raised lazily, on the first `read()` — which happens inside `json.load()`, not at the `open()` line. This is a general property of text-mode I/O in Python: the `encoding` argument is a claim you make about the file, and the file is under no obligation to honour it.

The real cause is visible in the raw bytes. The file begins `FF FE 7B 00 0D 00 0A 00`. `FF FE` is the UTF-16 little-endian Byte Order Mark (U+FEFF); after it, each ASCII character is stored as its byte followed by `00`. That trailing `00` padding is why the file looks spaced out when something displays it one byte at a time.

Byte `0xFF` is diagnostic. In UTF-8, lead bytes occupy `0x00`–`0x7F` and `0xC2`–`0xF4`, continuation bytes `0x80`–`0xBF`. Nothing above `0xF4` is legal anywhere in the scheme, so `0xFE` and `0xFF` can never appear in valid UTF-8 at all. Seeing `0xff at position 0` in a decode error is close to a signature for "this is UTF-16".

The relevant codec distinction, in documentation form: `encoding='utf-16'` reads the BOM, infers endianness from it, and consumes it; `encoding='utf-16-le'` assumes the endianness and does *not* consume the BOM, leaving a literal `﻿` as the first character. I confirmed both behaviours against your file. The parallel pair on the UTF-8 side is `utf-8` versus `utf-8-sig`, where `utf-8-sig` strips an `EF BB BF` BOM.

Most likely origin: Windows PowerShell 5.1's `>` redirection and `Out-File` default to UTF-16LE with BOM (the encoding it calls "Unicode"). So `ffprobe ... > metadatos.json` in `powershell.exe` produces exactly this file. PowerShell 7+ (`pwsh`) defaults to UTF-8 without BOM, and `cmd.exe`'s `>` passes bytes through untouched. I did not watch you generate the file, so treat the mechanism as certain and the specific shell as inference.

#### Related:
The `json` module documents that `json.loads` accepts `bytes` and auto-detects UTF-8/16/32 from the leading bytes, which is why JSON read in binary mode sidesteps this entire class of problem.

---

### 1. `.get()` retrieves a value; the second argument is a fallback (python_script.py - Comment 1)

#### User's Discovery/Doubt:
> 1. I have never seen the method `.get()`. For what I understand from
> this line of code below what is saying is that from the `data` variable
> (which are my metadata) I need to check the streams and retrieve the
> complete information of that specific attribute (that is why we use the
> `[]`).

#### Verdict:
Partly correct - the retrieval half holds, but the belief that `[]` means "the complete information" is false; it is the default value returned only when the key `"streams"` is absent.

#### Explanation:
`dict.get` is a dictionary method with the canonical signature:

```
dict.get(key, default=None)
```

It looks up `key`. If present, it returns the associated value. If absent, it returns `default` instead of raising. That is its entire behaviour, and it is the only difference from subscripting: `data["streams"]` raises `KeyError` on a missing key, `data.get("streams")` returns `None`, and `data.get("streams", [])` returns an empty list.

So in the loop header there are two independent things: `"streams"` names what you want, and `[]` names what you get if it is not there. The `[]` is never returned when the key exists — in your file it does exist, so the loop iterates over the real list of two stream objects and the `[]` is dead weight that never materialises.

Why an empty list specifically: the result is fed straight to a `for`. Iterating `[]` runs the body zero times and completes normally. Iterating `None` raises `TypeError: 'NoneType' object is not iterable`. The default is chosen to be a harmless value of the type the next operation expects.

One trap worth knowing now, because it is the most common `.get` surprise: if a key is present but its value is `None`, `.get` returns `None`, not your default. The default fires on *key absence*, never on value emptiness. I verified this: `{"a": None}.get("a", "FALLBACK")` returns `None`.

#### Related:
`dict.get` does not insert the default into the dictionary; `dict.setdefault(key, default)` is the method that does.

---

### 2. The `0` and the `{}` are both defaults, not indices or slices (python_script.py - Comment 2)

#### User's Discovery/Doubt:
> 2. What is interesting is that in these `.get()` methods I am using
> different syntax. In `idx` the zero makes me believe it is a specific row
> (just like in numpy) but `tags` makes me believe is the whole object
> which is being retrieved (what in numpy would be `[:,:]`).

#### Verdict:
Wrong - the belief that the second argument selects or slices something is false; both `0` and `{}` are default values in the identical grammatical position, differing only in the type the surrounding code needs when the key is missing.

#### Explanation:
There is no syntactic difference between the two calls. Both are `d.get(key, default)`. The apparent variety comes from the defaults having different types, not from the calls doing different things.

The numpy analogy is what to discard. In numpy, `a[0]` and `a[:, :]` are *subscript* expressions: the brackets are an indexing operator and what goes inside selects a region of an existing array. Here you are looking at *function arguments* inside parentheses. Nothing is being selected. Python never reinterprets a positional argument as an index; the second argument to `.get` is a value that gets handed back verbatim when the lookup misses.

The types are chosen by what happens downstream:

- `stream.get("index", 0)` — the result is used as a sort key that is compared with `<`. A missing index would need to still be a number for that comparison to work, so the fallback is a number.
- `stream.get("tags", {})` — the result immediately has `.get()` called on it again. An empty dict supports `.get` and yields the next fallback; `None` does not. Without the `{}`, a stream with no tags would produce `AttributeError: 'NoneType' object has no attribute 'get'`, which I confirmed. This chaining pattern is the usual reason you see `{}` as a `.get` default.

The rule that transfers: pick a default that is a valid, empty instance of the type the next operation expects.

#### Related:
The one place a mutable literal like `{}` or `[]` genuinely misbehaves is as a *function parameter default* in a `def` signature, where it is created once at definition time and shared across all calls; inside a `.get()` call it is rebuilt on every evaluation and is safe.

---

### 3. The default is not a type declaration and performs no coercion (python_script.py - Comment 3)

#### User's Discovery/Doubt:
> 3. Indeed it seems that it is a way to get json with a combination
> of key, value pairs... but then why do I need to specificy the value format?
> It seems odd for me, as it seems rendundant to have a file that stores specific
> values with semantic names that it is also asking you to remember the type in the
> value. What I imagine is that this is some type of coertion, so while the original
> object might be of one type I might ask for another when retrieving it.

#### Verdict:
Wrong - the belief that the second argument declares or coerces the value's type is false; it is a literal fallback object returned only on a missing key, and it has no effect whatsoever on a value that is present.

#### Explanation:
Nothing in `dict.get` inspects, converts, or validates types. The method is roughly: if the key hashes to an entry, return that entry's value unchanged; otherwise return the second argument unchanged. Two objects, one of which is returned. No conversion path exists between them.

The direct disproof, which I ran: `{"a": 5}.get("a", "")` returns the integer `5`, not the string `"5"`. If the second argument were a coercion request or a type annotation, that call would have to produce a string. It does not, because the present value is returned untouched and the `""` is simply never reached.

Your sense of redundancy is pointing at something real but mislocated. JSON does carry types — `"index": 0` is a JSON number and becomes a Python `int`; `"tags": {…}` is a JSON object and becomes a `dict`. Python's `json` module performs that mapping at parse time, inside `json.load`, before your code sees anything. By the time you call `.get`, every value already has a definite type and there is nothing left to declare. What you are choosing with the second argument is not the type of the data but the type of the *hole* left when the data is missing — and you choose it to match, so that code downstream cannot tell the difference and does not have to branch.

The searchable name for this pattern is a *sentinel* or *default value*, and the design goal is to avoid `if key in d:` checks scattered through the code. The coercion idea belongs to a different family of tools entirely: explicit constructors like `int(x)` and `str(x)`, or schema/validation libraries such as `pydantic`, where declaring a type genuinely does change what you get back.

---

### 4. Sorting by stream index is declaration order, not chronological order (python_script.py - Comment 5)

#### User's Discovery/Doubt:
> 5. How interesting, it seems that it is sorting based on the number of the `idx` so
> indeed it follows a chronological order (or so I expect).

#### Verdict:
Partly correct - the sort does order the pairs by `idx` ascending, but the belief that this is *chronological* order is false; an ffprobe stream index is the stream's position in the container's stream table, which encodes no time information at all.

#### Explanation:
Mechanically the line is `list.sort(key=…)`. The canonical form is:

```
list.sort(key=None, reverse=False)
```

`key` is a function called once per element; it receives the whole element and returns the value to compare. Since the elements are `(index, text)` tuples, `x[0]` selects the integer. The comparison then happens on those integers only — the strings are never compared. Order is ascending unless `reverse=True`. `sort()` mutates the list in place and returns `None`, which is the difference from `sorted()`, and it is a stable sort (Timsort), so pairs sharing an index keep the relative order in which they were appended.

The part to correct is the semantics of the number. In ffprobe output, `index` is the ordinal position of a stream in the container's stream table — stream 0 here is the audio track, stream 1 the video track. It reflects the order the muxer wrote the track headers, nothing more. Both of your streams start at timestamp `0.000000` and run for roughly the same eight seconds; they are simultaneous, not sequential. Sorting by index cannot recover a chronology because no chronology was ever encoded there.

For this exercise that distinction is worth holding lightly: if fragments of a message were placed one per stream, index order is the puzzle-setter's *convention* for reassembly, which is a reasonable thing to rely on. Just do not carry away the belief that index means time.

#### Related:
`json.load` preserves the order of a JSON array, and ffprobe emits streams already ordered by index, so this sort is a no-op on your data rather than a step that is doing work.

---

### 5. UTF-8 is an encoding of Unicode, not a version of it (python_script.py - Comment 7)

#### User's Discovery/Doubt:
> 7. `utf-8` seems to be the one most commonly used in northamerica,
> but what are other type formats?... actually I think that utf-8 is like
> the latest version of accepted characters, so the "u" might come from
> universal and it includes all the big languages of humanity (I don't think
> indigenous or historic characters are included though).

#### Verdict:
Partly correct - the coverage intuition holds, but three specifics are false: the "U" is Unicode, not universal; UTF-8 is not a "latest version" of anything; and Unicode does encode historic and indigenous scripts.

#### Explanation:
UTF stands for *Unicode Transformation Format*. UTF-8 was designed by Ken Thompson and Rob Pike in 1992 and its byte layout has not changed since; it does not gain a version each time Unicode does.

The distinction that dissolves most of the confusion is *character set* versus *encoding*. Unicode is the catalogue: it assigns a number, a code point, to each character, and that catalogue is what versions — currently well over 150,000 assigned characters across more than 160 scripts. UTF-8, UTF-16 and UTF-32 are three different schemes for turning those same code points into bytes. All three can represent the entire catalogue. They differ in byte layout, not coverage. Your file is proof that a non-UTF-8 encoding of the same characters exists.

Other encodings you will meet: ASCII (7-bit, the historic core); ISO-8859-1 / latin-1 and Windows-1252, single-byte Western European sets; UTF-16LE/BE, used by Windows APIs and PowerShell 5.1 redirection; UTF-32; and regional legacy sets such as Shift_JIS, GB18030 and Big5. Note a trap in the single-byte ones: latin-1 maps all 256 byte values to characters, so it can never raise a decode error — it produces *mojibake*, silently wrong characters, instead of an exception. Failing loudly, as UTF-8 did for you, is the better outcome.

On the parenthetical: Unicode encodes Egyptian Hieroglyphs, Cuneiform, Linear B, Gothic, Runic and Old Italic among historic scripts, and Cherokee, Unified Canadian Aboriginal Syllabics (Inuktitut, Cree), Osage, Adlam, N'Ko, Vai and Tifinagh among indigenous and minority ones. Coverage of exactly these is a stated goal of the standard, not an afterthought. Nor is UTF-8 regional — it is roughly 98% of the web worldwide, having won because valid ASCII is already valid UTF-8.

The point where this comment connects to comment 0 is the important one, and it is the reason your own note did not help you diagnose your own error. Comments 0 and 7 do not contradict each other, but 7 shows the belief that made 0 inexplicable: "UTF-8 includes every character" is true and irrelevant. Decoding does not ask whether the alphabet contains a letter; it asks whether this byte sequence obeys this codec's structural rules — lead byte, then the right number of continuation bytes in `0x80`–`0xBF`. `FF FE` breaks that grammar on byte one. A codec's repertoire and a file's byte format are independent facts.

---

## Unprompted corrections

### 6. Fixing the encoding will not produce a message; the tags being searched for are not in the file (python_script.py)

#### Evidence in the code:
`tags.get("handler_name", "")` and `tags.get("title", "")`

#### Verdict:
Wrong - the belief that the decode error is the only thing standing between you and the hidden message is false; the JSON contains neither `handler_name` nor `title` on any stream, so the reconstruction returns the empty string.

#### Explanation:
I decoded your file correctly and enumerated the tag keys actually present. Stream 0 has `creation_time` and `language`. Stream 1 has `creation_time`, `language` and `encoder`. The `format` block has `major_brand`, `minor_version`, `compatible_brands` and `creation_time`. There is no `handler_name` and no `title` anywhere in the document.

Trace the consequence through the mechanism from entry 1: both lookups miss, both return their `""` default, `contenido` is empty for every stream, nothing is ever appended, the join over an empty list produces `""`. I ran the script's exact logic over the correctly decoded data and the final value is `''`. The program will print its success prefix followed by nothing, which reads as "it worked and the answer is blank" rather than as a failure.

Why this matters more than the encoding bug: an empty result is a *silent* wrong answer, and you would likely spend the session re-checking the decoding step that you had already fixed.

Two things I can state and one I cannot. Observable: those keys are absent. Also observable: the video stream carries `"encoder": "AVC Coding"`, and `AVC Coding` is a string that ordinarily appears as an mp4 video track's *handler_name*, which is at least suggestive. Inference I am not confident about: `handler_name` and `vendor_id` normally do appear in ffprobe's mp4 stream tags, sourced from the container's `hdlr` box, and ffmpeg's mov demuxer omits the entry when the handler name is empty — so their absence could mean the tracks genuinely have blank handler names, or that this JSON is not a faithful dump. What would settle it: running ffprobe directly against `steganography-2026-08-12.mp4` and comparing the stream tags to this file.

---

### 7. The `[+] Pista de acceso reconstruida:` prefix is printed unconditionally and is not a status report (python_script.py)

#### Evidence in the code:
`except Exception as err: return f"Error durante la reconstrucción: {str(err)}"`

#### Verdict:
Wrong - the belief that the line you quoted is one message the program produced about its reconstruction attempt is false; it is a fixed prefix concatenated with whatever the function returned, and the function returns failures and successes as the same type.

#### Explanation:
The output you pasted is two unrelated pieces. The `print` at the bottom emits its prefix every single time the function returns, with no knowledge of what happened inside. The rest is the return value. Because the `except` block converts the exception into a formatted string and *returns* it, a failure travels back through the identical channel as a success — both are `str`. The caller has no way to distinguish them, so it labels the error as a reconstructed passphrase.

The mechanism to internalise is what `except Exception as err` costs. Raising an exception normally unwinds the stack and prints a traceback: the file, the line number, and the full call chain. Catching it and returning `str(err)` discards all of that and keeps only the message text. That is why you learned *what* went wrong but not *where* — the traceback would have pointed at the `json.load` line and told you the read, not the open, was the failing operation, which is the single most useful fact in entry 0.

This also means the function currently has no failure mode a caller can detect. A missing file, a malformed JSON document, a decode error and a genuinely empty result all arrive at the print statement as a string behind a success prefix.

---

### 8. `if contenido:` is a truthiness test, not an existence test (python_script.py)

#### Evidence in the code:
`contenido = title if title else handler` and `if contenido:`

#### Verdict:
Wrong - the belief that these tests distinguish "the tag was found" from "the tag was missing" is false; they test *falsiness*, and an empty string is falsy, so a present-but-empty tag is indistinguishable from an absent one.

#### Explanation:
Python evaluates the truth value of an object, not its existence. The falsy values are `False`, `None`, numeric zero, and every empty container: `""`, `[]`, `{}`, `()`, `set()`. Everything else is truthy. So `if contenido:` asks "is this a non-empty string", and the conditional expression `A if cond else B` asks the same question of `title`.

Combined with `""` as the `.get` default from entry 1, this collapses three genuinely different situations into one indistinguishable outcome: the tag key was absent; the tag key was present with an empty value; the tag key was present with a value the code then dropped. All three produce a falsy `contenido` and the stream is skipped with no record that it existed.

For a reconstruction task, that is the expensive part. If a fragment for one stream were legitimately blank, or if a stream carried a fragment under a key you did not check, the result is simply a shorter message with no gap, no index skip, and no warning — the failure is invisible in the output rather than marked in it.

The generalisation that will bite elsewhere: `if x:` on a value that could legitimately be `0` or `""` treats that legitimate value as absent. This is the reason `if x is not None:` exists as a distinct and much narrower test, and the reason the `.get`-returns-`None`-for-a-`None`-value trap from entry 1 keeps mattering.

---

## Not addressed

- python_script.py comments 4 and 6 - no comments carrying these numbers exist in the file as provided; if they were written into another file or removed before you sent this, attach that version and they will be covered.
- metadatos.json - contains no context comments, and JSON has no comment syntax in which to write any; it was read as evidence for entries 0, 4 and 6 rather than annotated.
