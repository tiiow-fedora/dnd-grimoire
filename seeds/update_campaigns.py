"""Second pass: fills in the characters that were unreadable on the first import
(Call of the Deep, What the Gods Left Behind, The Weight of the World).
Stop the server first. Refuses to run if the file changed since the first import (rev != 4)
unless --force is given. Usage: python update_campaigns.py [data-file] [--force]"""
import json, os, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
DATA = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "grimoire.json")
S = lambda **kw: [{"k": k.replace("_", " "), "v": str(v)} for k, v in kw.items()]
A = lambda name, text: {"name": name, "text": text.strip()}
R = lambda title, cat, text: {"title": title, "cat": cat, "text": text.strip()}
L = lambda title, cat, text: {"title": title, "cat": cat, "text": text.strip(), "img": "", "done": False}


def cust(name, role="", level="", origin="", hp="", hpMax="", stats=(), abilities=(), notes=""):
    return {"name": name, "role": role, "level": str(level), "origin": origin, "portrait": "", "hp": hp, "hpMax": hpMax,
            "stats": list(stats), "abilities": list(abilities), "notes": notes}


def add_rules(c, rules):
    have = {r["title"] for r in c["rules"]}
    c["rules"] += [r for r in rules if r["title"] not in have]


def add_lore(c, lore):
    have = {r["title"] for r in c["lore"]}
    c["lore"] += [r for r in lore if r["title"] not in have]


d = json.load(open(DATA, encoding="utf-8"))
if d.get("rev") != 4 and "--force" not in sys.argv:
    sys.exit("rev is %s, not 4: the data changed since the first import. Re-run with --force to overwrite anyway." % d.get("rev"))
by = {c["name"]: c for c in d["campaigns"]}

# ---- Call of the Deep
c = by["Call of the Deep"]
c["char"] = cust("Orien Blacktide", "Iron Sting attunement", 1, "Ignition Union (Ganymede, age 21)", hp=16, hpMax=16,
    stats=S(Strength=3, Fortitude=2, Agility=2, Intelligence=3, Willpower=3, Charisma=2, Light_weapons=1, Iron_Sting=11, AC_bonus="+1"),
    abilities=[
        A("Race: Ganymede", "+3 Willpower, +2 Intelligence."),
        A("Curse of the Side Character", "1d10 extra damage, but you can't kill anything."),
        A("Weapon", "1d6 pierce."),
        A("Metal Eruption (3 star)", "Stomp the ground and metal spikes erupt forward. Cost 20% Ether, range 10 ft, damage 2d10, on hit inflict 2 Iron Spikes."),
        A("Needle Barrage (3 star)", "Jump into the air and throw 3 projectiles. Cost 10% Ether, range 5 ft, damage 3d6, on hit inflict 3 Iron Spikes."),
        A("Metal Rampart (3 star)", "Form a pillar from below and ascend with it. Cost 20% Ether, range 1 ft, rises 10 ft."),
    ],
    notes="Sheet note: \"st from lv up 13\" (unclear what it means). Oath is blank. Inventory is blank.\nHP 16 = 10 + (Fortitude 2 x 3).")
add_rules(c, [
    R("Races", "Race", "Capra +3 Int +2 Wil\nKhan +3 Str +2 Agl\nGanymede +3 Wil +2 Int\nGremor +2 Str +3 Fort\nTiran +3 Agl +2 Wil\nCanor +3 Str +2 Cha\nChrysid +3 Cha +2 Agl\nAdret +3 Cha +2 Wil\nVesperian +3 Fort +2 Wil\nCeltor +3 Cha +2 Int\nFelinor +3 Agl +2 Cha\nEtrean +3 Int +2 Agl"),
    R("Curses", "Other", "Curse Of The Blinded One\nCurse Of The Yun'shul\nCurse Of The Voided Sea\nCurse Of Thornes\n(Effects are not posted; Orien has the Curse Of The Side Character.)"),
])

# ---- What the Gods Left Behind
c = by["What the Gods Left Behind"]
c["char"] = cust("Gabe retardatus est", "Cleric of Sereth, merchant", 40, "Shattercoast, about 6 ft", hp=211, hpMax=211,
    stats=S(Strength="18 (+4)", Dexterity="18 (+4)", Constitution="17 (+3)", Intelligence="20 (+5)", Wisdom="18 (+4)", Charisma="22 (+6)",
            Soul_type="The Hollow Soul", Patron="Sereth, the Whispering Coin", Sanity="32 (last logged 2026-06-28)", Gold="1,888 (2026-09-06)", Followers_ppl="500 (2026-09-06)"),
    abilities=[
        A("Sereth's magic", "Alters probability, luck or timing. Manipulates deals, debts and consequences. Transfers harm, fortune or cost from one place to another. Can change his own and others' rolls."),
        A("Merchant", "Gets Charisma +8 for 24 hours (GM ruling, 2026-03-27)."),
        A("Ritual Shortsword", "4d8 necrotic. Once a day you can reroll the weapon's damage and its damage type."),
        A("Ritual Dagger", "Same damage as a normal dagger. Coinflip: win and gain 5 sanity, lose and lose 5."),
        A("Dagger", "1d4 piercing."),
    ],
    notes="Gear logged: dagger, ritual dagger, ritual shortsword, empty scroll (\"be careful\"), fishing rod, music notes, ring device for Sereth that gives whoever you punch a Sereth eye debuff, sigil of Sereth.\nSanity is the spell resource (see the Rules tab for costs). The channel is mostly a running gold / follower ledger.\nThe formula HP at level 40 would be 10 + 3 + 39 x (5 + 3) = 325; the sheet says 211.\nTo do: bring tax to the ward / police station of this town.")
c["coins"]["gp"] = 1888
add_rules(c, [
    R("Soul types", "Class", "Choose one at character creation: The Enduring, The Commanding, The Violent, The Hollow, The Burdened, The Seeking, The Severed."),
    R("Stats and leveling", "Attributes", "Six core stats. Each level gives +1 stat point to any stat.\nBonus is +1 for every 2 points above 10 (12 = +1, 14 = +2, 15 = +2).\nSheet layout: Strength/Force, Dexterity/Agility, Constitution/Resolve, Intelligence/Insight, Wisdom/Perception, Charisma/Presence."),
    R("Hit points", "Health", "HP = 10 + Resolve modifier at level 1; each level up adds 5 + Resolve modifier."),
    R("Spell sanity cost", "Other", "Small spell 5 sanity: minor effects, subtle miracles.\nModerate 10: clear supernatural impact.\nMajor 20: powerful miracles, decisive turning points.\nGreat 35: rare, dramatic acts that reshape events or fate.\nCataclysmic 50+: acts no mortal was meant to perform safely."),
])

# ---- The Weight of the World
c = by["The Weight of the World"]
c["char"] = cust("", "Iron Lieutenant, Clockwork Hand", "", "Industrial sector",
    stats=S(Head_HP=10, Torso_HP=15, Left_Arm_HP=10, Right_Arm_HP=10, Left_Leg_HP=12, Right_Leg_HP=12, Max_AP=4, Start_AP=3,
            Detachment="27 Initiates, 28 Broken, 22 Steelbound, 1 Forge Choir (2026-08-29)", Armor="Longsight Carapace"),
    abilities=[
        A("Target Acquired (2 AP)", "Mark one visible target. You gain +2 Accuracy, allies +1; called shots cost 1 less AP. One marked target at a time."),
        A("Synchronized Fire (3 AP)", "Allies who hear or see you may make a firearm attack or reposition, +1 Accuracy, reduced recoil. Doesn't bypass BPT limits."),
        A("Execution Window (4 AP)", "From a stationary position, next firearm attack ignores armor tier, +3 damage, crits if it takes a limb to 0. Movement reduced next turn."),
        A("Passive: Clockwork Precision", "Ignore the first Accuracy penalty each turn. +1 Accuracy vs marked, stationary or suppressed targets. Reloading costs 1 less AP."),
        A("Passive: Commanding Presence", "Allies within Medium range get +1 Accuracy on coordinated attacks. Once per round an ally may reposition 1 space for free."),
        A("Basilisk Pattern Rail-Receiver", "Anti-material rifle. Damage 9, BPT 1, extreme range, Accuracy +2, 4 rounds, reload is a full action. Armor Negation (ignores 2 tiers on the limb), Structural Fracture below 50% limb HP, Recoil (+1 Strain or lose Minor Action), Target Lock on MARKED targets. Overpressure Shot once a combat: 12 damage, map-wide, ignores armor below Tier 3, +2 Strain. Always reveals your position."),
        A("Longsight Carapace (Tier 2-3)", "Armor Head 2, Torso 5, Arms 4, Legs 4. Tier 3 vs ballistic when braced. Recoil stabilization frame, braced fire (+1 Accuracy and -1 ranged damage if you don't move), damage redirection (once a round -2 damage). Drawbacks: reduced movement, loses bonuses if constantly moving."),
        A("Clockwork Targeting Optic", "+1 Accuracy with ranged attacks. Target Lock 1/combat (minor action): ignore 1 cover penalty and +1 damage on first ranged attack. Rangefinder. In a Clockwork targeting eye: +1 more Accuracy, +1 recoil control, lock lasts 2 rounds."),
        A("Favor of the Grand Mechanist", "Can be cashed in for the support of the whole Clockwork Hand for a short time."),
        A("The Cannibal Within", "Named by the GM in goon3; no description posted."),
    ],
    notes="Character name is not stated anywhere I could read (the sheet is a Google Doc titled \"I was born at a very young age\"). Limb HP values are the server's default template.\nNotes from #info: obsidian int password clearance of a foreman; a cool spot from a data cartridge in area 3.")
c["story"]["backstory"] = ("Growing up in the industrial sector meant living in the shadow of scrap heaps taller than the apartments themselves. While other kids joined gangs or learned to shoot, he spent his time elbow deep in grease and dead tech. By fifteen he was wiring and jailbreaking junked robotics into homemade augments.\n\n"
    "When the Clockwork Hand caught him poaching their proprietary tech they were supposed to kill him. Instead they took one look at his work and offered him a place among them. He accepted without hesitation.\n\n"
    "He lost an eye to an arc flash and replaced it with a targeting optic; the second was modified later, leaving a mismatched stare. His reinforced shoulder was built from his own blueprint to absorb heavy rifle recoil and blunt impacts.\n\n"
    "He rose to Iron Lieutenant and was given his own detachment: seventeen Initiates, twenty-eight Broken and eleven Steelbound as his personal vanguard. To most people in the sprawl augments are tools. To him, flesh is just a rough draft.")
c["story"]["appearance"] = "Mismatched eyes (two targeting optics), reinforced recoil-absorbing shoulder."
add_rules(c, [
    R("Echo costs", "Other", "Basic Skill 5 (max 3 stacks per category). Advanced Skill 15.\nStandard Feat 20 (Lucky, Ghost Step, Iron Will, Executioner). Elite Feat 40 (Bullet Time, Vein Resistant, Corporate Predator).\nVeil abilities: Minor 15, Major 35, Forbidden 60+.\nRituals / pacts: Minor 20, Major 50, Forbidden 100+.\nNo levels; lethal combat."),
    R("The Broken", "Combat", "Disposable shock troops. Armor H1 T3 A2 L2, crude plating -1 ballistic. Improvised Strike dmg 3 (acc -1, 25% minor bleed); Malfunctioning Sidearm dmg 2, BPT 2, acc -2, can jam. Immune to fear, ignores suppression. Failed augment roll at combat start: 1-2 +1 move, 3-4 +1 damage, 5 a random limb takes 1 per round, 6 explodes for 3 when killed. +1 Accuracy when 2+ attack one target."),
    R("Clockwork Hand Initiate", "Combat", "Armor H1 T4 A2 L2. Clockwork Carbine dmg 3, BPT 2, medium range; Industrial Baton dmg 3, acc +1, 25% Staggered. Disciplined Fire (+1 Accuracy if an ally hit the same target), ignores first suppression. Each has a low-grade augment (d6). Lockstep Push 2 AP."),
    R("Steelbound Unit", "Combat", "Armor H2 T6 A4 L4; first ballistic hit each round -1. Burst Rifle dmg 4, BPT 2, acc +1 (suppression if both hit); Calibration Blade dmg 5, Staggered. Lockstep Fire, Tactical Calibration (+1 Accuracy and damage vs the top threat), Reactive Armor (once a round -2 to a limb). Overwatch Grid 2 AP, Calibrated Advance 3 AP, System Failure Protocol once a combat (+2 damage 2 rounds below half HP)."),
])
add_lore(c, [
    L("Service Node 09-B", "Place", "A sealed maintenance room in District 09 that isn't on any current map. Intact municipal terminal, dead security drone, sealed data cartridges, dried black residue on the walls. Last terminal message, 18 years old: \"DO NOT OPEN LOWER ACCESS.\" The Initiates left it closed. Fresh footprints lead past the sealed door.\nSalvage from the district: electronics, industrial batteries, rifle magazines, maintenance kits, hydraulic actuators, a servo-motor assembly, medical kits, a crushed security drone."),
])

d["rev"] += 1
tmp = DATA + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False)
os.replace(tmp, DATA)
print("updated, rev", d["rev"])
