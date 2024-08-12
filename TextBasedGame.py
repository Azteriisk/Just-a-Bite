# Alec Brandt

# Creates the rooms and items dictionaries
def setup_game():
    rooms = {
        'The Camp': {'North': 'The Forest', 'description': 'You are at The Camp. There is a path to the North leading to The Forest.', 'items': ['Flashlight', 'Pickaxe', 'Snickers bar']},
        'The Forest': {'South': 'The Camp', 'East': 'The Grand Exchange', 'West': 'The Cave Exterior', 'description': 'You are in The Forest. Paths lead to the East, West, and South.', 'items': ['Shiny Rock']},
        'The Grand Exchange': {'West': 'The Forest', 'description': 'You are at The Grand Exchange. There is a path to the West leading to The Forest.', 'items': ['Hat'], 'people': ['Clerk']},
        'The Cave Exterior': {'East': 'The Forest', 'description': 'You are at the Cave Exterior. There is a ring doorbell on the side of the cave and a bush to the left. Paths lead to the North and East.', 'items': ['A nice looking bush'], 'actions': ['Ring Doorbell']},
        'The Cave Opening': {'South': 'The Cave Exterior', 'North': 'The Cave Architect\'s Crucible', 'East': 'The Cave Silicon Stalactites', 'description': 'You are at the Cave Opening. Paths lead to the North and South. East is blocked by stacks of disk-like shiny rocks with a note that says "Si Die." Die is a scary word. Wanna break them and go in? [Y/N]', 'items': [], 'actions': ['T-pose Robot']},
        'The Cave Silicon Stalactites': {'West': 'The Cave Opening', 'description': 'You are in the Cave of Silicon Stalactites. Path leads to the West.', 'items': []},
        'The Cave Architect\'s Crucible': {'South': 'The Cave Opening', 'description': 'You are in The Architect\'s Crucible. There is a path to the South.', 'items': [], 'people': ['The Architect']},
        'KFC': {'description': 'You have found a hidden autonomous KFC... or CAVE-FC. nice. Congratulations!', 'items': ['40% off 12pc bucket', 'Famous Bowl', 'Chimkin leg']}
    }
    
    items = {
        'Flashlight': 'The Camp',
        'Pickaxe': 'The Camp',
        'Snickers bar': 'The Camp',
        'Shiny Rock': 'The Forest',
        'Hat': 'The Grand Exchange',
        'A nice looking bush': 'The Cave Exterior',
        '40% off 12pc bucket': 'KFC',
        'Famous Bowl': 'KFC',
        'Chimkin leg': 'KFC'
    }
    
    return rooms, items

# Instructions for game start and commands/help command
def show_instructions():
    print("""
    \033[1;31mJust a Bite - The Text-Based Adventure\033[0m
    \033[1;37mYou are very poor and very hungry. Obtain borger... or better :)\033[0m
    -------------------
    \033[1;32mCommands:\033[0m
    - look (to look around)
    - go [direction] (North, South, East, West)
    - get [number] (to get an item by number)
    - inventory (to see your inventory)
    - interact [number] (to interact with items, people, or options in the room)
    - interact i [number] (to interact with items in your inventory)
    - commands or help (to show all commands again)
    - exit (to quit the game)
    """)

# Refreshes and gives the status of current room
def show_status(current_room, inventory, rooms):
    print(rooms[current_room]['description'])
    print("You see:")
    index = 1
    for item in rooms[current_room].get('items', []):
        print(f"{index}. {item}")
        index += 1
    for person in rooms[current_room].get('people', []):
        print(f"{index}. {person}")
        index += 1
    for action in rooms[current_room].get('actions', []):
        print(f"{index}. {action}")
        index += 1
    if current_room == 'The Cave Silicon Stalactites' and 'Master Seed Crystal' in inventory:  # Special check for secret end game (better than burger)
        print("A faint scent of.... fried chicken in the distance?")

# Prints inventory with index for interactions
def show_inventory(inventory):
    print("Inventory:")
    for index, item in enumerate(inventory, start=1):
        print(f"{index}. {item}")

# Moving between rooms and showing feedback to player
def move_between_rooms(current_room, direction, rooms, inventory):
    direction = direction.capitalize()
    if direction in rooms[current_room]:
        current_room = rooms[current_room][direction]
        show_status(current_room, inventory, rooms)
    else:
        print("You can't go that way!")
    return current_room

# Item pickup system and update room
def get_item_by_number(current_room, number, inventory, rooms):
    items_in_room = rooms[current_room].get('items', [])
    if 0 < number <= len(items_in_room):
        item = items_in_room[number - 1]
        # Special if case for
        if item == '40% off 12pc bucket':  # Special condition check for the caveFC experience
            print("Sorry, looks like this is an online-only offer. Looks like there's no exceptions...")
        elif item == 'Ring Doorbell' or item == 'A nice looking bush':
            print(f"You can't get the {item.lower()}.")
        else:
            inventory.append(item)
            rooms[current_room]['items'].remove(item)
            print(f"{item} retrieved!")
            show_status(current_room, inventory, rooms)  # Update room status after getting an item
    else:
        print("Invalid choice!")
    return inventory

# Clerk interaction with flags changing interaction depending on gameplay
def interact_with_clerk(inventory, interacted_with_clerk, learned_about_origin, learned_from_clerk):
    if not interacted_with_clerk:
        if 'Shiny Rock' in inventory:
            print("""
                   Clerk: Welcome to the Gra-.... oh it's you. That "gladly pay for 2 burgers tomorrow trick isn't going to work again.
                   Hold on, is that a pure silicon monocrystal fragment? I'm a bit of a computerphile. Want to learn about it?
                   """)
            while True:
                response = input("[Y/N]: ").strip().upper()
                if response in ["Y", "YES"]:
                    print("""
                           Clerk: Ah yes I knew you looked like you could mod a server... *Learns the ways of computer*
                           """)
                    inventory[inventory.index('Shiny Rock')] = 'Refined Silicon Fragment'
                    learned_from_clerk = True  # Set learned_from_clerk to True
                    return True, learned_from_clerk
                elif response in ["N", "NO"]:
                    print("""
                           Clerk: Actually don't tell people that. I just like computers. It doesn't need to be a -phile kinda thing. Anyway- get some more of that stuff and I'll take you to McD's myself!
                           """)
                    return False, learned_from_clerk
                else:
                    print("Invalid response. Please enter Y or N.")
        elif 'Master Seed Crystal' in inventory:
            print("""
                   Clerk: You found the Master Seed Crystal! Do you want to:
                   1. Sell it and the info of its origin and silicon stash
                   2. Swallow it in hopes that it does something right in front of me
                   """, end="")
            if learned_about_origin:
                print("""3. Conditionally sell it and the info of its origin and silicon stash""")
            while True:
                choice = input("Choose 1, 2, or 3: ").strip()
                if choice == '1':
                    print("""
                                You become rich beyond your wildest dreams, people buy NFTs of your face and want plots on your metaverse, but that did get all sold to Elon Musk and things have just been really annoying since.
                                """)
                    print("Massive W. Legendary Ending.")
                    return True, learned_about_origin
                elif choice == '2':
                    print("""
                                Wow that was really dumb. I'm just going to give you another burger, but you're for real paying me back for BOTH tomorrow.
                                Although the seed's perfect crystalline structure could never be recovered, you did manage to make it another day and with your new found trove of refined silicon, you should never have a problem getting a burger ever again.
                                Massive W. Legendary Ending.
                                """)
                    return True, learned_about_origin
                elif choice == '3' and learned_about_origin:
                    print("""
                                You force them to embed the first created godchip into AI Harambe and to love him as your own-- as the Sears/Skymall weird tech-gorilla thing he was always meant to be and you embrace this dystopian future together.
                                """)
                    print("Massive W. Legendary Ending.")
                    return True, learned_about_origin
                else:
                    print("Invalid choice!")
        else:
            print("Clerk: You don't have anything interesting for me. Come back when you do.")
    elif 'Master Seed Crystal' in inventory:
        print("""
               Clerk: You found the Master Seed Crystal! Do you want to:
               1. Sell it and the info of its origin and silicon stash
               2. Swallow it in hopes that it does something right in front of me
               """, end="")
        if learned_about_origin:
            print("""3. Conditionally sell it and the info of its origin and silicon stash""")
        while True:
            choice = input("Choose 1, 2, or 3: ").strip()
            if choice == '1':
                print("""
                            You become rich beyond your wildest dreams, people buy NFTs of your face and want plots on your metaverse, but that did get all sold to Elon Musk and things have just been really annoying since.
                            """)
                print("Massive W. Legendary Ending.")
                return True, learned_about_origin
            elif choice == '2':
                print("""
                            Wow that was really dumb. I'm just going to give you another burger, but you're for real paying me back for BOTH tomorrow.
                            Although the seed's perfect crystalline structure could never be recovered, you did manage to make it another day and with your new found trove of refined silicon, you should never have a problem getting a burger ever again.
                            Massive W. Legendary Ending.
                            """)
                return True, learned_about_origin
            elif choice == '3' and learned_about_origin:
                print("""
                            You force them to embed the first created godchip into AI Harambe and to love him as your own-- as the Sears/Skymall weird tech-gorilla thing he was always meant to be and you embrace this dystopian future together.
                            """)
                print("Massive W. Legendary Ending.")
                return True, learned_about_origin
            else:
                print("Invalid choice!")
    else:
        print("Clerk: We've already talked. Get some more of that stuff and I'll take you to McD's myself!")
    return interacted_with_clerk, learned_about_origin

# Architect interaction with special flag if you're wearing your *very cool* hat
def interact_with_architect(wearing_hat):
    print("""
    The Architect: I am The Architect. My god processor will soon be complete, and I will take over humanity!
    """)
    if wearing_hat:
        print("The Architect: That hat makes you look silly.")
    
    print("Dialogue Option(s):")
    print("1. Have you finished it yet...?")
    response = input("Choose 1: ").strip()
    if response == '1':
        print("""
               The Architect: *stumbles* uGH uhhh. well... no.
               At least not yet technically-- YOU JUST GIVE ME 1 DAY AND UR DONE!
               """)
        print("""
        You see:
        1. Another terminal with an antenna pointed directly at the user
        2. The Architect, a towering mountain of a bot
        3. An old Sears catalog on the floor nearest you
        """)
        while True:
            choice = input("Choose 1, 2, or 3: ").strip()
            if choice == '1':
                print("""
                You interact with the terminal, but it turns out the angled antenna is a laser that vaporizes you. GAME OVER!
                """)
                return False, False
            elif choice == '2':
                print("""
                You follow The Architect's long tail to an outlet and unplug him. The Architect is defeated!
                """)
                return True, True
            elif choice == '3':
                print("""
                You check the Sears catalog and find an ad for a lifesize AI Harambe clone. The note says:
                "Worst purchase ever: $800 for a hunk of metal that can't move and hates humans as much as any other animal who only ever knew captivity. RIP my wallet and RIP Harambe."
                """)
                break  # Exit the while loop after inspecting the catalog
        
        while True:
            print("""
            You see:
            1. Another terminal with an antenna pointed directly at the user
            2. The Architect, a towering mountain of a bot
            """)
            choice = input("Choose 1 or 2: ").strip()
            if choice == '1':
                print("""
                You interact with the terminal, but it turns out the angled antenna is a laser that vaporizes you. GAME OVER!
                """)
                return False, True
            elif choice == '2':
                print("""
                You proceed to walk past The Architect and follow his tail to an outlet and unplug him. The Architect is defeated!
                Not bad 😎
                """)
                return True, True
            else:
                print("Invalid choice!")
    else:
        print("Invalid choice!")
    return False, False

# T-Pose robot interact with pickaxe condition (there is not a bug related to this don't look ty)
def interact_with_robot(inventory):
    print("""
    The robot is blocking your way in a menacing T-pose position.
    Do you:
    1. Succumb and hope your karma is decent (it's not)
    2. Try to get the robot to question its existence
    """, end="")
    if 'Pickaxe' in inventory:
        print("""3. Throw your pickaxe at the terminal with the antenna nearest them\n""")
    choice = input("Choose 1, 2, or 3: ").strip()
    if choice == '1':
        print("You succumb and are defeated. GAME OVER!")
        return False
    elif choice == '2':
        print("The robot's eyes go dark blue and it collapses.")
        return 'defeated'
    elif choice == '3' and 'Pickaxe' in inventory:
        print("The robot's eyes go dark blue and it collapses.")
        return 'defeated'
    else:
        print("Invalid choice!")
        return False

# Ring Doorbell interaction with condition based on learning from the clerk or not.
def interact_with_ring_doorbell(learned_from_clerk):
    print("""
    You see a ring doorbell on the side of the cave entrance.
    Do you:
    1. Press the doorbell and announce yourself
    """, end="")
    if learned_from_clerk:
        print("2. Use the knowledge from the Clerk to hack it.")
    else:
        print("2. Back away from the doorbell slowly")
    choice = input("Choose 1 or 2: ").strip()
    if choice == '1':
        print("You press the doorbell and announce yourself. The doorbell camera records your presence.")
        return 'announce'
    elif choice == '2' and learned_from_clerk:
        print("You successfully disable the doorbell, avoiding detection.")
        return 'disable'
    elif choice == '2' and not learned_from_clerk:
        print("You back away from the doorbell slowly.")
        return False
    else:
        print("Invalid choice!")
        return False

# Solid Snake bush crawl
def interact_with_bush():
    print("""
    The fluffy bush looks so inviting- you jump into it solid snake style and use it to approach the cave entrance.
    """)
    return 'bush'

# Item interactions with super secret better than burger end game trick
def interact_with_inventory_item(item, inventory, current_room):
    if item == "Flashlight":
        print("Looks like a reliable Flashlight!")
    elif item == "Pickaxe":
        print("A sturdy Pickaxe, useful for mining.")
    elif item == "Snickers bar":
        print("A Snickers bar. You're not you when you're hungry.")
    elif item == "Shiny Rock":
        print("A shiny rock. Pretty cool, but not finger lickin' good. I wonder how much it's worth?")
    elif item == "Refined Silicon Fragment":
        print("A Refined Silicon Fragment. It's quite valuable.")
    elif item == "Hat":
        response = input("A remarkable hat! or at least your mom would say so :) \n put it on, champ [Y/N]: ").strip().upper()
        if response in ["Y", "YES"]:
            print("Hat is permanently bound! Not to worry, it looks *really* cool and I would --not-- lie about that kind of thing.")
            inventory.remove(item)  # Remove hat from inventory
            return True  # Indicate that the hat is being worn
        else:
            print("You decided not to put on the hat.")
    elif item == "Famous Bowl":
        print("You eat the Famous Bowl. It's pretty decent, I guess.")
        inventory.remove(item)  # Remove Famous Bowl from inventory after use
    elif item == "Chimkin leg":
        print("You eat the Chimkin leg. Not bad at all.")
        inventory.remove(item)  # Remove Chimkin leg from inventory after use
    elif item == "Master Seed Crystal":
        if current_room == 'KFC':
            response = input("Use the Master Seed Crystal to upgrade caveFC? [Y/N]: ").strip().upper()
            if response in ["Y", "YES"]:
                print("You become the god of this realm. Infinitely powerful and benevolent. Spreading fried chicken to every corner of the earth like a Japanese Christmas. Massive W. Legendary Ending.")
                return 'win'
            else:
                print("You decided not to use the Master Seed Crystal here.")
        else:
            print("The Master Seed Crystal is of such perfect design and crystalline structure that it is able to rewrite the fabric of reality like it's a python text game or something.")
    return False

# Calling all the setup and stuff sequentially and handling input and some stuff I really just didn't want to break away into another function even tho it may have been a little prettier
def main():
    rooms, items = setup_game()
    inventory = []
    current_room = 'The Camp'
    learned_from_clerk = False
    interacted_with_clerk = False
    learned_about_origin = False
    wearing_hat = False
    defeated_architect = False

    show_instructions()
    show_status(current_room, inventory, rooms)
    
    while True:
        action = input("> ").strip().lower()
        
        if action == 'exit':
            print("Thanks for playing!")
            break
        elif action == 'look':
            show_status(current_room, inventory, rooms)
        elif action == 'commands':
            show_instructions()
        elif action == 'help':
            show_instructions()
        elif action.startswith('go '):
            direction = action[3:]
            if current_room == 'The Cave Exterior' and direction.lower() == 'north':
                print("You can't go that way! Try interacting with something first.")
            elif current_room == 'The Cave Opening' and direction.lower() == 'north':
                if 'T-pose Robot' in rooms[current_room]['actions']:
                    result = interact_with_robot(inventory)
                    if result == 'defeated':
                        rooms[current_room]['actions'].remove('T-pose Robot')
                        current_room = move_between_rooms(current_room, direction, rooms, inventory)
                    else:
                        break
                else:
                    current_room = move_between_rooms(current_room, direction, rooms, inventory)
            elif current_room == 'The Cave Opening' and direction.lower() == 'east':
                print("Large disk-like shiny rocks in stacks block your path. There appears to be a note on it that says \"Si Die.\" Die is a scary word. Wanna break them and go in? [Y/N]")
                response = input("[Y/N]: ").strip().upper()
                if response in ["Y", "YES"]:
                    current_room = 'The Cave Silicon Stalactites'
                    show_status(current_room, inventory, rooms)
                else:
                    print("You decided not to break the shiny rocks.")
            elif current_room == 'The Cave Silicon Stalactites' and direction.lower() == 'north':
                if defeated_architect and 'Flashlight' in inventory and 'Pickaxe' in inventory:
                    current_room = 'KFC'
                    show_status(current_room, inventory, rooms)
                else:
                    print("A faint scent of.... fried chicken in the distance?")
                    print("Do you want to follow the scent? [Y/N]")
                    response = input("[Y/N]: ").strip().upper()
                    if response in ["Y", "YES"]:
                        if 'Flashlight' in inventory and 'Pickaxe' in inventory:
                            print("You use the flashlight to navigate and the pickaxe to break through the silicon. You arrive at the hidden KFC.")
                            current_room = 'KFC'
                            show_status(current_room, inventory, rooms)
                        else:
                            print("You get lost in the dark and perish. GAME OVER!")
                            break
                    else:
                        print("You decide not to follow the scent.")
            elif current_room == 'The Cave Silicon Stalactites' and direction.lower() == 'west':
                current_room = move_between_rooms(current_room, direction, rooms, inventory)
            elif current_room == 'The Cave Architect\'s Crucible' and direction.lower() == 'south':
                current_room = move_between_rooms(current_room, direction, rooms, inventory)
            else:
                current_room = move_between_rooms(current_room, direction, rooms, inventory)
            if current_room == 'KFC' and not defeated_architect:
                print("You can't go to the KFC until you've defeated The Architect and retrieved the Master Seed Crystal.")
                current_room = 'The Cave Silicon Stalactites'
        elif action.startswith('get '):
            try:
                number = int(action[4:])
                inventory = get_item_by_number(current_room, number, inventory, rooms)
            except ValueError:
                print("Please enter a valid number to get an item.")
        elif action == 'inventory':
            show_inventory(inventory)
        elif action.startswith('interact i '):
            try:
                number = int(action[10:])
                if 0 < number <= len(inventory):
                    item = inventory[number - 1]
                    if item == "Hat":
                        wearing_hat = interact_with_inventory_item(item, inventory, current_room)
                    elif item == "Master Seed Crystal":
                        result = interact_with_inventory_item(item, inventory, current_room)
                        if result == 'win':
                            break
                    else:
                        interact_with_inventory_item(item, inventory, current_room)
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number to interact with an inventory item.")
        elif action.startswith('interact '):
            try:
                choice = int(action[9:])
                total_choices = len(rooms[current_room].get('items', [])) + len(rooms[current_room].get('people', [])) + len(rooms[current_room].get('actions', []))
                if total_choices >= choice > 0:
                    if choice <= len(rooms[current_room].get('items', [])):
                        item = rooms[current_room]['items'][choice - 1]
                        if item == 'A nice looking bush':
                            result = interact_with_bush()
                            if result == 'bush':
                                current_room = 'The Cave Opening'
                                show_status(current_room, inventory, rooms)
                        else:
                            print(f"You inspect the {item}.")
                            inventory = get_item_by_number(current_room, choice, inventory, rooms)
                    elif choice <= len(rooms[current_room].get('items', [])) + len(rooms[current_room].get('people', [])):
                        person = rooms[current_room]['people'][choice - len(rooms[current_room].get('items', [])) - 1]
                        if person == 'Clerk':
                            interacted_with_clerk, learned_from_clerk = interact_with_clerk(inventory, interacted_with_clerk, learned_about_origin, learned_from_clerk)
                            if interacted_with_clerk and 'Shiny Rock' in inventory:
                                inventory[inventory.index('Shiny Rock')] = 'Refined Silicon Fragment'
                            if interacted_with_clerk and 'Master Seed Crystal' in inventory:
                                break
                        elif person == 'The Architect':
                            defeated_architect, learned_about_origin = interact_with_architect(wearing_hat)
                            if defeated_architect:
                                rooms[current_room]['people'].remove('The Architect')
                                print("You have defeated The Architect and retrieved the Master Seed Crystal!")
                                inventory.append('Master Seed Crystal')
                        else:
                            print("Clerk: We've already talked. Get some more of that stuff and I'll take you to McD's myself!")
                    else:
                        action = rooms[current_room]['actions'][choice - len(rooms[current_room].get('items', [])) - len(rooms[current_room].get('people', [])) - 1]
                        if action == 'T-pose Robot':
                            result = interact_with_robot(inventory)
                            if result == 'defeated':
                                rooms[current_room]['actions'].remove('T-pose Robot')
                                current_room = move_between_rooms(current_room, 'North', rooms, inventory)
                        elif action == 'Ring Doorbell':
                            result = interact_with_ring_doorbell(learned_from_clerk)
                            if result == 'announce':
                                current_room = 'The Cave Opening'
                                show_status(current_room, inventory, rooms)
                                if not interact_with_robot(inventory):
                                    break
                            elif result == 'disable':
                                current_room = 'The Cave Opening'
                                show_status(current_room, inventory, rooms)
                        else:
                            print("Invalid choice!")
            except ValueError:
                print("Please enter a valid number to interact.")
        else:
            print("Invalid command!")

#bc we like when things just work :)
if __name__ == "__main__":
    main()  #GOGOGOGO
