Writing Your Own Skills
A skill is a small Python class with two methods: match(text) decides if the skill should handle the message, and run(text, jarvis) returns the reply. Skills run before the AI, so they are instant and free.
Example
from jarvis import Jarvis
from jarvis.skills import Skill


class Coin(Skill):
    name = "coin"
    description = "Flip a coin"

    def match(self, text: str) -> bool:
        return text.strip().lower() == "flip a coin"

    def run(self, text: str, jarvis: Jarvis) -> str:
        import random
        return random.choice(["Heads", "Tails"])


jarvis = Jarvis()
jarvis.register_skill(Coin())
print(jarvis.ask("flip a coin"))
Tips
Match precisely (exact phrases or a clear prefix) so normal questions still reach the AI.
Use jarvis.memory to store data and jarvis.settings to read configuration.
Never use eval or exec on user input.
Keep skills fast. Use timeouts for network calls.
Making it permanent
Add your class to default_skills() in jarvis/skills/__init__.py (or a new file in jarvis/skills/), add a test in tests/, and open a pull request.
