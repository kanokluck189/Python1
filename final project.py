# =============================
# Malakor Eng Utility App 
# =============================

def is_vowel(c):
    return c.lower() in "aeiou"

def split_syllables(word):
    vowels = "aeiou" 
    consonants = "bcdfghjklmnpqrstvwxyz"
    word_lower = word.lower()
    syllables = []

    # Edge cases: short word <=3, consonant+e, word ends with y
    if len(word) <= 3 or (
        len(word) >= 2 and word_lower[-2] in consonants and word_lower[-1] == "e"
        ) or word_lower.endswith("y"):
        return [word_lower]

    i = 0
    length = len(word_lower)
    while i < length:
        start = i
        # Leading consonants
        while i < length and word_lower[i] in consonants:
            i += 1
        # At least one vowel
        if i < length and is_vowel(word_lower[i]):
            i += 1
        # Trailing consonants until next vowel
        while i < length and (i+1 >= length or not is_vowel(word_lower[i+1])):
            i += 1
        syllables.append(word_lower[start:i])
    return syllables

# =============== EN → MALAKOR ===============
def malakor_eng(word):
    syllables = split_syllables(word)
    consonants = "bcdfghjklmnpqrstvwxyz"
    malakor_syllables = []

    for syl in syllables:
        if not syl:
            continue

        cluster = ""
        rest = syl
        max_cluster_len = min(3, len(syl))
        consonants_lower = set(consonants)

        # Short word or ends with y -> cluster = first consonant
        if len(syl) <= 3 or syl.endswith("y"):
            cluster = syl[0]
            rest = syl[1:]
        else:
            # Find cluster at start
            for j in range(max_cluster_len, 0, -1):
                if all(c.lower() in consonants_lower for c in syl[:j]):
                    cluster = syl[:j]
                    rest = syl[j:]
                    break
            if not cluster:
                cluster = syl[0]
                rest = syl[1:]

            # Fix for case cluster = whole syllable
            if not rest:
                rest = cluster

        mal_syl = f"{cluster}a la g{rest}"
        malakor_syllables.append(mal_syl)

    return " / ".join(malakor_syllables)
  
# =============== MALAKOR → EN  ===================
def eng_from_malakor(mal_text):
    mal_text = mal_text.lower().strip()
    # Split by '/' or '  ' (two or more spaces)
    parts = []
    temp = ""
    for ch in mal_text:
        if ch == "/":
            if temp.strip():
                parts.append(temp.strip())
            temp = ""
        else:
            temp += ch
    if temp.strip():
        parts.append(temp.strip())

    english_words = []

    for phrase in parts:
        tokens = phrase.split()
        combined = ""
        i = 0
        while i < len(tokens):
            if (i + 2 < len(tokens)
                and tokens[i + 1] == "la"
                and tokens[i + 2].startswith("g")):
                cluster = tokens[i][:-1] if tokens[i].endswith("a") else tokens[i]
                rest = tokens[i + 2][1:]  # skip 'g'
                combined += cluster + rest
                i += 3
            else:
                combined += tokens[i]
                i += 1
        english_words.append(combined)

    return " ".join(english_words)


# =============================
# Main Program
# =============================

def main():
    print("==== Malakor Eng Utility App ====\n")
    print("This tool converts between English and 'Malakor Eng' language.\n")

    print("🧭 MODE GUIDE:")
    print("  0 → English → Malakor Eng")
    print("  1 → Malakor Eng → English")
    print("  2 → Exit\n")

    print("📘 INPUT RULES:")
    print("- Always type as STRING (letters only, not numbers). Example: 'cat', 'sky', 'shine'.")
    print("- For multiple English words, separate with a SPACE. Example: 'wake up'.")
    print("- For Malakor input, separate syllables with SPACES and words with '/'.")
    print("  Example: 'fa la gly / ha la gigh'  →  fly high\n")
    print("- Do NOT type quotes, int, or float values — only plain text.\n")

    while True:
        mode = input("Choose mode (0/1/2): ").strip()

        if mode == "2":
            print("\nGoodbye 👋")
            break

        elif mode == "0":
            text = input("\nEnter English word(s): ").strip()
            if not text:
                print("Please enter some text!\n")
                continue
            words = text.split()
            result = " | ".join(malakor_eng(w) for w in words)
            print(f"Malakor Eng: {result}\n")

        elif mode == "1":
            text = input("\nEnter Malakor Eng text: ").strip()
            if not text:
                print("Please enter Malakor text!\n")
                continue
            result = eng_from_malakor(text)
            print(f"English: {result}\n")

        else:
            print("Invalid choice! Please enter 0, 1, or 2.\n")

# =============================
# Run
# =============================
if __name__ == "__main__":
    main()
