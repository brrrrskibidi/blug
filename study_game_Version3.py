import random
import json

# ====== CONFIGURATION ======
SKOINS_PER_QUESTION = 5
UPGRADE_COSTS = {
    "Power Boost": 100,
    "Double Skoins": 200,
    "Extra Ability Slot": 150,
}
CHARACTER_UNLOCK_COST = 250
REBIRTH_LEVEL = 10
REBIRTH_PERK = "Permanent Skoins Boost"
SECRET_CHARACTER = "Dragon"
SECRET_ABILITIES = ["Inferno", "Flight", "Wisdom"]
SAVE_FILE = "savegame.json"

# ====== CHARACTER ======
class Character:
    def __init__(self, name, abilities=None, level=1, skoins=0, upgrades=None, rebirths=0, permanent_skoins_boost=1, extra_ability_slots=0):
        self.name = name
        self.skoins = skoins
        self.level = level
        self.abilities = abilities or ["Basic Attack"]
        self.upgrades = upgrades or []
        self.rebirths = rebirths
        self.permanent_skoins_boost = permanent_skoins_boost
        self.extra_ability_slots = extra_ability_slots

    def upgrade(self, upgrade_name):
        self.upgrades.append(upgrade_name)
        if upgrade_name == "Double Skoins":
            self.permanent_skoins_boost *= 2
        elif upgrade_name == "Extra Ability Slot":
            self.extra_ability_slots += 1

    def unlock_ability(self, ability):
        max_slots = 3 + self.extra_ability_slots
        if ability not in self.abilities and len(self.abilities) < max_slots:
            self.abilities.append(ability)
            return True
        return False

    def rebirth(self, secret_unlocked=False, secret_character=None, secret_abilities=None):
        self.rebirths += 1
        self.level = 1
        self.permanent_skoins_boost += 1  # Each rebirth increases Skoins earned per question
        if secret_unlocked and secret_character and secret_abilities:
            self.name = secret_character
            self.abilities = secret_abilities

    def to_dict(self):
        return {
            "name": self.name,
            "skoins": self.skoins,
            "level": self.level,
            "abilities": self.abilities,
            "upgrades": self.upgrades,
            "rebirths": self.rebirths,
            "permanent_skoins_boost": self.permanent_skoins_boost,
            "extra_ability_slots": self.extra_ability_slots,
        }
    
    @staticmethod
    def from_dict(data):
        return Character(
            name=data.get("name"),
            skoins=data.get("skoins", 0),
            level=data.get("level", 1),
            abilities=data.get("abilities"),
            upgrades=data.get("upgrades"),
            rebirths=data.get("rebirths", 0),
            permanent_skoins_boost=data.get("permanent_skoins_boost", 1),
            extra_ability_slots=data.get("extra_ability_slots", 0),
        )

# ====== QUESTION ======
class Question:
    def __init__(self):
        self.operators = ['+', '-', '*', '/']
        self.operator = random.choice(self.operators)
        self.a = random.randint(1, 20)
        self.b = random.randint(1, 20)
        self.text, self.answer = self.generate_question()

    def generate_question(self):
        if self.operator == '+':
            return f"{self.a} + {self.b} = ?", self.a + self.b
        elif self.operator == '-':
            return f"{self.a} - {self.b} = ?", self.a - self.b
        elif self.operator == '*':
            return f"{self.a} * {self.b} = ?", self.a * self.b
        elif self.operator == '/':
            b = self.b if self.b != 0 else 1
            return f"{self.a} / {b} = ?", round(self.a / b, 2)

# ====== GAME LOGIC ======
class Game:
    def __init__(self, player_name):
        self.player = Character(player_name)
        self.unlocked_characters = [self.player.name]
        self.available_characters = {
            "Knight": ["Sword Slash", "Shield Block"],
            "Mage": ["Fireball", "Magic Barrier"],
            "Rogue": ["Stealth Attack", "Poison Dart"],
            "Archer": ["Arrow Shot", "Eagle Eye"]
        }
        self.save_file = SAVE_FILE
        self.load_progress()

    def ask_question(self):
        q = Question()
        print(q.text)
        user_ans = input("Your answer: ")
        try:
            if float(user_ans) == q.answer:
                reward = SKOINS_PER_QUESTION * self.player.permanent_skoins_boost
                print(f"Correct! +{reward} Skoins")
                self.player.skoins += reward
            else:
                print(f"Wrong. Correct answer is {q.answer}")
        except ValueError:
            print("Invalid input. Try again.")

    def upgrade_character(self):
        print("Available upgrades:")
        for upgrade, cost in UPGRADE_COSTS.items():
            print(f" - {upgrade}: {cost} Skoins")
        upgrade = input("Which upgrade? ")
        cost = UPGRADE_COSTS.get(upgrade)
        if cost and self.player.skoins >= cost and upgrade not in self.player.upgrades:
            self.player.upgrade(upgrade)
            self.player.skoins -= cost
            print(f"Upgrade applied: {upgrade}")
        elif upgrade in self.player.upgrades:
            print("You already own this upgrade.")
        else:
            print(f"Not enough Skoins (need {cost}, you have {self.player.skoins}).")

    def unlock_character(self):
        if self.player.skoins >= CHARACTER_UNLOCK_COST:
            for char, abilities in self.available_characters.items():
                if char not in self.unlocked_characters:
                    self.unlocked_characters.append(char)
                    self.player.skoins -= CHARACTER_UNLOCK_COST
                    print(f"Unlocked {char} with abilities: {', '.join(abilities)}")
                    break
            else:
                print("All characters unlocked.")
        else:
            print(f"Not enough Skoins to unlock a new character (need {CHARACTER_UNLOCK_COST}, you have {self.player.skoins}).")

    def unlock_ability(self):
        print("Available abilities to unlock:")
        available = []
        for char, abilities in self.available_characters.items():
            for ab in abilities:
                if ab not in self.player.abilities:
                    print(f"- {ab} ({char})")
                    available.append(ab)
        if not available:
            print("No new abilities available.")
            return
        ability = input("Which ability to unlock? ")
        for abilities in self.available_characters.values():
            if ability in abilities:
                if self.player.unlock_ability(ability):
                    print(f"Ability unlocked: {ability}")
                else:
                    print("Ability slot limit reached or ability already owned.")
                return
        print("Ability not found.")

    def battle(self, opponent_name):
        print(f"Battling {opponent_name}...")
        # Simulate battle with random attack rolls based on number of abilities
        player_score = sum([random.randint(1, 6) for _ in self.player.abilities])
        opponent_score = random.randint(3, 18)
        print(f"Your attack roll: {player_score}")
        print(f"{opponent_name}'s attack roll: {opponent_score}")
        if player_score >= opponent_score:
            win_reward = 20 * self.player.permanent_skoins_boost
            print(f"You win! +{win_reward} Skoins and +1 level.")
            self.player.skoins += win_reward
            self.player.level += 1
        else:
            print("You lose! No rewards this time.")

    def check_rebirth(self):
        if self.player.level >= REBIRTH_LEVEL:
            print("You can rebirth! Want to rebirth? (y/n)")
            ans = input().lower()
            if ans == 'y':
                secret_unlocked = self.player.rebirths == 0 # Unlock on first rebirth
                self.player.rebirth(
                    secret_unlocked=secret_unlocked,
                    secret_character=SECRET_CHARACTER if secret_unlocked else None,
                    secret_abilities=SECRET_ABILITIES if secret_unlocked else None
                )
                print("Rebirth complete! You now earn more Skoins per question.")
                if secret_unlocked:
                    print(f"You unlocked the secret character: {SECRET_CHARACTER}!")
            else:
                print("Rebirth cancelled.")
        else:
            print(f"Need to reach level {REBIRTH_LEVEL} to rebirth (currently {self.player.level}).")

    def save_progress(self):
        data = {
            "player": self.player.to_dict(),
            "unlocked_characters": self.unlocked_characters,
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f)
        print("Game progress saved.")

    def load_progress(self):
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                self.player = Character.from_dict(data["player"])
                self.unlocked_characters = data.get("unlocked_characters", [self.player.name])
                print("Game progress loaded.")
        except Exception:
            print("No previous save found. Starting new game.")

    def show_status(self):
        print(f"\nPlayer: {self.player.name} | Level: {self.player.level} | Skoins: {self.player.skoins} | Rebirths: {self.player.rebirths}")
        print(f"Abilities: {', '.join(self.player.abilities + self.player.upgrades)}")
        print(f"Unlocked characters: {', '.join(self.unlocked_characters)}")
        print(f"Skoins boost: x{self.player.permanent_skoins_boost}")

    def main_menu(self):
        while True:
            self.show_status()
            print("-" * 40)
            print("1. Answer an arithmetic question")
            print("2. Upgrade character")
            print("3. Unlock new character")
            print("4. Unlock new ability")
            print("5. Battle another user")
            print("6. Check rebirth")
            print("7. Save progress")
            print("8. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.ask_question()
            elif choice == '2':
                self.upgrade_character()
            elif choice == '3':
                self.unlock_character()
            elif choice == '4':
                self.unlock_ability()
            elif choice == '5':
                opponent = input("Enter opponent name: ")
                self.battle(opponent)
            elif choice == '6':
                self.check_rebirth()
            elif choice == '7':
                self.save_progress()
            elif choice == '8':
                self.save_progress()
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice.")

# ====== MAIN ======
if __name__ == "__main__":
    name = input("Enter your character name: ")
    game = Game(name)
    game.main_menu()