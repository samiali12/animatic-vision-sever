import spacy
import re
from typing import List, Dict, Tuple
from enum import Enum

# Load once at import
nlp = spacy.load("en_core_web_sm")

class AnimeStyle(Enum):
    SHONEN = "shonen"
    SHOJO = "shojo"

class StoryProcessing:
    def __init__(
        self,
        target_duration: int = 25,
        max_scenes: int = 5,
        anime_style: AnimeStyle = AnimeStyle.SHONEN
    ):
        self.target_duration = target_duration
        self.max_scenes = max_scenes
        self.anime_style = anime_style
        self.min_scene_duration = 3

        self.style_settings = {
            AnimeStyle.SHONEN: {
                "camera": "dynamic_angles",
                "colors": "vibrant",
                "motion": "fast_paced"
            },
            AnimeStyle.SHOJO: {
                "camera": "close_ups",
                "colors": "soft_pastel",
                "motion": "gentle"
            }
        }

    def process_story(self, story_text: str) -> List[Dict]:
        print(f"Starting {self.anime_style.value.upper()} pipeline...")
        raw_scenes = self.split_into_scenes(story_text)
        self.adjust_duration(raw_scenes)
        return raw_scenes

    def split_into_scenes(self, story_text: str) -> List[Dict]:
        doc = nlp(story_text.strip())
        sentences = [s.text.strip() for s in doc.sents]
        sentences = sentences[:self.max_scenes]

        scenes = []
        for i, sent in enumerate(sentences):
            sent_doc = nlp(sent)
            characters = self.find_characters(sent)
            speaker, dialogue = self.extract_dialogue(sent)
            actions = self.find_actions(sent_doc, sent)
            mood = self.find_mood(sent)

            scene_data = {
                "scene_index": i,
                "description": sent,
                "duration": self.calculate_duration(sent),
                "characters": characters,
                "speaker": speaker,
                "dialogue": dialogue,
                "actions": actions,
                "mood": mood,
                "style": self.anime_style.value,
                "background_prompt": self.generate_bg_prompt(sent, mood, characters)
            }
            scenes.append(scene_data)
        return scenes

    def calculate_duration(self, sentence: str) -> int:
        base = self.min_scene_duration
        words = len(sentence.split())
        if words > 15:
            base += 1
        if '"' in sentence:
            base += 1
        return min(base, 6)

    def find_characters(self, sentence: str) -> List[str]:
        words = sentence.lower().split()
        known = ["boy", "girl", "man", "woman", "hero", "friend", "dragon", "teacher", "knight", "wolf", "king"]
        found = [w.capitalize() for w in known if w in words]
        return found or ["Character"]

    def extract_dialogue(self, sentence: str) -> Tuple[str | None, str | None]:
        m = re.search(r'"([^"]+)"\s*,?\s*(?:said|asked|shouted)\s+([A-Z][a-z]+)', sentence)
        if m:
            return m.group(2), m.group(1)
        m = re.search(r'^([A-Z][a-z]+)\s*:\s*"([^"]+)"', sentence)
        if m:
            return m.group(1), m.group(2)
        return None, None

    def find_actions(self, doc, sentence: str) -> List[str]:
        verb_lemmas = {token.lemma_.lower() for token in doc if token.pos_ == "VERB"}
        action_verbs = {
            "run", "jump", "fight", "talk", "smile", "cry", "find", "discover",
            "wave", "fly", "shout", "laugh", "dance", "grip", "land", "hit",
            "kick", "punch", "throw", "catch", "walk", "sit", "stand"
        }
        found = [v for v in verb_lemmas if v in action_verbs][:2]
        prefix = "dynamic_" if self.anime_style == AnimeStyle.SHONEN else "gentle_"
        return [f"{prefix}{v}" for v in found] or ["stand"]

    def find_mood(self, sentence: str) -> str:
        s = sentence.lower()
        if any(w in s for w in ["fight", "battle", "power", "run", "jump", "shout", "sword"]):
            return "exciting"
        if any(w in s for w in ["love", "heart", "beautiful", "kiss", "hug"]):
            return "romantic"
        if any(w in s for w in ["sad", "cry", "tear", "miss", "lonely"]):
            return "emotional"
        return "neutral"

    def generate_bg_prompt(self, desc: str, mood: str, characters: List[str]) -> str:
        style = "shonen anime style, vibrant colors" if self.anime_style == AnimeStyle.SHONEN else "shojo anime style, soft pastel"
        setting = desc.split(" in ")[-1].split(" at ")[-1].split(".")[0] if " in " in desc or " at " in desc else "scene"
        return f"{setting}, {', '.join(characters)}, {mood} mood, {style}, detailed background, 2D animation"

    def total_duration(self, scenes: List[Dict]) -> int:
        return sum(s['duration'] for s in scenes)

    def adjust_duration(self, scenes: List[Dict]) -> None:
        total = self.total_duration(scenes)
        while total < self.target_duration and any(s['duration'] < 6 for s in scenes):
            for s in scenes:
                if s['duration'] < 6:
                    s['duration'] += 1
                    total += 1
                    break
        while total > self.target_duration + 5 and any(s['duration'] > self.min_scene_duration for s in scenes):
            for s in scenes:
                if s['duration'] > self.min_scene_duration:
                    s['duration'] -= 1
                    total -= 1
                    break