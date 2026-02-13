from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional


INTENT_ICONS = {
    "attack": "⚔",
    "defend": "🛡",
    "buff": "✨",
    "debuff": "☠",
}


CARD_ART = {
    "Strike (Ogun)": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/87/Ogun_shrine%2C_Lagos%2C_Nigeria.jpg",
        "credit": "Wikimedia Commons (CC BY-SA)",
    },
    "Defend (Obatala)": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Yoruba_carved_wooden_figure%2C_British_Museum.jpg",
        "credit": "Wikimedia Commons (CC BY-SA)",
    },
    "Ofunmeji": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f3/Ifa_divination_tray.jpg",
        "credit": "Wikimedia Commons (CC BY-SA)",
    },
    "Osemeji": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Yoruba_ifa_bowl.jpg",
        "credit": "Wikimedia Commons (CC BY-SA)",
    },
    "Curse": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/Yoruba_mask%2C_Nigeria.jpg",
        "credit": "Wikimedia Commons (CC BY-SA)",
    },
}


@dataclass
class Card:
    name: str
    cost: int
    card_type: str
    description: str
    marks: List[str]
    art_url: str = ""
    art_credit: str = ""
    retain: bool = False

    def play(self, game: "Game", target: Optional["Enemy"] = None) -> None:
        if self.name == "Strike (Ogun)":
            if target:
                dmg = 6 + game.player.bonus_attack
                target.take_damage(dmg)
                print(f"You strike {target.name} for {dmg} damage.")
        elif self.name == "Defend (Obatala)":
            block = 5 + game.player.bonus_block
            game.player.block += block
            print(f"You gain {block} Block.")
        elif self.name == "Ofunmeji":
            if target:
                target.take_damage(4 + game.player.bonus_attack)
                print(f"Ofunmeji sears {target.name}.")
        elif self.name == "Osemeji":
            game.player.block += 3 + game.player.bonus_block
            print("Osemeji steadies your spirit: +Block.")


@dataclass
class Enemy:
    name: str
    hp: int
    max_hp: int
    intents: List[str]
    turn: int = 0
    strength: int = 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def intent(self) -> str:
        return self.intents[self.turn % len(self.intents)]

    def take_turn(self, game: "Game") -> None:
        act = self.intent()
        icon = INTENT_ICONS.get(act, "?")
        print(f"{self.name} acts: {icon} {act}")
        if act == "attack":
            dmg = 5 + self.strength
            game.player.take_damage(dmg)
            print(f"{self.name} attacks for {dmg}.")
        elif act == "defend":
            self.hp = min(self.max_hp, self.hp + 3)
            print(f"{self.name} fortifies and recovers 3 HP.")
        elif act == "buff":
            self.strength += 1
            print(f"{self.name} gains +1 Strength.")
        elif act == "debuff":
            game.player.weakened = max(game.player.weakened, 1)
            print(f"{self.name} weakens you.")
        self.turn += 1

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - amount)


@dataclass
class Player:
    hp: int = 60
    max_hp: int = 60
    ase: int = 3
    block: int = 0
    weakened: int = 0
    deck: List[Card] = field(default_factory=list)
    draw_pile: List[Card] = field(default_factory=list)
    discard_pile: List[Card] = field(default_factory=list)
    hand: List[Card] = field(default_factory=list)
    relics: List[str] = field(default_factory=list)
    bonus_attack: int = 0
    bonus_block: int = 0

    def take_damage(self, amount: int) -> None:
        reduced = max(0, amount - self.block)
        self.block = max(0, self.block - amount)
        self.hp = max(0, self.hp - reduced)
        print(f"You take {reduced} damage ({self.hp}/{self.max_hp} HP).")

    def draw(self, n: int = 5) -> None:
        for _ in range(n):
            if not self.draw_pile:
                if not self.discard_pile:
                    break
                self.draw_pile = self.discard_pile[:]
                self.discard_pile.clear()
                random.shuffle(self.draw_pile)
                print("↺ Your discard pile shuffles into the draw pile.")
            self.hand.append(self.draw_pile.pop())


class Game:
    def __init__(self) -> None:
        self.player = Player()
        self.floor = 1
        self.matrix: List[str] = []
        self.seed_deck()

    def seed_deck(self) -> None:
        def make_card(name: str, cost: int, card_type: str, description: str, marks: List[str], retain: bool = False) -> Card:
            art = CARD_ART.get(name, {})
            return Card(
                name,
                cost,
                card_type,
                description,
                marks,
                art_url=art.get("url", ""),
                art_credit=art.get("credit", ""),
                retain=retain,
            )

        base = [
            make_card("Strike (Ogun)", 1, "Attack", "Deal 6 damage.", ["I"]),
            make_card("Strike (Ogun)", 1, "Attack", "Deal 6 damage.", ["I"]),
            make_card("Strike (Ogun)", 1, "Attack", "Deal 6 damage.", ["I"]),
            make_card("Defend (Obatala)", 1, "Skill", "Gain 5 Block.", ["II"]),
            make_card("Defend (Obatala)", 1, "Skill", "Gain 5 Block.", ["II"]),
            make_card("Defend (Obatala)", 1, "Skill", "Gain 5 Block.", ["II"], retain=True),
            make_card("Ofunmeji", 1, "Ifa", "Deal 4 damage.", ["I", "II"]),
            make_card("Osemeji", 1, "Ifa", "Gain 3 Block.", ["II", "I"]),
        ]
        self.player.deck = base

    def print_card_art_sources(self) -> None:
        print("\nCard art sources (license-free/open-license web images):")
        for name, info in CARD_ART.items():
            print(f"- {name}: {info['url']} [{info['credit']}]")

    def start_floor(self) -> None:
        self.player.ase = 3
        self.player.block = 0
        self.player.draw_pile = self.player.deck[:]
        self.player.discard_pile = []
        self.player.hand = []
        random.shuffle(self.player.draw_pile)

    def matrix_append(self, card: Card) -> None:
        for m in card.marks:
            self.matrix.append(m)
        self.matrix = self.matrix[-8:]

    def print_matrix(self) -> None:
        print("Ifá Signature (4x2):")
        bits = self.matrix + ["."] * (8 - len(self.matrix))
        for r in range(4):
            print(f"  {bits[r*2]} {bits[r*2+1]}")

    def combo_check(self, names: List[str], enemies: List[Enemy]) -> None:
        if "Ofunmeji" in names and "Osemeji" in names:
            print("⚡ Addition Mod 2 resolved: Oyekumeji manifests. BOARD WIPE!")
            for e in enemies:
                e.take_damage(12)

    def encounter_for_floor(self) -> List[Enemy]:
        if self.floor == 6:
            return [
                Enemy("Oba A", 22, 22, ["attack", "buff"]),
                Enemy("Oba B", 20, 20, ["defend", "attack"]),
                Enemy("Oba C", 18, 18, ["attack", "debuff"]),
            ]
        if self.floor == 10:
            return [Enemy("Ugbo Marauder", 45, 45, ["attack", "attack", "buff", "debuff"])]
        return [Enemy(f"Spirit Foe F{self.floor}", 20 + self.floor * 2, 20 + self.floor * 2, ["attack", "defend", "buff"])]

    def floor_event(self) -> None:
        if self.floor == 5:
            print("Eshu offers crossroads: 1) Ire (+8 max HP)  2) Osogbo (+2 Attack, add Curse)")
            choice = input("> ").strip()
            if choice == "1":
                self.player.max_hp += 8
                self.player.hp += 8
                print("Ire accepted. Vitality rises.")
            else:
                self.player.bonus_attack += 2
                art = CARD_ART.get("Curse", {})
                self.player.deck.append(
                    Card(
                        "Curse",
                        1,
                        "Curse",
                        "Dead card.",
                        ["II", "II"],
                        art_url=art.get("url", ""),
                        art_credit=art.get("credit", ""),
                    )
                )
                print("Osogbo accepted. Power with burden.")
        elif self.floor == 8:
            print("Ajala Mopin reveals your Ori: 1) Oshun (combo score)  2) Shango (+3 atk, -8 max HP)")
            choice = input("> ").strip()
            if choice == "1":
                self.player.relics.append("Ori of Oshun")
                print("You chose Ori of Oshun.")
            else:
                self.player.relics.append("Ori of Shango")
                self.player.bonus_attack += 3
                self.player.max_hp = max(1, self.player.max_hp - 8)
                self.player.hp = min(self.player.hp, self.player.max_hp)
                print("You chose Ori of Shango.")
        elif self.floor == 9:
            print("Guaranteed treasure: 1) Golden Chain (+1 Àṣẹ/turn) 2) Snail Shell (+2 Block gain)")
            choice = input("> ").strip()
            if choice == "1":
                self.player.relics.append("Golden Chain")
            else:
                self.player.relics.append("Snail Shell of Sand")
                self.player.bonus_block += 2

    def combat(self) -> bool:
        enemies = self.encounter_for_floor()
        print("\nEnemies:")
        for e in enemies:
            print(f"- {e.name} ({e.hp} HP) intent {INTENT_ICONS[e.intent()]} {e.intent()}")

        while self.player.hp > 0 and any(e.is_alive() for e in enemies):
            self.player.block = 0
            self.player.ase = 3 + (1 if "Golden Chain" in self.player.relics else 0)
            self.player.draw(5)
            played_names: List[str] = []

            while True:
                alive = [e for e in enemies if e.is_alive()]
                if not alive:
                    break
                print(f"\nHP {self.player.hp}/{self.player.max_hp} | Àṣẹ {self.player.ase} | Block {self.player.block}")
                self.print_matrix()
                for i, c in enumerate(self.player.hand, start=1):
                    art_hint = " (art)" if c.art_url else ""
                    print(f"{i}. {c.name} [{c.cost}] - {c.description}{art_hint}")
                cmd = input("Play card #, 'art', or 'end': ").strip().lower()
                if cmd == "art":
                    for c in self.player.hand:
                        if c.art_url:
                            print(f"{c.name}: {c.art_url} [{c.art_credit}]")
                    continue
                if cmd == "end":
                    break
                if not cmd.isdigit() or int(cmd) < 1 or int(cmd) > len(self.player.hand):
                    print("Invalid choice.")
                    continue
                card = self.player.hand[int(cmd) - 1]
                if card.cost > self.player.ase:
                    print("Not enough Àṣẹ.")
                    continue
                self.player.ase -= card.cost
                target = alive[0]
                if len(alive) > 1:
                    print("Targets:")
                    for j, e in enumerate(alive, start=1):
                        print(f"{j}. {e.name} ({e.hp} HP)")
                    pick = input("Target #: ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(alive):
                        target = alive[int(pick) - 1]
                card.play(self, target)
                self.matrix_append(card)
                played_names.append(card.name)

                self.player.hand.pop(int(cmd) - 1)
                if card.name != "Curse":
                    self.player.discard_pile.append(card)

            self.combo_check(played_names, enemies)
            for e in [x for x in enemies if x.is_alive()]:
                e.take_turn(self)

            for c in self.player.hand[:]:
                if c.retain:
                    continue
                self.player.discard_pile.append(c)
                self.player.hand.remove(c)

        return self.player.hp > 0

    def tutorial_text(self) -> None:
        lessons: Dict[int, str] = {
            1: "Floor 1 The Descent: Learn basic attack and Àṣẹ use.",
            2: "Floor 2 The Clay Vessel: Block mitigates incoming damage.",
            3: "Floor 3 Eshu's Gaze: Read enemy intents before acting.",
            4: "Floor 4 Binary Signatures: Build the 4x2 Ifá matrix with marks I/II.",
            5: "Floor 5 The Crossroads: Event node choice—blessing or obstruction.",
            6: "Floor 6 Elu Resistance: First elite battle with multiple foes.",
            7: "Floor 7 Addition Mod 2: Combine Ofunmeji + Osemeji for transformation.",
            8: "Floor 8 The Inner Head: Pick an Ori for permanent archetype bonuses.",
            9: "Floor 9 Basket of Existence: Guaranteed treasure relic selection.",
            10: "Floor 10 Rhythmic Cycles: Master discard reshuffle loops.",
        }
        print("\n" + "=" * 72)
        print(lessons[self.floor])
        print("=" * 72)

    def run(self) -> None:
        print("Welcome to Ìrìn Àṣẹ: Descent from Òrún")
        self.print_card_art_sources()
        for f in range(1, 11):
            self.floor = f
            self.tutorial_text()
            self.floor_event()
            self.start_floor()
            won = self.combat()
            if not won:
                print("Your vessel breaks before Ilé-Ifẹ̀. Run ended.")
                return
            print(f"Floor {f} cleared.")
        print("You mastered the first ten floors and reach the gates of Ilé-Ifẹ̀.")


if __name__ == "__main__":
    Game().run()
