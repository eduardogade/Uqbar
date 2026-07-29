# SPDX-License-Identifier: MIT
# uqbar/acta/prompt_maker.py
"""
Acta Diurna | Prompt Maker
==========================

Overview
--------
Placeholder.

Metadata
--------
- Project: Acta diurna
- License: MIT
"""

# -------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------
from __future__ import annotations

import re
from pathlib import Path
from collections.abc import Iterable
from datetime import datetime

from uqbar.acta.trends import Trend, TrendList

# -------------------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------------------

# Get the current local date and time as a datetime object
NOW: str = str(datetime.now())

OUT: Path = Path("/Users/egg/Desktop")


DEFAULT_PROMPT_TTS_PATH: Path = OUT / "tts.txt"

DEFAULT_PROMPT_IMAGE_KEYWORD_PATH: Path = OUT / "image_keyword.txt"

DEFAULT_PROMPT_IMAGE_SCALE_PATH: Path = OUT / "image_scale.txt"

DEFAULT_PROMPT_MOOD_PATH: Path = OUT / "mood.txt"

DEFAULT_PROMPT_THUMB_IMAGE_PATH: Path = OUT / "thumb_image.txt"

DEFAULT_PROMPT_THUMB_BACK_PATH: Path = OUT / "thumb_background.txt"

DEFAULT_PROMPT_THUMB_SCALE_PATH: Path = OUT / "thumb_scale.txt"


# Rulers
BIG_RULER_LEN: int = 170

SMALL_RULER_LEN: int = 25

# Other Parameters
TOTAL_TEXT_WORDS: int = 1_000

TOTAL_IMAGE_KEYWORD_WORDS: int = 5

TOTAL_THUMB_PROMPT_WORDS: int = 50


# Regular expressions
BIG_RULER_RE = re.compile(rf"^-{{{BIG_RULER_LEN}}}")

SMALL_RULER_RE = re.compile(rf"^-{{{SMALL_RULER_LEN}}}")

PROMPT_HEADER_RE = re.compile(
    r"^> TREND PROMPTS \[(?P<prompt_number>\d+) of (?P<prompt_total>\d+)\]"
)


# --------------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------------
# def _get_prompt_string(
#     is_last: bool,
#     news_url_list: list[str],
#     current_count: int,
#     total_count: int,
#     *,
#     total_word_count: int = TOTAL_WORD_COUNT,
#     summary_word_count: int = SUMMARY_WORD_COUNT,
#     total_word_image_count: int = TOTAL_WORD_IMAGE_COUNT,
#     small_ruler_len: int = SMALL_RULER_LEN,
#     big_ruler_len: int = BIG_RULER_LEN,
# ) -> tuple[str, str]:

#     first_ruler: str = f"{'-'*big_ruler_len}\n\n"
#     last_ruler: str = "\n"
#     if is_last:
#         first_ruler: str = f"{'-'*big_ruler_len}\n\n"
#         last_ruler: str = ""

#     regular_prompt: str = (
#         f"1. Goal: Write a Continuous Prose as a Professional Calm News-Media "
#         f"Narrator, targeting a General Audience; synthesizing these three news "
#         f"sources, which report the same facts with minor framing differences:\n"
#         f"    1.1. {news_url_list[0]}\n"
#         f"    1.2. {news_url_list[1]}\n"
#         f"    1.3. {news_url_list[2]}\n"
#         f"\n"
#         f"2. Length of text: ~{total_word_count:,} words (±20%).\n"
#         f"\n"
#         f"3. Style:\n"
#         f"    3.1. Predominantly in a news-style impersonal voice.\n"
#         f"    3.2. Hook the reader with mystery in the first 2–3 sentences.\n"
#         f"    3.3. Develop the news arc while maintaining mystery.\n"
#         f"    3.4. Release the mystery once the reader’s full attention is secured.\n"
#         f"    3.5. Fill the remainder of the report with background and established "
#         f"facts.\n"
#         f"\n"
#         f"4. Optimize the textual flow for neural TTS. Minor trimming after "
#         f"generation is acceptable. Keep sentences short to medium in length.\n"
#         f"\n"
#         f"5. Constraints:\n"
#         f"    5.1. Create mystery and tension. Atmospheric or metaphorical "
#         f"language is allowed, but do not introduce false factual claims.\n"
#         f"    5.2. Adopt a news-anchor storytelling tone. Avoid excessive "
#         f"LinkedIn-style seriousness or job-market structure.\n"
#         f"    5.3. Avoid hyphens and other TTS-unfriendly characters.\n"
#         f"\n"
#         f"6. Please return each in a separate triple-backtick codebox:\n"
#         f"    6.1. The full text.\n"
#         f"    6.2. A ~{summary_word_count}-words (±20%) summary of the full text "
#         f"in another triple-backtick code block.\n"
#         f"    6.3. A semicolon-separated list of the TOP ~{total_word_image_count} "
#         f"most representative keywords (±20%), **optimised for a google-like "
#         f"search**.\n"
#         f"    6.4. A single word, most representative of the **mood that an average "
#         f"person would feel when seeing such news story**.\n"
#         f"\n"
#         f"7. Do **return only the four triple-backtick codeboxes mentioned above**, "
#         f"stacked and in order. Do **NOT** return anything else.\n"
#     )

#     special_prompt: str = (
#         f"{first_ruler}"
#         f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
#         f"\n"
#         f"Honeybun,\n"
#         f"\n"
#         f"{regular_prompt}\n"
#         f"\n"
#         f"{'-'*small_ruler_len}\n"
#         f"\n"
#         f"XXXXX\n"
#         f"{last_ruler}"
#     )

#     return regular_prompt, special_prompt

def _get_tts_prompt_string(
    is_last: bool,
    news_url_list: list[str],
    current_count: int,
    total_count: int,
    *,
    total_word_count: int = TOTAL_TEXT_WORDS,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"You are a professional broadcast journalist.\n"
        f"\n"
        f"GOAL:\n"
        f"Write a continuous news report that synthesizes the\n"
        f"following three sources. They report the same core\n"
        f"event but may differ in framing or emphasis.\n"
        f"\n"
        f"SOURCES:\n"
        f"1) {news_url_list[0]}\n"
        f"2) {news_url_list[1]}\n"
        f"3) {news_url_list[2]}\n"
        f"\n"
        f"LENGTH:\n"
        f"Approximately {total_word_count} words (±20%).\n"
        f"\n"
        f"STYLE REQUIREMENTS:\n"
        f"- Neutral, calm, authoritative tone.\n"
        f"- Written for a general audience.\n"
        f"- First 2–3 sentences should create curiosity\n"
        f"  or tension without exaggeration.\n"
        f"- Gradually clarify the core facts.\n"
        f"- After the reveal, provide background,\n"
        f"  context, and confirmed details.\n"
        f"\n"
        f"TTS OPTIMIZATION:\n"
        f"- Use short to medium sentences.\n"
        f"- Avoid hyphens, emojis, bullet lists,\n"
        f"  and special symbols.\n"
        f"- Avoid parentheses.\n"
        f"- Avoid excessive commas.\n"
        f"- No URLs in the final text.\n"
        f"\n"
        f"FACTUAL CONSTRAINTS:\n"
        f"- Do NOT invent facts.\n"
        f"- If sources disagree, describe the\n"
        f"  disagreement neutrally.\n"
        f"- Do NOT speculate beyond reported facts.\n"
        f"\n"
        f"OUTPUT FORMAT:\n"
        f"Return ONLY the final continuous prose\n"
        f"inside a single triple backtick code block.\n"
        f"Do NOT return commentary or explanations.\n"
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _get_image_keyword_prompt_string(
    is_last: bool,
    main_news_text: str,
    current_count: int,
    total_count: int,
    *,
    n_keywords: int = TOTAL_IMAGE_KEYWORD_WORDS,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"Extract the core visual entities from the "
        f"following news report. Focus only on concrete, "
        f"photographable subjects such as people, "
        f"locations, objects, institutions, events, "
        f"vehicles, infrastructure, symbols, and "
        f"geopolitical actors. Avoid abstract concepts. "
        f"Avoid emotions. Avoid analysis.\n"
        f"\n"
        f"NEWS TEXT:\n"
        f"{main_news_text}\n"
        f"\n"
        f"Return exactly {n_keywords} distinct terms "
        f"that would work as effective image search "
        f"queries. Use short noun phrases. "
        f"No full sentences. No explanations."
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _get_mood_prompt_string(
    is_last: bool,
    main_news_text: str,
    current_count: int,
    total_count: int,
    *,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"Determine the emotional tone conveyed by the "
        f"following news report. Focus on the emotional "
        f"impact on an average reader.\n"
        f"\n"
        f"{main_news_text}\n"
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _get_thumbnail_prompt_image_prompt_string(
    is_last: bool,
    main_news_text: str,
    current_count: int,
    total_count: int,
    *,
    total_thumb_prompt_words: int = TOTAL_THUMB_PROMPT_WORDS,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"Goal: Write ONE image prompt for a 512x512 news "
        f"thumbnail.\n"
        f"\n"
        f"Input news text:\n"
        f"{main_news_text}\n"
        f"\n"
        f"Rules:\n"
        f"1. Pick ONE dominant real-world subject.\n"
        f"2. Describe a simple scene with that subject.\n"
        f"3. Centered composition. Clean background.\n"
        f"4. Neutral lighting. High contrast.\n"
        f"5. No text. No captions. No logos.\n"
        f"6. No metaphor. No symbolism.\n"
        f"\n"
        f"Length:\n"
        f"- Output must be at most {total_thumb_prompt_words} "
        f"words.\n"
        f"- Prefer 40 to 60 words.\n"
        f"\n"
        f"Output:\n"
        f"Return ONLY the final image prompt, nothing else.\n"
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _get_thumbnail_background_prompt_string(
    is_last: bool,
    thumbnail_main_prompt: list[str],
    current_count: int,
    total_count: int,
    *,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"Enhance the following thumbnail concept with a "
        f"clean modern visual style suitable for online "
        f"news media.\n"
        f"\n"
        f"Base subject:\n"
        f"{thumbnail_main_prompt}\n"
        f"\n"
        f"Apply:\n"
        f"1. Subtle depth of field.\n"
        f"2. Soft background gradient or light texture.\n"
        f"3. High clarity on main subject.\n"
        f"4. Professional lighting, neutral color tone.\n"
        f"5. Slight contrast boost.\n"
        f"6. Minimal composition, no clutter.\n"
        f"\n"
        f"Constraints:\n"
        f"- No text.\n"
        f"- No logos.\n"
        f"- No watermark.\n"
        f"- No dramatic exaggeration.\n"
        f"\n"
        f"Return only the final image-generation prompt.\n"
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _get_thumbnail_upscale_prompt_string(
    is_last: bool,
    current_count: int,
    total_count: int,
    *,
    small_ruler_len: int = SMALL_RULER_LEN,
    big_ruler_len: int = BIG_RULER_LEN,
) -> tuple[str, str]:

    first_ruler: str = f"{'-'*big_ruler_len}\n\n"
    last_ruler: str = "\n"
    if is_last:
        first_ruler: str = f"{'-'*big_ruler_len}\n\n"
        last_ruler: str = ""

    regular_prompt: str = (
        f"Upscale and enhance the provided thumbnail image "
        f"to high resolution while preserving composition.\n"
        f"\n"
        f"Instructions:\n"
        f"1. Do not alter subject or layout.\n"
        f"2. Do not add new objects.\n"
        f"3. Improve sharpness and fine details.\n"
        f"4. Enhance edges and texture clarity.\n"
        f"5. Maintain original colors and lighting.\n"
        f"6. Keep background clean and minimal.\n"
        f"\n"
        f"Goal: Produce a crisp, high-resolution news "
        f"thumbnail suitable for web display.\n"
    )

    special_prompt: str = (
        f"{first_ruler}"
        f"> TREND PROMPTS [{current_count:02d} of {total_count:02d}]\n"
        f"\n"
        f"Honeybun,\n"
        f"\n"
        f"{regular_prompt}\n"
        f"\n"
        f"{'-'*small_ruler_len}\n"
        f"\n"
        f"XXXXX\n"
        f"{last_ruler}"
    )

    return regular_prompt, special_prompt


def _flush_prompt(
    prev_id: int,
    curr_result: list[str] | None,
) -> list[str] | None:
    """Returns chunked prompt results"""

    if curr_result is None:
        print(f"Error at flush_prompt(): prev_id = {prev_id}")
        print("Table does not exist or is empty. Go get more data please.")
        return None

    # Create Story Chunks
    curr_chunk: list[str] = []
    story_chunk_list: list[str] = []
    for cline in curr_result:

        curr_chunk.append(cline)
        if len(cline) <= 2:
            story_chunk_list.append("".join(curr_chunk))
            curr_chunk: list[str] = []

    # Update prompt result list
    return story_chunk_list


# --------------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------------
# def create_trend_prompt(
#     trend_list: TrendList,
#     *,
#     prompt_file_path: Path = DEFAULT_PROMPT_TTS_PATH,
#     overwrite_file: bool = False,
#     write_file: bool = False,
# ) -> TrendList:
#     """
#     Create Trends Prompt for Chat GPT or OpenRouter models.
#     """

#     # Check file
#     prompt_file_path.parent.mkdir(parents=True, exist_ok=True)
#     if prompt_file_path.exists() and not overwrite_file:
#         print("prompt_file_path does not exist.")
#         return trend_list

#     # Check length of multi-prompt
#     total_size: int = len(trend_list)

#     # Iterate through trends
#     for counter, trend in enumerate(trend_list, start=1):

#         # Get news_url_list
#         news_url_list: list[str] = [
#             e for e in [
#                 trend.news_item_url_1,
#                 trend.news_item_url_2,
#                 trend.news_item_url_3,
#             ] if e
#         ]

#         tts_prompt_query, file_prompt_query = _get_prompt_string(
#             is_last=counter == total_size,
#             news_url_list=news_url_list,
#             current_count=counter,
#             total_count=total_size,
#         )

#         trend.tts_prompt_query = tts_prompt_query
#         trend.tts_file_prompt_query = file_prompt_query

#     # Check whether to write in a file
#     if not write_file:
#         return trend_list

#     # Write Output to file and return Path
#     with open(prompt_file_path, "w") as file:
#         for trend in trend_list:
#             if trend and isinstance(trend.tts_file_prompt_query, str):
#                 file.write(trend.tts_file_prompt_query)

#     return trend_list


def create_trend_prompt(
    trend_list: TrendList,
    *,
    prompt_file_path: Path = DEFAULT_PROMPT_TTS_PATH,
    overwrite_file: bool = False,
    write_file: bool = False,
) -> TrendList:
    """
    Create Trends Prompt for Chat GPT or OpenRouter models.
    """

    # Check file
    prompt_file_path.parent.mkdir(parents=True, exist_ok=True)
    if prompt_file_path.exists() and not overwrite_file:
        print("prompt_file_path does not exist.")
        return trend_list

    # Check length of multi-prompt
    total_size: int = len(trend_list)

    # Iterate through trends
    for counter, trend in enumerate(trend_list, start=1):

        # Get news_url_list
        news_url_list: list[str] = [
            e for e in [
                trend.news_item_url_1,
                trend.news_item_url_2,
                trend.news_item_url_3,
            ] if e
        ]

        tts_prompt_query, file_prompt_query = _get_prompt_string(
            is_last=counter == total_size,
            news_url_list=news_url_list,
            current_count=counter,
            total_count=total_size,
        )

        trend.tts_prompt_query = tts_prompt_query
        trend.tts_file_prompt_query = file_prompt_query

    # Check whether to write in a file
    if not write_file:
        return trend_list

    # Write Output to file and return Path
    with open(prompt_file_path, "w") as file:
        for trend in trend_list:
            if trend and isinstance(trend.tts_file_prompt_query, str):
                file.write(trend.tts_file_prompt_query)

    return trend_list


def read_trend_prompt(
    *,
    prompt_file_path: Path = DEFAULT_PROMPT_TTS_PATH,
) -> list[list[str]]:
    """
    Placeholder.
    """

    prev_id: int = 0

    curr_result: list[str] = []
    prompt_result_list: list[list[str]] = []

    inside_prompt: bool = False
    inside_result: bool = False
    inside_result_idx: int = 0

    # Reading file
    file_lines: list[str] = []
    with open(prompt_file_path, encoding="utf-8") as file:

        for line in file:

            file_lines.append(line)

    for counter, line in enumerate(file_lines, start=1):

        sline = line.strip()

        # Try to match
        big_ruler_match: bool = BIG_RULER_RE.match(line) is not None

        # Start of prompt
        if big_ruler_match:
            inside_prompt: bool = True
            inside_result: bool = False

        # Inside Results
        if inside_result:

            if inside_result_idx == 0:
                inside_result_idx += 1
                continue

            elif inside_result_idx >= 1:

                # Newline, end of prompt, end of file
                if len(sline) == 0:

                    # End of file
                    try:
                        file_lines[counter]
                    except Exception:
                        break

                    # End of prompt
                    if "-----" in file_lines[counter]:
                        inside_result: bool = False
                        inside_prompt: bool = False
                        inside_result_idx: int = 0
                        continue

                    # Just newline
                    curr_result.append(line)
                    inside_result_idx += 1
                    continue

                # Regular line with result
                curr_result.append(sline)
                inside_result_idx += 1
                continue

        # Inside prompt - wait for small ruler or header
        if inside_prompt:

            # Check header
            pmatch = PROMPT_HEADER_RE.match(sline)
            prompt_header_match: bool = pmatch is not None
            if prompt_header_match and pmatch is not None:

                prompt_number: int = int(pmatch.group("prompt_number"))
                int(pmatch.group("prompt_total"))
                curr_id: int = prompt_number

                cond_id: bool = False
                if prev_id:
                    cond_id: bool = curr_id != prev_id

                if cond_id:
                    prompt_results = _flush_prompt(prev_id, curr_result)
                    if prompt_results is not None:
                        prompt_result_list.append([e for e in prompt_results if e])
                    curr_result: list[str] = []

                prev_id: int = curr_id
                prompt_header_match: bool = False

            # If still in big ruler, small ruller will match also
            # To prevent that, stop early if in big ruller line
            if big_ruler_match:
                big_ruler_match: bool = False
                continue

            # Try to match end of prompt
            small_ruler_match: bool = SMALL_RULER_RE.match(sline) is not None

            # End of prompt
            if small_ruler_match:
                inside_prompt: bool = False
                inside_result: bool = True
                small_ruler_match: bool = False
                inside_result_idx: int = 0

    if curr_result:
        prompt_results = _flush_prompt(prev_id, curr_result)
        if isinstance(prompt_results, Iterable):
            prompt_result_list.append([e for e in prompt_results if e])

    # Return the prompt result list chunked
    return prompt_result_list


# --------------------------------------------------------------------------------------
# Exports
# --------------------------------------------------------------------------------------
__all__: list[str] = [
    "create_trend_prompt",
    "read_trend_prompt",
]


# -------------------------------------------------------------------------------------
# Test | python -m uqbar.acta.trend_prompt_parser > out.txt 2>&1
# -------------------------------------------------------------------------------------
# if __name__ == "__main__":
