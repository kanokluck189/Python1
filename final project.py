# =============================
# Malakor Eng Utility App 
# =============================

def is_vowel(character: str) -> bool:
    """Check if a character is a vowel."""
    return character.lower() in "aeiou"


def split_syllables(word: str) -> list[str]:
    """Split an English word into approximate syllables."""
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"
    word_lower = word.lower()
    syllable_list = []

    # Handle short or special-case words
    if (
        len(word) <= 3
        or (
            len(word) >= 2
            and word_lower[-2] in consonants
            and word_lower[-1] == "e"
        )
        or word_lower.endswith("y")
    ):
        return [word_lower]

    position = 0
    word_length = len(word_lower)

    while position < word_length:
        start_index = position

        # Leading consonants
        while position < word_length and word_lower[position] in consonants:
            position += 1

        # At least one vowel
        if position < word_length and is_vowel(word_lower[position]):
            position += 1

        # Trailing consonants until next vowel
        while (
            position < word_length
            and (position + 1 >= word_length or not is_vowel(
                word_lower[position + 1]
            ))
        ):
            position += 1

        syllable_list.append(word_lower[start_index:position])

    return syllable_list


# =============== EN → MALAKOR ===============

def convert_english_to_malakor(word: str) -> str:
    """Convert an English word to Malakor Eng format."""
    syllable_list = split_syllables(word)
    consonants = "bcdfghjklmnpqrstvwxyz"
    malakor_syllables = []

    for syllable in syllable_list:
        if not syllable:
            continue

        consonant_cluster = ""
        remainder = syllable
        max_cluster_length = min(3, len(syllable))
        consonant_set = set(consonants)

        # Handle short word or ending with 'y'
        if len(syllable) <= 3 or syllable.endswith("y"):
            consonant_cluster = syllable[0]
            remainder = syllable[1:]
        else:
            # Detect leading consonant cluster
            for cluster_length in range(max_cluster_length, 0, -1):
                if all(
                    char.lower() in consonant_set
                    for char in syllable[:cluster_length]
                ):
                    consonant_cluster = syllable[:cluster_length]
                    remainder = syllable[cluster_length:]
                    break

            # Default fallback if none found
            if not consonant_cluster:
                consonant_cluster = syllable[0]
                remainder = syllable[1:]

            # Edge case: entire syllable is consonant cluster
            if not remainder:
                remainder = consonant_cluster

        malakor_form = f"{consonant_cluster}a la g{remainder}"
        malakor_syllables.append(malakor_form)

    return " / ".join(malakor_syllables)


# =============== MALAKOR → EN  ===============

def convert_malakor_to_english(malakor_text: str) -> str:
    """Convert Malakor Eng text back to English."""
    malakor_text = malakor_text.lower().strip()

    # Split by '/' (word separator)
    malakor_words = []
    current_phrase = ""

    for character in malakor_text:
        if character == "/":
            if current_phrase.strip():
                malakor_words.append(current_phrase.strip())
            current_phrase = ""
        else:
            current_phrase += character

    if current_phrase.strip():
        malakor_words.append(current_phrase.strip())

    english_words = []

    for malakor_word in malakor_words:
        tokens = malakor_word.split()
        reconstructed_word = ""
        token_index = 0

        while token_index < len(tokens):
            # Pattern: "<cluster>a la g<rest>"
            if (
                token_index + 2 < len(tokens)
                and tokens[token_index + 1] == "la"
                and tokens[token_index + 2].startswith("g")
            ):
                cluster_part = (
                    tokens[token_index][:-1]
                    if tokens[token_index].endswith("a")
                    else tokens[token_index]
                )
                rest_part = tokens[token_index + 2][1:]  # remove 'g'
                reconstructed_word += cluster_part + rest_part
                token_index += 3
            else:
                reconstructed_word += tokens[token_index]
                token_index += 1

        english_words.append(reconstructed_word)

    return " ".join(english_words)


# =============================
# Main Program
# =============================

def main() -> None:
    """Run the main interactive program."""
    print("==== Malakor Eng Utility App ====\n")
    print("This tool converts between English and 'Malakor Eng' language.\n")

    print("🧭 MODE GUIDE:")
    print("  0 → English → Malakor Eng")
    print("  1 → Malakor Eng → English")
    print("  2 → Exit\n")

    print("📘 INPUT RULES:")
    print("- Always type as STRING (letters only, not numbers). "
          "Example: 'cat', 'sky', 'shine'.")
    print("- For multiple English words, separate with a SPACE. "
          "Example: 'wake up'.")
    print("- For Malakor input, separate syllables with SPACES "
          "and words with '/'.")
    print("  Example: 'fa la gly / ha la gigh'  →  fly high\n")
    print("- Do NOT type quotes, int, or float values — only plain text.\n")

    while True:
        mode_choice = input("Choose mode (0/1/2): ").strip()

        if mode_choice == "2":
            print("\nGoodbye 👋")
            break

        elif mode_choice == "0":
            english_text = input("\nEnter English word(s): ").strip()
            if not english_text:
                print("Please enter some text!\n")
                continue

            english_words = english_text.split()
            converted_result = " | ".join(
                convert_english_to_malakor(word) for word in english_words
            )
            print(f"Malakor Eng: {converted_result}\n")

        elif mode_choice == "1":
            malakor_input = input("\nEnter Malakor Eng text: ").strip()
            if not malakor_input:
                print("Please enter Malakor text!\n")
                continue

            converted_result = convert_malakor_to_english(malakor_input)
            print(f"English: {converted_result}\n")

        else:
            print("Invalid choice! Please enter 0, 1, or 2.\n")


# =============================
# Run
# =============================
if __name__ == "__main__":
    main()
