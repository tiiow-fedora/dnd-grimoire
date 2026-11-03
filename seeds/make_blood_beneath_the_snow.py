"""Builds seeds/blood-beneath-the-snow-rules.json from the rules the GM posted in the
Blood Beneath the Snow Discord (player category). Re-run after editing."""
import json, os

R = []
def rule(title, cat, text):
    R.append({"title": title, "cat": cat, "text": text.strip()})

rule("Attributes", "Attributes", """
Roll 4d6, drop the lowest die (for each attribute).
Skills: pick 3 and add 2 to them.

Might - strength, physical force, lifting, grappling, powerful attacks.
Agility - speed, reflexes, balance, movement, precision.
Endurance - health, toughness, resisting exhaustion and wounds.
Wits - knowledge, perception, investigation, solving problems.
Will - courage, determination, resisting fear and supernatural influence.
Presence - leadership, intimidation, persuasion, reputation.
""")

rule("Hit Points", "Health", """
HP = 10 + (Endurance x 3) + Class HP

Class HP:
Berserker +12 | Drengr +10 | Huscarl +12 | Raider +8 | Ulfhednar +10
Skald +6 | Galdurman +4 | Seiðr-Witch +4 | Völva +4 | Seiðsmith +6

GM examples: Berserker with Endurance 6 = 10 + 18 + 12 = 40 HP. Galdurman with Endurance 4 = 10 + 12 + 4 = 26 HP.

(App note: "Endurance" in the formula is treated as the Endurance modifier, (score - 10) / 2 rounded down. That is what gives Benjamin's sheet value of 22 HP at Endurance 15.)
""")

rule("Downed and Death", "Health", """
0 HP - Downed: you are unconscious, incapacitated, or otherwise unable to fight.

You can fall below 0 HP.
Death threshold = -(Endurance). Endurance 6 dies at -6 HP.

A character at 0 HP is not necessarily dead, but they are in serious danger.
""")

rule("Armor", "Combat", """
Armor does not make an attack miss. If someone swings an axe at you, they can still hit you. The question is: does the axe reach your flesh?

Armor reduces the damage that gets through.

Damage Taken = Damage Dealt - Armor

Example: a mail shirt gives 3 Armor. An axe hits for 8. 8 - 3 = 5 damage taken.
If an attack deals less damage than the armor provides, the armor absorbs the blow.
""")

rule("Shields", "Combat", """
Armor reduces damage. A shield lets you actively defend yourself.

Shield Block (reaction): reduce incoming damage by a significant amount. The shield takes Wear.

Example: enemy deals 9 damage. Shield Block reduces it by 5. You take 4. Your shield gains 1 Wear.
When the shield reaches its Wear limit, it becomes damaged or breaks.
""")

rule("Weapons", "Combat", """
Damage = damage dealt before armor.
Reach = how far the weapon can effectively attack.
Properties give weapons their identity.

Light - easy to wield and carry.
Heavy - requires significant Strength.
Reach - attacks from farther away.
Thrown - can be thrown effectively.
Piercing - particularly effective against armor.
Hooking - can pull, trip, or manipulate enemies.
Brutal - especially capable of causing Wounds.
Two-Handed - requires both hands.
Shield-Handed - can be used alongside a shield.
""")

rule("Starting Gear", "Gear", """
Simple clothing appropriate to their homeland
Wool cloak
Belt
Boots
Waterskin
Flint & steel
Small bedroll
Simple eating utensils
3 days of rations
Small pouch
10 Silver

(Plus whatever your class and background grant.)
""")

rule("Human", "Race", """
Humans are the most numerous people in the world. They possess no divine blood. No inherited blessing. No ancient power sleeping within their veins.

What they lack in supernatural heritage, they make up for through numbers, ingenuity, skill, and sheer stubbornness. Humans have built kingdoms, founded clans, raised great halls, crossed the seas, and killed things that should have been impossible to kill.
""")

rule("The Tainted", "Race", """
Those whose blood carries the faintest remnants of the gods. Their divine ancestry may be so distant that hundreds of generations separate them from their divine ancestor. Most Tainted never know which god runs through their blood. Some never display anything unusual at all.

Others are born with abilities that should not exist: strength beyond their size, sight others cannot have, surviving wounds that should have killed them. And sometimes something far stranger happens.
""")

rule("The Danger of Being Tainted", "Race", """
The blood of the Tainted is extremely valuable. It can be used as a component in certain forms of magic, ritual, and binding. Because of this, Tainted people are hunted. Some are captured, sold, or experimented upon. Some are turned into Thralls.

A Thrall is a Tainted person whose will has been magically bound to another. They remain alive, may keep their memories and even their personality, but their freedom is no longer entirely their own.

Many Tainted hide what they are.

GM warning: if you are careless, you will die.
""")

BG = [
 ("Noble", "Persuasion & Leadership", ["Noble contacts", "Knowledge of politics and clans", "Family name or inheritance"], "Born into status, wealth, or influence. Whether you still have it is up to you."),
 ("Outcast", "Stealth & Survival", ["Knowledge of hidden places", "Experience living alone", "Someone or something that drove you away"], "You were never meant to belong: exiled, rejected, or simply never accepted."),
 ("Warrior", "Athletics & Intimidation", ["Military training", "Knowledge of weapons and warfare", "A scar, war story, or old enemy"], "You have known blood and battle, for clan, coin, glory, or survival."),
 ("Hunter", "Survival & Perception", ["Tracking", "Hunting and trapping", "Knowledge of animals and the wilderness"], "You know the wilderness better than most people know their own homes."),
 ("Sailor", "Sailing & Perception", ["Knowledge of ships and the sea", "Navigation", "Experience with distant lands"], "The sea is a teacher, a home, and sometimes a grave."),
 ("Skald", "Performance & Persuasion", ["History and lore", "Storytelling", "A reputation, good or bad"], "You carry stories in your heart and words on your tongue."),
 ("Craftsman", "(craft-based)", ["Crafting knowledge", "Knowledge of materials and tools", "A trade", "Connections within your profession"], "Choose a craft: Blacksmith, Woodworker, Leatherworker, Weaponsmith, Shipwright, Weaver, Jeweler, Other."),
 ("Healer", "Medicine & Wisdom", ["Herbs and remedies", "Knowledge of wounds and illness", "Someone whose life you saved"], "You learned how to mend what is broken."),
 ("Scout", "Stealth & Perception", ["Tracking", "Knowledge of terrain", "Ambush and reconnaissance"], "You see what others miss."),
 ("Prisoner", "Endurance & Will", ["Knowledge of prisons and captivity", "Escaping restraints", "A hatred, debt, or unfinished business"], "You have known captivity, and you survived."),
 ("Farmer", "Endurance & Survival", ["Farming", "Knowledge of animals and crops", "Strong connection to a home or community"], "Hard work, patience, and the land. Not glorious, but it kept you alive."),
 ("Trader", "Insight & Persuasion", ["Trading", "Knowledge of markets and goods", "Contacts in distant settlements"], "You know the value of silver, goods, information, and good company."),
 ("Hermit", "Survival & Insight", ["Knowledge of the wilderness", "Knowledge of old traditions", "A personal philosophy, secret, or obsession"], "You left society behind."),
 ("Bystander", "Perception & Insight", ["Knowledge of a major event", "A secret that others don't know", "A reason to become involved"], "You weren't part of the fight, but you were there, and it changed you."),
 ("Thrall", "(not listed)", [], "You were not free. Through blood, magic, debt, or force, your will belonged to another. You escaped, or someone freed you. But freedom comes with a price."),
 ("Monster Hunter", "Survival & Perception", ["Knowledge of monsters", "Tracking supernatural creatures", "Experience fighting something unnatural"], "You have seen what others refuse to believe. You carry: a trophy, scar, or story from your greatest hunt."),
 ("Raider", "Athletics & Intimidation", ["Knowledge of raiding and warfare", "Sailing and boarding", "Experience fighting as part of a warband"], "Take what you can. Leave before the tide turns. You carry: something taken during a raid."),
 ("Exile", "Survival & Will", ["Knowledge of distant lands", "Experience living without a clan", "Someone who wants you returned, or dead"], "Your name was taken from you. You carry: the symbol or token of the home you lost."),
 ("Jarl's Retainer", "Warfare & Insight", ["Knowledge of clans and politics", "Military training", "Contacts among warriors and nobles"], "You served beneath a powerful lord. You carry: a token proving who you once served."),
 ("Runebearer", "Lore & Perception", ["Knowledge of ancient symbols", "Knowledge of old stories and traditions", "Possession of a mysterious rune, relic, or inscription"], "You were entrusted with something you do not fully understand. You carry: a mysterious object whose purpose is unknown."),
]
for name, skills, gains, blurb in BG:
    t = blurb + "\n\nSkills: " + skills
    if gains:
        t += "\nYou gain:\n- " + "\n- ".join(gains)
    rule(name, "Background", t)

CL = [
 ("Berserker - The Bear-Wolf", 12, "A brutal frontline warrior who becomes more dangerous as battle grows more intense.", ["Powerful melee attacks", "Battle-fury", "Enduring wounds", "Intimidating enemies", "Fighting through pain"], "When the shield breaks, the Berserker begins."),
 ("Drengr - The Oathbound", 10, "A versatile warrior whose strength is tied to courage, conviction, and oaths.", ["Strong martial abilities", "Exceptional courage", "Oath-based abilities", "Fighting against overwhelming odds", "Rewards for keeping your word"], "A man's word is heavier than his sword."),
 ("Huscarl - The Shield of the Jarl", 12, "A defensive warrior who protects allies and controls the battlefield.", ["Shield techniques", "Protecting allies", "Counterattacks", "Holding positions", "Battlefield control"], "Let them break their swords upon my shield."),
 ("Raider - The Sea-Wolf", 8, "A mobile and aggressive warrior who excels at taking advantage of openings.", ["Fast attacks", "Mobility", "Ambushes", "Ranged and melee weapons", "Fighting in difficult situations"], "The sea gives nothing freely."),
 ("Ulfhednar - The Wolf Warriors", 10, "A supernatural hunter who combines martial skill with the instincts of a predator.", ["Hunting abilities", "Enhanced senses", "Tracking", "Predatory combat", "Supernatural abilities"], "The wolf does not ask whether the prey is ready."),
 ("Skald - The Voice of the Saga", 6, "A versatile support character who uses words, songs, stories, and reputation.", ["Inspiring allies", "Songs and stories", "Social influence", "Knowledge", "Manipulating morale"], "A man dies twice: once when his heart stops, and once when his name is forgotten."),
 ("Galdurman - The Rune-Learned", 4, "A scholar of words, runes, and symbols; knowledge carved into wood, stone, bone, and flesh.", ["Ancient knowledge", "Runes", "Rituals", "Mysteries", "A great deal of reading"], "A fool sees a mark. A Galdurman wonders who taught the stone to speak."),
 ("Seiðr-Witch - The Fate-Touched", 4, "A mysterious supernatural character whose abilities are tied to forces beyond ordinary understanding.", ["Strange supernatural abilities", "Spirits and omens", "Visions", "Unusual powers", "Things that may not always make sense"], "Some doors are opened. Others were never closed."),
 ("Völva - The Seer", 4, "Reads signs, listens to dreams, watches the ravens, and asks questions about knowledge, omens, spirits, and the unseen.", ["Prophecy", "Divination", "Omens", "Spirits", "Secrets"], "The future has already happened somewhere."),
 ("Seiðsmith - The Forgemaster", 6, "Works with metal, bone, wood, stone, and stranger things, creating objects that ordinary smiths cannot. Uses seiðr to bind supernatural properties into physical objects.", ["Smithing and crafting", "Magical objects, weapons, and armor", "Appraising crafted things"], "Not every warrior carries an ordinary weapon."),
]
for title, hp, play, exp, quote in CL:
    rule(title, "Class", "Class HP: +%d\n\nPlaystyle: %s\n\nYou can expect:\n- %s\n\n\"%s\"" % (hp, play, "\n- ".join(exp), quote))

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blood-beneath-the-snow-rules.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=1)
print(len(R), "rules ->", out)
