import json, os, re
from googletrans import Translator
from pathlib import Path
#pip install googletrans==4.0.0rc1

input_lang = "en"
output_lang =  "es"

translator = Translator()
errores = []

files_path = [archivo.as_posix() for archivo in Path('./x-Events').glob("**/*.json")]

special_words = ["Harpy 1", "Harpy 2", "Harpy 3", "Slime 1", "Slime 2", "Slime 3", 'Wild Oni Mating', 'Captivation Kiss', 'Amazing Tits', 'Umbral Chain Necklace', 'Making Out', 'Captivating Grind', 'Alluring Dance', 'Tail Suck', 'Ninja Art: Paizuri Whirlpool', 'Paralytic Saliva Swapping', 'Arousero Orb', 'Hellish Invitation', 'Chilling Kiss', "Nicci's Sweet Invitation", 'Wall Pinned Thighjob', 'Jumbo Mint Choco Chip Clarity Cookie', 'Bubbly Slime Submerge', "Aiko's Silky Sex", 'Wild Ride', 'Wild Rune', 'Wind Rune', 'Mika Defeated', 'Tempting Thigh Prison', 'Anal Adverse', 'Already Anal Transition', 'Loss Jump', 'Bubbly Bounce', 'Bondage Net', 'Command Masturbate', 'Thigh Grinding', 'Tantric Thrust', "'Sword' Handling", 'Comforting Thighjob', 'Sleepy Kisses', 'Impish Reverse Spitroast', 'Slimy Insertion', 'Venom Soaked Love', 'Triple Blowjob', 'Feral Slash', 'Harpy Feather', 'Ninja Art: Flash Step', 'Insomnia Potion', 'Infernal Grind', 'Impish Insert', 'Dissolving Gyration', 'Treasure Finder', 'Grasping Claws', 'Ninja Art: Submissive Charm', 'Sweet Valley Vista', 'Harpy Love Song', 'Trisha Defeated', 'Loss scene', 'Mischievous Suction', 'Harpy Double Trouble', "Vili's Curse", 'Nerves Of Steel', 'Silken Assjob', 'Loss Scene', 'Pinning Pounce', 'Perpetua Sex Win', 'Spectral Suction', 'Umbral Heel', 'Manticore Spikes', 'Melting Erosion Kisses', 'Lucky Jelly', "Oni's Lovemaking", 'Indomitable Rune', 'No stance Transition', 'Heated Handjob', "Mimic's Greedy Mating", 'Sleepy Mushroom Insert', "Mika's Anal Capture", 'Bunny Blitz', 'Heart Rune', 'Ravenous Passion', 'Tentacle Tease', 'Teasing Winds', 'Lazy Slime Insert', 'Undulating Full Body Massage', 'No sex start', 'Shimenawa Chime', "Venefica's Desire", 'Push Away', 'Blue Blaze Impulse Drive - SEX', 'Nightshade Slave', 'Feather Job', 'Bag of Gummi Slimes', 'Tittilating Terror', 'Titillating Temptation', 'Nectar Soaking Deepthroat', 'Arcane Master', 'Tail Churn', 'Corroding Depravity Assjob', 'Infernal Milking', 'Ninja Art: Molten Tiger', 'Ninja Art: Oral Assault', 'Hellhounds Hunt', 'ThighLock Transition', 'Melting Point', 'Blazing Gyration', 'Inebriating Affection', 'Helpless Prey Oral Capture', 'Arouse Orb', 'Insightful Schemer', 'Draining Sex', 'Feather Tease', 'Thighgrinding Loss', 'Undeniable Pleasure', 'Run Away', 'Accidental Slime Fuck', 'Blue Slime', 'Stiffening Tonguejob', 'Squishy Kissing Mating Press', 'Bubbly Kissing Submerging', 'Fucked senseless', 'Face Fuck', 'Slumber Spores', 'Mika Event Bind', "Vili's Puff Puff Surprise", 'Blue Oni', 'Umbral Arousaga', 'Delicious Sin', 'Sinister Eye Bangle', 'Obscene Slimy Enchantment', 'Predatory Oral Capture', 'Intoxicating Kisses', 'Tail Fuck', 'Amazing Legs', 'Umbral Bunny Rampage', 'Ninja Art: Tornado Suction', 'Teasing Oni', 'Sex Expert', 'Manticore Pin', "Mika's Seductive Sway", "Vili's Puff Puff Temptation", 'Spectral Double-Team', "Frog's Clenched Pounding", 'Slimy Frog Tongue Capture', 'Tempting Rose', 'Witches Intoxication', 'Wurm Coil', "'Please don't tease my butt.'", 'Enthralling Display', 'Melting Dark Matter Cascade', 'Sense Weakness', 'Occultic Curse Kiss', 'Hellish Prison', 'Harpies Song', 'Anal Penetration', 'Gates of Hell', 'Mind Melting Makeout', 'Forced Thrusting Thighjob', 'Ninja Art: Double Blowjob Kiss', 'Dream Sex', 'Ofuda Rune', 'Breast Knead', 'Miring Pseudopod Surge', 'Enchanting Allure', 'Intoxicating Kiss', "Alraune's Invitation", 'Thigh Squeeze', 'Double Kunoichi loss', 'Gooey Titfuck', 'Greedy Tease', 'One Harpy Scene', 'Golden Marking', 'Witch Hat', 'Binding Braid', 'Umbral Mania', 'Possessively Draining Sex', 'Tranquility Jelly', 'Ninja Art: Grinding Step', 'Grasp Of The Oni', 'Kissing Adverse', 'Sensitivity Spores', 'Charming Barrage', 'Empowered Thrust', 'Titnotizing Drop', 'Blazing Surge', "Venefica's Magical Binding", 'Opulent March', 'Paizuri Inferno', 'Trisha Lost Spar Sex', 'Umbral Kiss', 'Grope Ass', 'Otherworldly Purr', 'Magic Touch', 'Hypnotic Pheromone', 'Umbral Marshmallows', 'Relaxing Bubble Burst', "Oni's Drunken Prize", 'Intimate Lover', 'Calamity Rush', 'Fucked Her into submission', 'Coiling Evil Tide', 'Hellish Pampering', 'Slime Cling', "Vili's Overwhelming Puff Puff Massage", 'Static Rush', 'Specially Maid Spice Mix', 'Lascivious Gooey Temptation', "Aiko's Loving Submission", 'Breast Suffocation', 'Tormenting Oni', 'Syrupy Sweet Kiss', 'Forced Nectar Feeding', 'Glans Blowjob', 'Sleeping Sex Finisher', 'Captured Prey Feast', 'Sex start', 'Aphrodisiac Enduring', 'Ninja Art: Draining Waves', 'Forbidden Tome', 'Mischievous Tighten', 'Charm Wave', 'Ninja Art: Paizuri Burial', 'Slippery Sinful Squeezing', 'Ravenous Blowjob Assault', 'Sensual Draught', 'Umbral Arousa', 'Ninja Art: Blowjob', 'Toxic Matango', 'Enduring Body', 'Camilla Titfuck Loss', 'Ninja Art: Erotic Mist', 'Kyra Defeated Anal', 'Fizzy Kiss', 'Tighten Coils', 'Ninja Art: Seductive Tease', 'Silver Rune', 'Mind Scrambler', 'Golden Mimic', 'Manticore Spike', 'Marshmallowy Love', 'Anal Scene', 'Signed Picture of Vili', 'Slimy Smooch', 'Double Fight Loss.', 'Power Word: Cum', 'Two Harpies', 'Temple Checkpoint Gem', 'Tengu Scene', 'Nibbling Thigh Grind', "Vili's Smothering Puff Puff", 'One Imp Start', 'Squishy Kissy Mating Press', 'Lecherous Spores', "Rosaura's Oral Invitation", 'Playful Tease', 'Mimic Abyss Hold', 'Paizuri Drain', 'Gooey Titfucking', "Vili's Titfuck Temptation", 'Sex Adept', 'Blue Blaze Impulse Drive', 'Ball-Draining Suction Massage', 'Frog Rune', "Feng's Feral Grace", 'Loving Kiss', 'Harpy Double Team', 'Depraved Entangling Temptation', 'Restrained Leg Grind', 'Enthralling Paizuri Enhancement', 'Steady Pacing', 'Alraune Nectar', 'Nibbling Tease', 'Ugli Herb', 'Oni Peach Drop', 'Feng Foot Pump Restraint', 'Vine Restrain', 'Lust Blaze', 'Umbral Rending', "Vili's Enthralling Tittyfuck", 'Luck Rune', 'Cock Ring of Satisfaction', 'Gloves of Skill', 'Hellfire Hat', 'Treasure Chest', 'Iron Will', 'Ghostly Rhythm', 'Enlightenment Rune', 'Anti-Magic Rune', 'Enslaving Embrace', 'Demon Layer', 'Ring of Allure', 'Alraune Nectar Glazed Donut', 'Nectar Grind', 'Honey Trap', 'Captivatingly Corruptive Kiss', 'Ethereal Overstimulation', 'Slimy Thighjob', 'Hellish Lactation', 'Howling Leg Sweep', 'Luxurious Sway', 'Foot Stroke', 'Ninja Art: Pressure Points', 'Fae Moon Rune', 'Cozy Paizuri', 'Charm Spores', 'Playful Grind', 'Sensual Leg Locked Love Making', 'Semen Eater', "Mika's Tail Cuffs", 'Bunny Press', 'Multi Imp Start', 'Hostile Handjob', 'Intoxicating Pheromones', 'Wrist-Locked Thighjob', 'Seductive Touch', 'Swaying Ass', 'Mika Defeated Anal', 'Imp Juice', "Vili's Vexatious Paizuri", 'Sleep Sex', 'Relaxi Appel Jelly', "Oni's Invitation", "Ancilla's Invitation", 'Great Tits', 'Predatory Leap', 'Scalding Taunt', 'Rage of the Arch-Succubus', 'Gildara Orb', 'Pussy Worship', 'Resilience Rune', 'Nectar Laden Vacuum Blowjob', 'Surging Calamity', 'Wurm Tackle', 'Lovers Passion', 'Demonic Determination', 'Passionate Hell', 'Opulent Kiss', 'Paralytic Haze', "Huntress' Pin", 'Intoxicating Embrace', 'Trisha Defeated Blowjob', 'Immobilizing Peck', 'Imperious Captivation', 'Sex lossScene', 'Sweet Scent', 'Minotaur Mating Pin', 'Occultic Caress', 'Stiff Hopping', 'Ninja Art: Sensual Tease', 'Expert Pacing', 'Treasure Chest Golden', "Vili's Vexatious Love Making", "Ancilla's Thigh Trap", 'Stunning Flare', 'Sleepy Sexual Embrace', 'Exotic Spices', 'Make Out', 'Ravenous Tonguejob', 'Fluff Step Counter', 'Agility Amplification', 'Ghostly After-Image', 'Ninja Art: Electric Dragon', 'Imperious Tease', 'Calm Mind', 'Romantic Escape', 'Gilded March', 'Massage Ass', 'Red Slime Blob', 'Tail Stroke', 'Enchanting Kiss', 'Naughty Oral Synergy', 'Witches Sole', 'Tail Pounding', 'Royal Indulgence', "Vili's Playful Tittyfuck", 'Scalding Domination', 'Luxurious Indulgence', 'Deep Fish', 'Sinful Slime Rune', 'Footjob loss', 'Dive Bomb', 'Ninja Art: Breast Defence', 'Titillating Rose', 'Umbral Domination', 'Sinful Perpetual Caress', 'Bond Breaker', 'Misty Kiss', 'Lazy Slime Seduction', 'Sensitizing Lubricant', 'Loss Sex scene', 'Swirly Blowjob Assault', 'Power Belt', 'Gooey Face Grind', 'Loving Purgatory', 'Breast Nuzzle', "Vili's Bewitching Bounce", 'Sex Toy', 'Phantasmal Vili Titfuck', 'Green Scale', 'Ninja Art: Super Erotic Mist', 'Energetic Bounce', 'Impish Encouragement', 'Teasing Seduction', ' ', 'Unbound Rune', 'Ninja Art: Breast Tsunami', 'Enfeebling Curse', 'Restrained Insert', 'Manticore Intimacy', 'Playful Hunt', 'Trisha Defeated Sex', "Manticore's Venom", 'Obscene Blown Kiss', 'Umbral Caress', 'Numb Self', 'Slimy Re-Insertion', 'Spectral Sex', 'Gale Force', 'Escape Artist', 'Worship Ass', 'Bubble Slime', 'Say nothing.', 'Hunting Howl', 'Fashionable Succubus', 'Amazing Ass', 'Salaris Predatory Kiss', "Vili's Mind-Breaking Puff Puff", "Frog's Bouncing Mating", 'Anti-Elly Dark Matter Burst', 'Spiraling Ass Enslavement', 'Addictive Sweetness', 'Thigh Trapped Footjob Loss', 'Fizzing Hip Swing', 'Entrancing Masturbate Command', 'Oni Sake', 'Hellish Temptation', 'Perpetual Paradise Entrapment', 'Total Umbral Lockdown', 'Ninja Art: Sleep Bomb', 'Melting Gooey Mating', 'Ensnaring Shadows', 'Echoing Whispers', 'Voracious Make Out', 'Only the below feilds matter', 'Silken Paizuri', 'Slimy Escape', 'Energy Drainer', 'Ninja Art: Gyration', 'Captivating Hypnotic Spiral', 'Whimsical Bangle', 'Perpetua wins', 'Enfeebling Abyssal Mating', 'Creeping Evil Tide', 'Umbral Sucker', 'Lethargic Bubbles', 'Aphrodisiac Tolerant', 'Spectral Triple Team', 'Imp Pussy Altar', 'Leaping Assault', 'Infernal Embrace', 'Loving Venom Injection', 'Clinging Feral Sex', "Feng's Alternating Thighjob", 'Flicker Rune', 'Lizard Girl', 'BJ loss', 'Paralyzing Blowjob', 'Web Restrain', 'Melty Sweet Temptation', 'Tiny Fungal Lantern', 'Stun Flare', 'White Wolf Jiangshi Fur', 'Sensual Dance', 'Full Body Slime Massage', 'Blown Kisses Erosion', 'Umbral Leash', 'Fizzing Pool Entrapment', 'Cleanse Lust', 'Coils Loss after quest', 'Voracious Oralfice', 'Swirly Blowjob Kisses', 'Anal Piston', 'Immobilizing Oral', "Nicci's Pheromone Cloud", 'Sleepy Temptation', 'Gloves of Passion', 'Smoldering Flaunt', 'Ninja Art: Face Step', 'Infernal Impact', "Frog's Mating Squeeze", 'Slimy Thighjob Pump', 'Face Grind', 'Hellish Heft', 'Overflowing Evil Tide', 'Impish Cock Worship', 'Cunning Gooey Grapple', "Vili's Double Trouble", 'Sensual Lover', 'Captivating Gaze', 'Entrancing Sway', 'Nara Defeated', 'Breast Massage', 'Ninja Art: Ero Mist', 'Berri Cherri Jelly', 'Primordial Ecstasy', 'Opulent Advance', 'Blowjob to sex', 'Greedy Abyssal Mating', 'Haunting Blowjob', "Spider's Embrace", 'Breast Bounce', 'Breast Smother', 'Sensitizing Smooch', 'Harpy Insert', 'Sigil Of Allure', 'Ball-Draining Oral Prison', 'Soft Amber Embrace', 'Trisha Lost Spar BJ', 'Malicious Blown Kiss', 'Silken Paizuri - No Paizuri Intro', 'Ear Tease', 'Oni Mind Breaker', 'Ninja Art: Trampling Step', 'Sex Master', 'Greedy Squeezing Sex', "Succubi's Charm", 'Perverting Entangling Temptation', 'Rising Evil Tide', 'Opportunistic Oral', 'Rough Ride', 'Arousara Orb', 'Tail Fucking', 'Flying Leg Lock Loss', "Rosaura's Titillating Temptation", "Mika's Relentless Mating", 'Scalding Kiss', 'Single Loss scene', 'Thighjob loss', 'Oni Mating Press', 'Succubus Vice', 'Thighjob Loss', 'Pinch Nipples', 'Rapacious Kiss', "Vili's Grinding Titillation", 'Tied to Bed', 'Loving Rose', 'Bubble Bounce', "Demon's Loincloth", 'Forest Kebab', 'Chocolate Marshmallow Temptation', "Tengu's Luminescent Love Making", 'Lust Inferno', 'Pinpoint Pleasure', "Vili's Overflowing Tittyfucking", 'Angry Lizard Girl', 'Slime Engulf', 'Spiraling Breast Obsession', 'Restrained Foot Pump', "Mizuko's Overcharge", 'Nara Defeated Sex', 'Slimy Thigh Capture', 'Warm Jiggly Temptation', 'Ninja Art: Sinking Pressure Paizuri', 'Ninja Art: Hungry Succubi', 'Night Bane', 'Megami Staff', "Vili's Enchanting Tittyfuck", 'Imperious Kiss', 'Nectar Sex', 'Conquering Advance', 'Swirly Kiss Flurry', 'Slimy Prostate Milking', 'Nightshade Stockings', 'Nightshade Smooch', 'Haughty Reversal', 'Stunning Smooch', 'Quick Witted', 'Sensual Gyration', "Vili's Vexing Paizuri", "Nicci's Sweet Love", 'Blaze Impulse', 'Anal Sex Loss - You probably gave up intentionally.', "Vili's Dick-Enslaving Tittyfuck", 'Ninja Art: Sixty Nine Draining', 'Cold Sheltering Paizuri', 'Placebo Pheromone', 'Insatiable Tease', 'Enchanting Jiggle', "Vili's Perfect Puff Puff", 'Ninja Art: Crushing Pressure Paizuri', 'Ghostly Blowjob', 'Nectar Nursing Handjob', 'Harmony Jelly', 'Mesmerizing Jiggle', 'Skilled Tongue', 'Kunoichi Trainee', 'Lizard Girl Thug', 'Elven Kiss', 'Black Knight', 'Magi Boost', 'Righteous Fury', 'Alraune Nectar Item', 'Strange Collar', "'Please do...鈾�'", 'Swirly Kiss Slather', 'Smothering Pawjob', 'Slimed 50%', 'Venom Laced Titfuck', 'Flash Bomb', 'Toxic Temptation', 'Gooey Caress', 'Slimy Kisses', 'Possessive Makeout', "Trisha's Allure", "Dancer's Two Step Seduction", 'Ninja Art: Double Blowjob: Suck and Tease', "Venefica's Love", 'Channeling Thrust', 'Frozen Regalia', 'Twin Oni Rune', 'Sweet Hunger', 'Voracious Tail Sweep', 'Calamity Crown', 'Methodical Pacification', 'Blazing Oni Overcharge', 'Snowstorm Rune', "Frog's Reckless Pounding", 'Succubus Trisha', 'Vacuum Blowjob', 'Wild Mating Pounce', 'Valley Of Fascination', 'Struggle ', 'Perpetual Ruinous Ride', 'Bull Rune', 'Absolute Umbral Territory', 'Nipple Tease', 'Smoldering Seduction', 'Slimy Footjob Massage', 'Box of Assorted Deluxe Chocolates', 'Oblivion Sole', 'Breast Fondle', 'Enduring Draught', 'Disarming Appeal', 'Ninja Art: Eternal Love Kick', 'Oblivion Kiss', 'Energy Potion', 'Semen Frenzy', 'Swirly Tongue Assault', 'Ninja Art: Erotic Mist Kiss', 'Ninja Suit', 'Paralysis Spores', 'Wild Foot Pump', 'Lecherous Kiss', 'Luxury Lotion', 'Enticing Molten Squeeze', 'Sex loss', 'Steel Flash Rune', 'Loss tease scene', 'Intoxicating Affection', 'Destructive Gooey Mating', 'Umbral Mating', 'Blue Slime Blob', 'Enchanting Intoxication', 'Weak Grip', 'Thigh Squeeze Loss', 'Arcane Adept', 'Draining BJ', 'Beguiling Paizuri Enhancement', 'Inferno Pin', "Venefica's Affection", 'Accursed Draining Abyss', 'Oni Scented Sweat 2', 'Oni Scented Sweat 3', 'Contempt of the Arch-Succubus', 'Oni Scented Sweat 1', 'Umbral Connection', 'Kissing Dance', "Aiko's Invitation", 'Slimy Dexterous Footjob', 'Anaph Rune', 'Double Blowjob', 'Sensually Seductive Kiss', 'Temptation Victory', 'Dark Perpetua', 'Gilded Kisses', 'Jumping Assault', 'Yuki-Onna Tears', 'Slimy Pumping Blowjob', 'Salaris Predatory Make Out', 'Bubble Splash', 'Coil Crush', 'Hellish Kiss', 'Erotic Mist', 'Oni Spitroast', 'Cuddly Handjob', 'Already fucking Transition', "Favor's Misfortune", 'Loss MakingOut scene', 'Stylish Jacket', 'Seductive Slime Massage', 'Inebriating Melons', 'Elven Kissing', 'Power Up!', 'Hypnotic Sway', "Nicci's Peppering Petal Pecks", 'Energetic Dance', 'Fluff Step', 'Elf Blew It', 'Arcane Expert', 'Depraved Alluring Languor', 'Lovingly Rough Kiss', 'Twin Hunger', 'Numbing Ride', 'Infernal Compulsion', 'Matango Mushroom', 'Incite Dreams', 'Silken Paizuri - Intro', 'Tail Peg Loss', 'Rough Handjob', 'Wild Hip Check', 'Warming Kisses', 'Foot Grind', 'Hellish Rub', 'Brain Crusher', 'Slimy Sexual Entrapment', 'Rapacious Squeeze', 'Mushroom Temptation', 'Interlocking Abyssal Loving', 'Umbral Lockdown', 'Gentle Thighjob', 'Taming Temptation', "Wurm's Lash", 'Silky Snuggling Kisses', 'Monstrous Expert', 'Okami Gi', 'Cat Rune', 'Wild Inferno', 'Venomous Blast', 'Glans Teasing', 'Instinct Draught', 'Veloci Jelly', "Vili's Dick-Breaking Tittyfuck", 'Giant Shank of Meat', 'Manticore Tail Fuck Offer', 'Nightshade Worship', 'Slimy Titfucking', "Feng's Wild Power", 'Purgatory Pin', 'Minotaur Charge', 'Occultic Embrace', 'Overwhelming Tongue Massage', 'Impish Face Grind', 'Swirly Blowjob Slurp', "Manticore's Sting", 'Soothing Potion', 'Lovers Rune', "Queen's Corruption", 'Deep Kiss', 'Breast Smothering', 'Holy Headpat', 'Lulling Grind', 'Melting Depravity', 'Imp Reverse Spitroast', 'Ethereal Grind', 'Occultic Mating Curse', 'Sex Loss Scene', 'Anaph Herb', 'Ninja Rope Trap', "Vili's Mind Melting Puff Puff", 'Slimy Blowjob Squeeze', 'Otherworldly Suction', 'Serpentine Grind', 'Otherworldly Tonguejob', 'Sensual Pace', 'Nice Legs', 'Flawless Feet', 'Mystic Hat', 'Harpy Egg', "Rosaura's Invitation", 'Tail Prostate Crush', "Nicci's Nectary Makeout", 'Slimy Vacuum Blowjob', 'Scalding Sex', 'Warming Paizuri', 'Umbral Devastation', 'Ninja Art: Love Button Blowjob', 'Cuddly Loss', 'Circlet of Seduction', "Wind's Blessing", 'Smothering Purgatory', 'Amulet of Vitality', 'Nectar Titfuck', 'Temple Loss', 'Bubbling Slime Massage', 'Melty Ripple Ruin Wave', 'Oni Pelvis Breaker', 'Sweet Pheromones', 'Kyra Defeated Sex', 'Footjob Loss', 'Perpetual Obscene Ride', "Frog's Slimy Grind", 'Frenzied Bunny', 'Loss Anal scene', 'Churning Squeeze', 'Skilled Feet', 'Fizzy Green Slime Bubble', 'Passionate Lovemaking', 'Stiff Ride', 'Tit Fucking', "Venefica's Fancy", 'Ethereal Blowjob', 'Drugged Food', 'Leg Grind', 'Luminous Bonds', 'Monstrous Adept', 'Breast Caress', 'Perpetua Lvl 5', 'Blazing Titnosis Vortex', 'Oblivion Press', 'Orgasm Denial.', 'Avaricious Ring', "Mika's Relentless Anal", 'Smooth Rune', 'Inferno Rune', 'Bubbling Gyration', 'Sudden Mattress', 'Tail Peg Loss after quest', 'Harpy Tengu', 'Fucked Her into submission2', 'Obscene Ripple Wave Enchantment', 'Phantasmal Vili', 'Lips of Temptation', 'Normal loss', 'Thigh Trapped Footjob', "Frog's Frenzied Pounding", 'Nibbling Kiss', 'Greedy Kiss', 'Venom Overdosed Titfuck', 'Captive Audience', 'Oni Spitroast Mating', 'Dance Invitation', 'Chained Rune', "Mimic's Grasp", 'Rose Pheromone', 'Skillfully Passionate Kiss', 'Leash of Darkness', 'Erosion Lotion Lathering', 'Fluffy Feather Sex', 'Oblivion Connection', 'Paralytic Lick', 'Stinging Love', 'Ethereal Oral', 'Taming Lockdown', 'Toxic Matango Mushroom', 'Anal Victory', 'Massaging Seduction', 'Tail Pegging', 'Slimy Thighjob Squeeze', 'Thoughtful Schemer', 'Leg Locked Restraint', 'Long Tongued Kiss', "Hero's Cape", 'Occultic Caress ', "Alraune's Temptation", 'Soothing Whisper Sex', 'Arachne Webbing', 'Labyrinth Checkpoint Gem', 'Elven Herb', 'Ravenous Leap', 'Squeeze Ass', 'Sole Seduction', "Nicci's Enticing Invitation", 'Mika Defeated Sex', 'Spider Bite', 'In Chest Loss scene', 'Rune Of Action', 'Sinfully Divine Chocolate Truffle', 'Oblivion Milk', 'Aphrodisiac Resistant', 'Slimy Kiss', 'Umbral Shadow', 'Oblivion Marshmallows', 'Nimble Frog Capture', 'Voltlin Livewire', 'Slimy Cushion', "Vili's Mind-Enslaving Puff Puff", 'Great Ass', 'Deep Rune', 'Infernal Pillows', 'Slimy Frog Footjob', 'Hug of the Drunken Oni', 'Mass Seduction', 'Paralyzingly Long Kiss', 'Accursed Caress', 'Possessive Kissing Caress', 'Sleim Shoppe Slime', 'Stabilizing Phantasm', 'Ninja Art: Bowing the Mountain', 'Melty Sweet Domination', 'Mating Leg Lock', 'Sexual Tempt', "Sofia's Enthralling Embrace", 'Restraining Expert', 'Witches Temptation', 'Ooey Gooey Titfucking', 'No Stance', 'Face Sit', 'Oblivion Vista', 'Imp Binding Magic', 'Oral Temptation', 'Infernal Coaxing', 'Phantasmal Vili PuffPuff', 'Manticore Venom Injection', 'Sleeping Thighjob Finisher', 'Explosive Tackle', 'Draining Gyration', 'Amulet of Tongues', 'Sigil Of Will-Power', 'Umbral Milk', 'Hellish Ride', 'Slimed 100%', 'Group Sensitize', "Vili's Puff Puff Massage", 'Paizuri and Kisses', 'Drunken Breakup', 'Imp Fury', 'Nightshade Embrace', 'Elven Rope Trap', 'Lewd Bottle', 'Ninja Art: Endless Depths', 'Carrying Fuck', 'Camilla Vaginal Sex Loss', 'Urethral Slime Attack', 'Hip Dance', 'Ooey Gooey Love Making', 'Pleasure for Pleasure', 'Sex Adverse', 'Tongue Invasion', 'Unbridled Passion', 'Footjob Loss Scene', 'Slimy Face Sit', 'Cloying Mist', 'Normal loss2', 'Ninja Art: Bouncing Bliss', 'Slimed 75%', 'Slimed 25%', 'Intoxicating Melons', 'Monster Pacing', 'Pressure Titfuck', 'Fengs Wrist Lock', 'Devouring Ride', 'Manticore Tail Fuck', "Vili's Seductive Switch Up", 'Umbral Footpump', 'Livewire Rune', 'Slimy Thigh Lock', 'Kyra Defeated', 'Tail Thrust', 'Slimy Submerging'] #Agregar

def open_file(input_file_name):
	try: 
		with open(input_file_name, 'r', encoding='utf-8') as f:
			return json.load(f)    
	except:
		with open(input_file_name, 'r') as f:
			return json.load(f)

def check_brackets(text):
    # Verificar si el texto contiene corchetes [] o llaves {}
    return True if re.search(r'[\[\]]', text) else False
    
def correct_brackets(text1, text2):
	# Encontrar todas las coincidencias entre corchetes en ambos textos
	content1_list = re.findall(r'\[(.*?)\]', text1)
	content2_list = re.findall(r'\[(.*?)\]', text2)
	
	# Reemplazar cada elemento de text1 con el correspondiente de text2
	for content1, content2 in zip(content1_list, content2_list):
		text1 = text1.replace(f'[{content1}]', f'[{content2}]')
		return text1

def translate_file(data):
	print("init translation")
	for a in range(len(data["EventText"])): #Lista de eventos
		print("Event", a) # dicc Evento individual
		textEvent = data["EventText"][a]["theScene"] # list Texto del evento
		for c in range(len(textEvent)):
			b = str(textEvent[c])
			if " " in b and not(".mp3" in b) and not(".png" in b) and not(".jpeg" in b) and not(".ogg" in b) and not(".jpg" in b) and not(".wav" in b) and not(b in special_words):
				
				if "|f|" in b:
					print("r1")
					partes = b.split('|f|')
					# Lista resultante
					resultado = []
					
					# Procesar cada segmento
					for parte in partes:
					    if parte:
					        resultado.append(parte.split('|n|'))
				
					for t in range(len(resultado)):
						text = resultado[t][1]
						resultado[t][1] = translator.translate(fr"{text}", dest=output_lang).text or b
						
						union  = ["|n|".join(x) for x in resultado]
						traduccion ="|f|" +"|f|".join(union)
						if check_brackets(traduccion):
							traduccion = correct_brackets(traduccion, b)
						print(traduccion,"\n")
						data["EventText"][a]["theScene"][c] = traduccion
				else:		
					print("r2",f"Event: {a} / {len(data['EventText'])}", f"SceneNum: {c} / {len(textEvent)}")
					try:
						traduccion = translator.translate(fr"{b}", dest=output_lang).text or b
						if check_brackets(traduccion):
							traduccion = correct_brackets(traduccion, b)
						print(traduccion,"\n")
						data["EventText"][a]["theScene"][c] = traduccion
					except Exception as err:
						errores.append(["\n",open_file_path,err, f"Event: {a}", f"SceneNum: {c}", str(textEvent[c]),"\n"])
						create_debug(save_file_path, errores)
						print(err)
			
def get_special_wor(data):
	for a in range(len(data["EventText"])): #Lista de eventos
		b = data["EventText"][a]["NameOfScene"]
		if " " in b and len(b)>=2:
			special_words.append(b) # list


def save_file(data, output_file_name):
	with open(output_file_name, 'w') as f:
  	  json.dump(data, f, ensure_ascii=False, indent=4)

def create_debug(save_file_path = "", errores = ""):
	with open('-Errores_debug.txt', 'w', encoding='utf-8') as f:
		f.write(save_file_path + str(errores))

print(files_path)


for file_path in files_path:
	open_file_path = f"./{file_path}"
	save_file_path = f"./ES/{file_path}"
	dirname_save_file = os.path.dirname(save_file_path)
	
	print("file",open_file_path)
	print("save path file,", save_file_path)
	print("save path",dirname_save_file)
	
	try:
		os.makedirs(dirname_save_file, exist_ok=True)
		if os.path.isfile(save_file_path):
			raise Exception("Archivo existente.")
		
		try:
			data = open_file(open_file_path)
			get_special_wor(data)
			translate_file(data)
			special_words = list(set(special_words))
			save_file(data, save_file_path)
		    
		except Exception as e:
		    print(f'\n\nError en el archivo : {open_file_path} ...',e)
		    errores.append(["\n",open_file_path,e,"\n"])
		    save_file(data, save_file_path)
		    create_debug(save_file_path, errores)

	except Exception as err:
		print("error: ",err)
	
	

	  	  
print('Done.\nErrores: \n', errores)