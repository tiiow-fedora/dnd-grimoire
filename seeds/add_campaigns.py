"""Adds the Discord-derived campaigns to the live Grimoire data. Stop the server first.
Usage: python add_campaigns.py [data-file]   (skips names that already exist; bumps rev)"""
import json, os, random, string, sys

DATA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "grimoire.json")
uid = lambda: "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
R = lambda title, cat, text: {"title": title, "cat": cat, "text": text.strip()}
S = lambda **kw: [{"k": k.replace("_", " "), "v": str(v)} for k, v in kw.items()]
A = lambda name, text: {"name": name, "text": text.strip()}
L = lambda title, cat, text: {"title": title, "cat": cat, "text": text.strip(), "img": "", "done": False}


def camp(name, system, char=None, story=None, rules=(), lore=(), people=(), notes=()):
    c = {"id": uid(), "name": name, "system": system,
         "story": {"backstory": "", "appearance": "", "traits": "", "ideals": "", "bonds": "", "flaws": "", "goals": "", "gallery": [], **(story or {})},
         "coins": {"cp": 0, "sp": 0, "ep": 0, "gp": 0, "pp": 0},
         "items": [], "notes": list(notes), "people": list(people), "lore": list(lore), "rules": list(rules)}
    c["char"] = char if char is not None else {}
    return c


def cust(name, role="", level="", origin="", hp="", hpMax="", stats=(), abilities=(), notes=""):
    return {"name": name, "role": role, "level": str(level), "origin": origin, "portrait": "", "hp": hp, "hpMax": hpMax,
            "stats": list(stats), "abilities": list(abilities), "notes": notes}


C = []

# ---- Soul Eater
C.append(camp("Soul Eater", "custom",
  cust("Vincent Moretti", "Meister", "", "Age 24",
       stats=S(Strength=10, Weapons_mastery=11, Constitution=13, Soul=17, Agility=18, IQ=14, Charisma=13, Willpower=11),
       notes="Level not filled in on the server sheet. Weapon partner: not recorded (the abilities channel is empty)."),
  rules=[
   R("Stat rolls", "Attributes", "4d6, drop the lowest, for each stat."),
   R("Health", "Health", "HP = 10 + (Fortitude modifier x 3), plus 10 per level except level 1.\nVincent's Constitution 13 = +1 mod, so 13 HP at level 1."),
   R("Meister sheet", "Other", "Name, age, level, Strength, Weapons mastery, Constitution, Soul, Agility, IQ, Charisma, Willpower.\nWeapons mastery rises passively with every level but can be upgraded to rise faster.\nSoul is used to upgrade your abilities."),
   R("Weapon sheet", "Other", "Name, age, level, Sharpness, Durability, Soul, Agility, IQ, Charisma, Willpower.\nSoul is used to upgrade abilities."),
  ]))

# ---- Nitrogen Fan D&D
C.append(camp("Nitrogen Fan (D&D)", "dnd5e", None,
  rules=[
   R("Character overview", "Other", "Name, race, class, subclass, level, background, alignment, age, height, weight, player, art.\nInitiative, speed, AC, proficiency bonus, passive Perception / Investigation / Insight, inspiration.\nCurrent / max / temp HP, hit dice, death saves."),
   R("Races on offer", "Race", "Human, Elf, Dwarf, Halfling, Gnome, Dragonborn, Tiefling, Half-Orc, Half-Elf."),
   R("Classes on offer", "Class", "Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard, Bloodhunter, Artificer."),
   R("Backgrounds", "Background", "What your character did before adventuring: skill and tool proficiencies, languages, equipment, roleplaying suggestions.\nExamples: Soldier, Criminal, Sage, Acolyte, Entertainer, Noble, Folk Hero, Hermit."),
   R("Skills", "Other", "Standard 5e skill list with the usual ability links (Acrobatics DEX ... Survival WIS), plus languages, tool, weapon and armor proficiencies."),
  ]))

# ---- Call of the Deep
C.append(camp("Call of the Deep", "custom",
  cust("Orien Blacktide", notes="Sheet values were not found on the server's stat-sheet channel; fill in from your own copy."),
  rules=[
   R("Character creation", "Attributes", "Start with 10 stat points; your race grants 5 more. Start at level 1. Every 15 points above the base is a level up."),
   R("Health", "Health", "Base HP = 10 + (Fortitude x 3)."),
   R("Sheet layout", "Other", "Name, level, race, age, origin, oath.\nMain stats: Strength, Fortitude, Agility, Intelligence, Willpower, Charisma.\nWeapon stats: Heavy, Medium, Light.\nAttunement stats: Vitality, Erudition, Proficiency, Songchant.\nInventory."),
  ]))

# ---- What the Gods Left Behind
C.append(camp("What the Gods Left Behind", "custom",
  cust("Gabe", hp=211, hpMax=211, notes="HP taken from the 211/211 shown on the server name; the sheet itself was not readable (the linked Google Sheet was blank)."),
  rules=[
   R("Notes from the server", "Other", "Can change his own and others' rolls.\nRing device for Sereth that gives whoever you punch a Sereth eye debuff.\nBring tax to the ward / police station of this town.\n2d12 slashing. 10d10 psychic (GM notes)."),
  ],
  lore=[
   L("The Old Gods", "Gods", "Existed before the world and shaped it. They no longer walk the land; their will shows through signs, omens and ancient rites.\n\nVaelun, the Pale Witness: moon and watching night.\nTharos, the Bound Maker: creation and shaping.\nMorveth, the Final Mercy: destruction and endings.\nNhal'Kael, the Unspoken: nature rarely described; worship forbidden in several lands."),
   L("The New Gods", "Gods", "Once mortal. They still walk the world, or are believed to, and touch mortal affairs directly.\n\nOssuar, Lord of Bones: death's remains, graves.\nCarthyne, the Gilded Crown: rule, law, legitimacy.\nVelkra, the Red Host: war, violence, survival.\nSereth, the Whispering Coin: trade, debt, exchange."),
   L("The Ascendant Wars", "History", "The time mortals learned a human could become a god. Kings, archmages and warriors vied for ascension, drawing on Old Gods, New Gods, heaven or hell. Cities rose and fell; no one truly won."),
   L("Magic", "Magic", "Magic always costs something, and the cost is invisible to most. It is tied to higher powers and cannot be forced.\n\nDivine: prayers and offerings; respected and feared.\nDark / Forbidden: spirits, demons, the dead; fast, effective, rarely safe.\nCelestial: discipline; cold, precise and powerful.\n\nEveryone agrees magic changes the caster."),
   L("Greyfold Realm", "Kingdom", "\"A land that remembers what others forget.\" Cold, misty, stone towns and tall archives. Families keep records; forgetting brings misfortune. Values endurance, diligence, restraint."),
   L("High Writ Dominion", "Kingdom", "\"Order above all else.\" Roads, courts, defined borders; law and precedent rule daily life. Values discipline, civic duty, reliability."),
   L("Shattercoast", "Kingdom", "\"The world is harsh. Adapt, or be lost.\" Jagged cliffs, storm-swept shores, shifting alliances. Values strength, loyalty, adaptability, action."),
  ]))

# ---- The Book Within
C.append(camp("The Book Within", "custom",
  cust("Ryn", "Wrath affinity", "", "The Thumb", hp=30, hpMax=30,
       stats=S(Sanity_Mentality="16 (+3)", Strength_Force="15 (+2)", Dexterity_Agility="13 (+1)", Constitution_Resolve="13 (+1)", Intelligence_Insight="14 (+2)", Charisma_Presence="14 (+2)", SP=30),
       abilities=[A("Thumb Outfit passive: Ammo Support", "Allies who consume ammo get +20% ammo back when they run out (2x per encounter). Ammo bag carries 32 extra bullets (takes a bonus / action page to retrieve)."),
                  A("Thumb Soldato Rifle (Red)", "Rifle 14-20 Pierce. Bayonet 6-14 Slash. Holds 5 bullets; carry 18 plus 32 in the bag; can supply allies. Scorch bullets can inflict burn.")],
       notes="Outfit resistances: Slash 2x Fatal, Pierce 0.8x Endured, Blunt 1x, Red 1x, White 0.8x Endured, Black 1.5x Weak, Pale 2x Fatal.\nHP/SP shown are the level-1 base of 30; level and grade not filled in on the sheet."),
  rules=[
   R("Stats and leveling", "Attributes", "Roll 4d6 drop lowest, six times; one free reroll of a stat below 10.\nLevel up: +1 stat point to any stat.\nBonus is +1 per two points above 10 (12 = +1, 14 = +2). In focused encounters each stat gives a small buff by type."),
   R("HP and SP", "Health", "Start with 30 HP and 30 SP; both rise by 5 per level.\nExample gain: (5 HP + Constitution/Resolve) x level, (5 SP + Sanity/Mentality) x level."),
   R("Light", "Combat", "Everyone starts an encounter with 3 Light (cap rises with grade). Gain 1 Light per turn; from your third turn gain 3 per turn. A critical or heavy attack gives 1 Light."),
   R("Sanity and Posture", "Combat", "Sanity is separate from posture; you can't die from losing it, but at 0 SP you panic (type unknown yet).\nPosture below 0 is mental deterioration. At -45 posture you lose half SP (85% with an EGO) and lose a turn with 2 dice down (Weakening Mentality), then posture resets to 0. Hit -45 again: lose all SP and panic."),
   R("Focused vs unfocused", "Combat", "Focused: draw pages from a deck and clash with a speed value.\nUnfocused: freeform, use modifiers and describe the action.\nWeapon = damage dice; dice count = how many times you roll it."),
   R("Emotion level", "Combat", "Gained by winning clashes, killing 4 enemies, and at the start of turn 3 then every 2 turns.\nFocused: Lv1 EGOs, Lv2 draw 2 extra pages, Lv3 draw 3 extra and higher speed.\nUnfocused: Lv1 EGOs, Lv2 sanity shield, Lv3 +1 die."),
   R("Pages and chapters", "Combat", "Pages = number of attacks / defenses. Chapters = the skill a page set belongs to. Light pays for pages. Action pages are defensive / support moves that cost 1-2 slots.\nChapter format: name, type (Attack/Action), dice count, page amount, damage type, slot cost (actions). Power and Light cost are set by the GM."),
   R("Damage types", "Combat", "Red: physical. White: mental / SP. Black: both, equal to HP and SP. Pale: soul damage, 2 bursts (percentage plus flat), bypasses defenses and shields. Fixed damage is true damage.\nOutfits give resistances but always carry a weakness."),
   R("Status effects", "Combat", "Stagger: all defenses fatal (2x) except colour, lose turn. Forced Stagger: weak (1.5x), lose turn.\nDice Power Up +1 to total. Final Power Up +1 if no dice lost. Base Power Up +1 base. Value Up +1 to all dice. Shield: extra HP, fixed damage reduction."),
   R("Sin affinities", "Class", "Pick one: Wrath, Lust, Sloth, Gluttony, Gloom, Pride, Envy. It decides your panic type and can affect pages, deck and dice rolls."),
   R("Table rules", "Other", "1: No ALEPH / WAW EGO at the start; ZAIYAN / TETH guaranteed.\n2: Can't be born in A, B, C or X Wings unless negotiated.\n6: Born in a wing, you may join ONE syndicate / office and it must be your story focus.\n7: Count your Light and have fun."),
  ]))

# ---- Elden Ring / Born to Die
lv = [400, 800, 1200, 1600, 2000, 2500, 3000, 3500, 4200, 5000, 5800, 6600, 7500, 8500, 9500, 11000, 12500, 14000, 16000,
      18500, 21000, 23500, 26000, 28500, 31000, 33500, 36000, 38500, 41000, 44000]
C.append(camp("Elden Ring: Born to Die", "custom",
  cust("Ferravix", "Duelist", 17, "Alabaster Lord", hp=30, hpMax=30,
       stats=S(Vigor=10, Mind=9, Endurance=10, Strength="13 (+1)", Dexterity=7, Intelligence=10, Faith=7, Arcane=10, Stamina=50, Speed="30 ft (20 ft in armor)"),
       abilities=[A("Stone Flesh", "Resistance to slashing damage."),
                  A("Gravity Adept", "Gravitic Pull cantrip (pull a creature 5 ft, Str save DC 8+Int+prof). At 5th level Gravity Well once per long rest."),
                  A("Duelist: Chain-Fighter's Reach / Momentum Swing / Arena Bloodlust", "Heavy weapon reach +5 ft once a turn. Once per rest, a hit lets you attack a second creature. Killing with melee gives temp HP = Str mod + level."),
                  A("Duelist: Brutal Reputation", "Advantage on Intimidation in combat. Duel Challenge (bonus action, 1/rest): Wis save or frightened."),
                  A("Alabaster Gravity Hook", "Fixed to armor, can't be disarmed. 2d10+STR piercing, reach 10 ft, chain throw 30 ft, pulls targets 10 ft. Meteor Slam recharge 5-6: 15 ft radius, DEX save, 4d10 bludgeoning + 2d6 force."),
                  A("Gravitational Pull / Rock Sling / Gravity Well", "Pull 10 ft (FP 8, DC 13); three rocks 2d6 each (FP 12); 4d10 force well (FP 18, DC 15)."),
                  A("Blades of Stone", "FP 18, AP 2, 60 ft, 10 ft radius: DEX save, 4d8 piercing + 2d6 force and prone; area becomes difficult terrain.")],
       notes="Alabaster Duelist armor: slashing 4, piercing 4, bludgeoning 5, fire 1, cold 2, lightning 1, holy 2, arcane 4; -10 ft speed; no crits from non-magical weapons.\nSheet HP 30 matches the formula 10 + 2 x Vigor 10."),
  story={"backstory": "Born from a meteor, the first thing you saw was the night sky. You taught your meteor-brothers to use gravity. After a Great War of the gods you were enslaved by the Golden Order and forced to fight as a heretic. You escaped, and you are an enemy of the Golden Order. You seek the Elden Ring: to return to the stars, reunite with your brothers, or take ultimate power."},
  rules=[
   R("Point buy", "Attributes", "All stats start at 5. Distribute 15 extra points. No stat above 10 at level 1 before racial or origin bonuses.\nStats: Vigor, Mind, Endurance, Strength, Dexterity, Intelligence, Faith, Arcane."),
   R("HP / FP / Stamina", "Health", "HP = 10 + (Vigor x 2)\nFP = 10 + (Mind x 3)\nStamina = 10 + (Endurance x 4)"),
   R("Damage types", "Combat", "Slashing, Piercing, Bludgeoning, Fire, Cold, Lightning, Holy, Arcane."),
   R("Rune cost per level", "Other", "\n".join("%d -> %d: %s" % (i + 1, i + 2, format(v, ",")) for i, v in enumerate(lv)) + "\n(Table continues to level 60 on the server.)"),
   R("Messmerfire Grease", "Gear", "Weapon coating, 1 action, 3 rounds. +1d8 fire, +1d4 burn next turn, no healing until end of target's next turn. Same target hit twice: CON save or 2d6 fire and -2 AC.\nDrawstring version: bonus action, 1 round, +2d8 fire, burn 1d6, 3d6 on a double hit."),
   R("Races doc", "Race", "The server links a Google Doc of races (Demi-Humans, Living Jars, etc.) that could not be read."),
  ],
  lore=[
   L("Redmane Castle", "Place", "Stronghold of General Radahn and the Redmanes in Caelid. After the Radahn / Malenia battle the knights stayed to hold back the Scarlet Rot with fire and walls of flame."),
   L("Commander Gaius", "Person", "Gravity sorcery user and friendly rival of Radahn in their youth; Blades of Stone is the product of that rivalry."),
  ]))

# ---- The Weight of the World
C.append(camp("The Weight of the World", "custom",
  cust("", "Iron Lieutenant, Clockwork Hand", "", "Industrial sector",
       stats=S(Head_HP=10, Torso_HP=15, Left_Arm_HP=10, Right_Arm_HP=10, Left_Leg_HP=12, Right_Leg_HP=12, Max_AP=4, Start_AP=3, Corruption="0-10"),
       abilities=[A("Target Acquired (2 AP)", "Mark one visible target. You gain +2 Accuracy, allies +1; called shots cost 1 less AP. One marked target at a time."),
                  A("Synchronized Fire (3 AP)", "Allies who hear or see you may make a firearm attack or reposition, +1 Accuracy, reduced recoil. Doesn't bypass BPT limits."),
                  A("Execution Window (4 AP)", "From a stationary position, next firearm attack ignores armor tier, +3 damage, crits if it takes a limb to 0. Movement reduced next turn."),
                  A("Basilisk Pattern Rail-Receiver", "Damage 9, BPT 1, extreme range, Accuracy +2, 4 rounds. Ignores 2 armor tiers on the limb. Fracture below 50% limb HP. Overpressure shot once a combat: 12 damage, map-wide, ignores armor below Tier 3.")],
       notes="Name not found: the character sheet channel is a Google Doc link. Limb HP values are the server's default template, not confirmed for this character. Backstory from the doc preview: grew up in the industrial sector among scrap heaps, rewiring junked robotics. Notes in the info channel: obsidian int password clearance of a foreman; a cool spot from a data cartridge in area 3."),
  rules=[
   R("Body parts and limb loss", "Health", "Each body part has its own HP. At 0 the part is disabled; damage of 2x its max HP in one attack removes it (replace with an augment or regeneration).\nDefaults: Head 10, Torso 15, Arms 10 each, Legs 12 each.\nArm lost: can't attack with it. Leg: movement halved or none. Head at 0: instantly incapacitated. Torso: major threat."),
   R("Armor", "Combat", "Armor tier 1-4 blocks calibers up to its tier completely. A higher caliber damages armor first; leftover spills to the body part. Armor has durability and must be repaired.\nMelee: blunt reduces armor slightly; piercing may treat armor as 1 tier lower."),
   R("Action points", "Combat", "Max AP 4, start combat with 3. Guns cost no AP; melee and defensive actions do."),
   R("The Vein and Corruption", "Other", "Corruption 0-10, rises with each Vein ability; spend a turn to cleanse.\n0-2 stable. 3-4 -1 Accuracy. 5-6 +1 Power Die, -2 defense. 7-8 +2 Power Dice, 1d6 self-damage per turn. 9 lose control one turn. 10 become an Echo-Wraith.\nPower Die: d6 (0-2), d8 (3-5), d10 (6-8), d12 (9-10, unstable)."),
   R("Echoes", "Other", "Earned from meaningful choices. Spend on Mastery (skills, techniques), Augmentation (install / upgrade augments) or Resonance (Vein powers).\nTypes: Common, Refined, Pure, Fractured."),
   R("Classes", "Class", "Negotiator (support), Marksman (ranged / sniper), The Big Brother (melee frontliner), The Wanderer (Vein specialist), The Infiltrator (stealth), The Desperado (close-quarters gunfighter)."),
   R("Starting equipment", "Gear", "One primary: Snub Nose Revolver (1d6, 6 rounds), Light Pistol (1d8, 8 rounds) or Machete / Short Sword (1d8, 1 AP, bleed).\nArmor: Leather Jacket + Padded Vest (10 HP/piece), Cloth Coat (8), or Chainmail Vest + Leather Pads (12).\nTwo tools: Medkit (+5 limb HP), Repair Kit (+5 armor), Grapple Hook, Smoke Grenade."),
  ],
  lore=[L("Clockwork Hand hierarchy", "Faction", "Grand Mechanist (leader) > Cog Council (5-7 high command) > Iron Lieutenants (field commanders) > Gearwardens (veteran specialists) > Steelbound (core soldiers) > Initiates > The Broken (failed members used as labor, fodder, test subjects, drones).\nThe Forge Choirs are machine priests and engineers running augmentation rituals, maintenance and production.")]))

# ---- Jujutsu Kaisen Experimental
C.append(camp("Jujutsu Kaisen Experimental", "custom",
  cust("Ryuma Kuro", "Grade 4 sorcerer", 7, "Asian / white", hp=72, hpMax=72,
       stats=S(Age=21, Strength=10, Agility=12, Fortitude=18, Willpower=14, IQ=18, Charisma=12, Domain="N/A", Debt="3,210,100 Yen (last note)", Yen=360),
       abilities=[A("Cursed technique: Crystalline manipulation", "The player channel also lists the technique as Supreme Monopoly."),
                  A("Cursed energy reinforcement (-4)", "Bonus action. Reduce damage taken by your Constitution modifier (not soul damage); base melee dice become 1d8 instead of 1d6; add Strength modifier to successful melee hits.")],
       notes="Level 6 on the sheet, then \"+1 level\" posted 2026-07-08, so 7. Formula HP at level 7 would be 10 + 4x3 + 60 = 82; sheet says 72.\nRunes: burn contact evil spirit. 5x8x5 cage.\nInventory: bandage wraps, disinfectant, 3 gauze pads, 4 bandages."),
  rules=[
   R("Stats", "Attributes", "4d6 drop the lowest. Fields: Strength, Agility, Fortitude, Willpower, IQ, Charisma, cursed technique, grade (grade 4 until told otherwise), domain expansion (N/A until told)."),
   R("Health", "Health", "HP = 10 + (Fortitude modifier x 3), plus 10 per level except level 1."),
  ],
  lore=[L("Timeline", "History", "Dec 2025: Geto survived the Night of a Thousand Curses and is the top threat; those aligned with him are arrested or executed.\nMar 2026: the Shibuya arc was prevented; Mahito fell; Sukuna gained 4 minutes 22 seconds.\nApr 2026: Satoru Gojo has been sealed.")]))

# ---- Dn
C.append(camp("Dn", "custom", cust(""),
  rules=[R("Server status", "Other", "The Dn server has no rules posted. The character channels are empty and the news channel is DM-only.")]))

d = json.load(open(DATA, encoding="utf-8"))
have = {c["name"] for c in d["campaigns"]}
new = [c for c in C if c["name"] not in have]
d["campaigns"] += new
d["rev"] = int(d.get("rev", 0)) + 1
tmp = DATA + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
os.replace(tmp, DATA)
print("added", [c["name"] for c in new], "rev", d["rev"])
