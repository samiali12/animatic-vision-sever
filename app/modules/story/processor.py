# modules/story/processing.py
import spacy
import re
from typing import List, Dict
from enum import Enum

# Load once
nlp = spacy.load("en_core_web_sm")

class AnimeStyle(Enum):
    SHONEN = "shonen"
    SHOJO = "shojo"


class StoryProcessing:
    def __init__(
        self,
        target_duration: int = 25,
        max_scenes: int = 5,
        anime_style: AnimeStyle = AnimeStyle.SHONEN,
    ):
        self.target_duration = target_duration
        self.max_scenes = max_scenes
        self.anime_style = anime_style
        self.min_scene_duration = 3

    def process_story(self, story_text: str) -> List[Dict]:
        raw_scenes = self.split_into_scenes(story_text)
        self.adjust_duration(raw_scenes)
        return raw_scenes

    def split_into_scenes(self, story_text: str) -> List[Dict]:
        doc = nlp(story_text.strip())
        sentences = [s.text.strip() for s in doc.sents if s.text.strip()]
        sentences = sentences[: self.max_scenes]

        scenes = []
        for i, sent in enumerate(sentences):
            characters = self.extract_characters(sent)
            bg_prompt = self.generate_background_prompt(sent, characters)
            char_prompts = self.generate_character_prompts(characters)

            scene_data = {
                "scene_index": i,
                "description": sent,
                "background_prompt": bg_prompt,
                "character_prompts": char_prompts,  # ← JSON list
            }
            scenes.append(scene_data)
        return scenes

    def extract_characters(self, sentence: str) -> List[str]:
        """Find 1–3 character names from sentence"""
        doc = nlp(sentence)
        # Look for proper nouns (likely characters)
        candidates = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG"]]
        if not candidates:
            # Fallback: common roles
            keywords = ["knight", "princess", "dragon", "wolf", "king", "hero", "girl", "boy"]
            candidates = [w for w in keywords if w in sentence.lower()]
        return list(dict.fromkeys(candidates))[:3]  # dedupe + max 3

    def generate_background_prompt(self, desc: str, characters: List[str]) -> str:
        style = "shonen anime style, vibrant colors" if self.anime_style == AnimeStyle.SHONEN else "shojo anime style, soft pastel"
        mood = self.detect_mood(desc)
        setting = self.extract_setting(desc)
        return f"{setting}, {', '.join(characters)}, {mood} mood, {style}, detailed background, 2D animation"

    def generate_character_prompts(self, characters: List[str]) -> List[str]:
        """One prompt per character → transparent PNG"""
        base = "anime style, detailed, transparent background, character only"
        style_suffix = ", shonen" if self.anime_style == AnimeStyle.SHONEN else ", shojo"
        return [f"{char}{style_suffix}, {base}" for char in characters or ["Character"]]

    def detect_mood(self, sentence: str) -> str:
        s = sentence.lower()
        if any(w in s for w in ["fight", "battle", "run", "shout", "sword"]):
            return "exciting"
        if any(w in s for w in ["love", "kiss", "hug", "heart"]):
            return "romantic"
        if any(w in s for w in ["sad", "cry", "tear", "lonely"]):
            return "emotional"
        return "neutral"

    def extract_setting(self, sentence: str) -> str:
        s = sentence.lower()
        settings = {
            "forest": "dense forest, tall trees",
            "cave": "dark cave, glowing crystals",
            "river": "rushing river, rocks",
            "castle": "grand castle, stone walls",
            "village": "cozy village, wooden houses",
            "mountain": "snowy mountain peak",
        }
        for key, prompt in settings.items():
            if key in s:
                return prompt
        return "scene"

    def calculate_duration(self, sentence: str) -> int:
        words = len(sentence.split())
        base = self.min_scene_duration
        if words > 20:
            base += 2
        elif words > 10:
            base += 1
        return min(max(base, 3), 8)

    def total_duration(self, scenes: List[Dict]) -> int:
        return sum(self.calculate_duration(s["description"]) for s in scenes)

    def adjust_duration(self, scenes: List[Dict]) -> None:
        total = self.total_duration(scenes)
        target = self.target_duration

        # Increase
        while total < target and any(self.calculate_duration(s["description"]) < 8 for s in scenes):
            for s in scenes:
                if self.calculate_duration(s["description"]) < 8:
                    total += 1
                    break

        # Decrease
        while total > target + 5 and any(self.calculate_duration(s["description"]) > 3 for s in scenes):
            for s in scenes:
                if self.calculate_duration(s["description"]) > 3:
                    total -= 1
                    break