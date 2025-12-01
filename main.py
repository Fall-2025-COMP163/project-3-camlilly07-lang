"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    
    
    print("\n" + "=" * 50)
    print("MAIN MENU")
    print("=" * 50)
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    print("=" * 50)
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number (1-3).")


def new_game():
    
    global current_character
    
   
    
    print("\n" + "=" * 50)
    print("CREATE NEW CHARACTER")
    print("=" * 50)
    
    # Get character name
    name = input("Enter your character name: ").strip()
    if not name:
        print("Invalid name. Using 'Hero'.")
        name = "Hero"
    
    # Display class options
    print("\nAvailable classes:")
    print("1. Warrior (HP=120, STR=15, MAG=5)")
    print("2. Mage (HP=80, STR=8, MAG=20)")
    print("3. Rogue (HP=90, STR=12, MAG=10)")
    print("4. Cleric (HP=100, STR=10, MAG=15)")
    
    class_map = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue', '4': 'Cleric'}
    
    while True:
        choice = input("\nSelect class (1-4): ").strip()
        if choice in class_map:
            character_class = class_map[choice]
            break
        else:
            print("Invalid choice. Please select 1-4.")
    
    # Create character
    try:
        current_character = character_manager.create_character(name, character_class)
        print(f"\n✓ Created {name} the {character_class}!")
        
        # Save character
        character_manager.save_character(current_character)
        print(f"✓ Character saved!")
        
        # Start game loop
        game_loop()
    
    except InvalidCharacterClassError as e:
        print(f"✗ Error: {e}")


def load_game():
    
    global current_character
    
    
    
    print("\n" + "=" * 50)
    print("LOAD GAME")
    print("=" * 50)
    
    # Get saved characters
    saved_chars = character_manager.list_saved_characters()
    
    if not saved_chars:
        print("No saved characters found.")
        return
    
    # Display saved characters
    print("\nSaved characters:")
    for i, char_name in enumerate(saved_chars, 1):
        print(f"{i}. {char_name}")
    
    # Get player choice
    while True:
        try:
            choice = int(input(f"\nSelect character (1-{len(saved_chars)}): "))
            if 1 <= choice <= len(saved_chars):
                selected_char = saved_chars[choice - 1]
                break
            else:
                print(f"Invalid choice. Please select 1-{len(saved_chars)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Load character
    try:
        current_character = character_manager.load_character(selected_char)
        print(f"\n✓ Loaded {current_character['name']}!")
        
        # Start game loop
        game_loop()
    
    except CharacterNotFoundError as e:
        print(f"✗ Character not found: {e}")
    except SaveFileCorruptedError as e:
        print(f"✗ Save file corrupted: {e}")
    except InvalidSaveDataError as e:
        print(f"✗ Invalid save data: {e}")


# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
     
    while game_running:
        if current_character['health'] <= 0:
            handle_character_death()
            if not game_running:
                break
            continue
        
        choice = game_menu()
        
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("\n✓ Game saved!")
            game_running = False
        else:
            print("Invalid choice.")
        
        # Auto-save after each action (except quit)
        if choice != 6 and game_running:
            save_game()


def game_menu():
    

    
    
    print("\n" + "=" * 50)
    print(f"GAME MENU - {current_character['name']}")
    print("=" * 50)
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    print("=" * 50)
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter 1-6.")
        except ValueError:
            print("Invalid input. Please enter a number (1-6).")


# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    
    global current_character
    
   
    
    char = current_character
    
    print("\n" + "=" * 50)
    print("CHARACTER STATS")
    print("=" * 50)
    print(f"Name: {char['name']}")
    print(f"Class: {char['class']}")
    print(f"Level: {char['level']}")
    print(f"\nHealth: {char['health']}/{char['max_health']}")
    print(f"Strength: {char['strength']}")
    print(f"Magic: {char['magic']}")
    print(f"\nExperience: {char['experience']}")
    print(f"Gold: {char['gold']}")
    print(f"\nActive Quests: {len(char.get('active_quests', []))}")
    print(f"Completed Quests: {len(char.get('completed_quests', []))}")
    print("=" * 50)


def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    
    
    while True:
        print("\n" + "=" * 50)
        print("INVENTORY MENU")
        print("=" * 50)
        
        # Display inventory
        inventory_system.display_inventory(current_character, all_items)
        
        # Show options
        print("\n1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Unequip Weapon")
        print("5. Unequip Armor")
        print("6. Drop Item")
        print("7. Back")
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 1:
                # Use item
                item_id = input("Enter item ID to use: ").strip()
                if item_id in all_items:
                    try:
                        message = inventory_system.use_item(
                            current_character, item_id, all_items[item_id]
                        )
                        print(f"✓ {message}")
                    except (ItemNotFoundError, InvalidItemTypeError) as e:
                        print(f"✗ {e}")
                else:
                    print(f"Item '{item_id}' not found.")
            
            elif choice == 2:
                # Equip weapon
                item_id = input("Enter weapon ID to equip: ").strip()
                if item_id in all_items:
                    try:
                        message = inventory_system.equip_weapon(
                            current_character, item_id, all_items[item_id]
                        )
                        print(f"✓ {message}")
                    except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
                        print(f"✗ {e}")
                else:
                    print(f"Item '{item_id}' not found.")
            
            elif choice == 3:
                # Equip armor
                item_id = input("Enter armor ID to equip: ").strip()
                if item_id in all_items:
                    try:
                        message = inventory_system.equip_armor(
                            current_character, item_id, all_items[item_id]
                        )
                        print(f"✓ {message}")
                    except (ItemNotFoundError, InvalidItemTypeError, InventoryFullError) as e:
                        print(f"✗ {e}")
                else:
                    print(f"Item '{item_id}' not found.")
            
            elif choice == 4:
                # Unequip weapon
                try:
                    weapon_id = inventory_system.unequip_weapon(current_character)
                    if weapon_id:
                        print(f"✓ Unequipped weapon")
                    else:
                        print("No weapon equipped.")
                except InventoryFullError as e:
                    print(f"✗ {e}")
            
            elif choice == 5:
                # Unequip armor
                try:
                    armor_id = inventory_system.unequip_armor(current_character)
                    if armor_id:
                        print(f"✓ Unequipped armor")
                    else:
                        print("No armor equipped.")
                except InventoryFullError as e:
                    print(f"✗ {e}")
            
            elif choice == 6:
                # Drop item
                item_id = input("Enter item ID to drop: ").strip()
                try:
                    inventory_system.remove_item_from_inventory(current_character, item_id)
                    print(f"✓ Dropped {item_id}")
                except ItemNotFoundError as e:
                    print(f"✗ {e}")
            
            elif choice == 7:
                break
            
            else:
                print("Invalid choice.")
        
        except ValueError:
            print("Invalid input.")


def quest_menu():
    
    global current_character, all_quests
    
    while True:
        print("\n" + "=" * 50)
        print("QUEST MENU")
        print("=" * 50)
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest")
        print("7. Back")
        print("=" * 50)
        
        try:
            choice = int(input("\nEnter your choice (1-7): "))
            
            if choice == 1:
                # View active quests
                active = quest_handler.get_active_quests(current_character, all_quests)
                if active:
                    print("\nActive Quests:")
                    quest_handler.display_quest_list(active)
                else:
                    print("\nNo active quests.")
            
            elif choice == 2:
                # View available quests
                print("\nAvailable Quests:")
                available = quest_handler.get_available_quests(current_character, all_quests)
                quest_handler.display_quest_list(available)
            
            elif choice == 3:
                # View completed quests
                completed = quest_handler.get_completed_quests(current_character, all_quests)
                if completed:
                    print("\nCompleted Quests:")
                    quest_handler.display_quest_list(completed)
                else:
                    print("\nNo completed quests.")
            
            elif choice == 4:
                # Accept quest
                quest_id = input("\nEnter quest ID to accept: ").strip()
                try:
                    quest_handler.accept_quest(current_character, quest_id, all_quests)
                    print(f"✓ Accepted quest: {all_quests[quest_id]['title']}")
                except (QuestNotFoundError, InsufficientLevelError, 
                        QuestRequirementsNotMetError, QuestAlreadyCompletedError) as e:
                    print(f"✗ {e}")
            
            elif choice == 5:
                # Abandon quest
                quest_id = input("\nEnter quest ID to abandon: ").strip()
                try:
                    quest_handler.abandon_quest(current_character, quest_id)
                    print(f"✓ Abandoned quest")
                except QuestNotActiveError as e:
                    print(f"✗ {e}")
            
            elif choice == 6:
                # Complete quest
                quest_id = input("\nEnter quest ID to complete: ").strip()
                try:
                    result = quest_handler.complete_quest(current_character, quest_id, all_quests)
                    print(f"✓ Completed: {result['quest_title']}")
                    print(f"  Rewards: {result['xp_reward']} XP, {result['gold_reward']} Gold")
                except QuestNotActiveError as e:
                    print(f"✗ {e}")
            
            elif choice == 7:
                break
            
            else:
                print("Invalid choice.")
        
        except ValueError:
            print("Invalid input.")


def explore():
    
    global current_character
    
    print("\n" + "=" * 50)
    print("EXPLORING...")
    print("=" * 50)
    
    # Get random enemy for character level
    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    print(f"\nYou encountered a {enemy['name']}!")
    
    # Start battle
    try:
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()
        
        if result['winner'] == 'player':
            # Award XP and gold
            xp_gained = result['xp_gained']
            gold_gained = result['gold_gained']
            
            current_character['gold'] += gold_gained
            character_manager.gain_experience(current_character, xp_gained)
            
            print(f"\n✓ Victory!")
            print(f"  XP Gained: {xp_gained}")
            print(f"  Gold Gained: {gold_gained}")
            print(f"  New Level: {current_character['level']}")
        else:
            # Character died
            print(f"\n✗ You were defeated!")
            current_character['health'] = 0
    
    except CharacterDeadError as e:
        print(f"✗ {e}")


def shop():
    
    global current_character, all_items
    
    
    
    while True:
        print("\n" + "=" * 50)
        print("SHOP")
        print("=" * 50)
        print(f"Your Gold: {current_character['gold']}")
        print("\nShop Items:")
        for item_id, item in all_items.items():
            print(f"  {item_id}: {item['name']} - {item['cost']} Gold ({item['type']})")
        
        print("\n1. Buy Item")
        print("2. Sell Item")
        print("3. Back")
        print("=" * 50)
        
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            
            if choice == 1:
                # Buy item
                item_id = input("\nEnter item ID to buy: ").strip()
                if item_id in all_items:
                    try:
                        inventory_system.purchase_item(
                            current_character, item_id, all_items[item_id]
                        )
                        print(f"✓ Purchased {all_items[item_id]['name']}!")
                    except (InsufficientResourcesError, InventoryFullError) as e:
                        print(f"✗ {e}")
                else:
                    print(f"Item '{item_id}' not found.")
            
            elif choice == 2:
                # Sell item
                item_id = input("\nEnter item ID to sell: ").strip()
                if item_id in all_items:
                    try:
                        gold_received = inventory_system.sell_item(
                            current_character, item_id, all_items[item_id]
                        )
                        print(f"✓ Sold {all_items[item_id]['name']} for {gold_received} Gold!")
                    except ItemNotFoundError as e:
                        print(f"✗ {e}")
                else:
                    print(f"Item '{item_id}' not found.")
            
            elif choice == 3:
                break
            
            else:
                print("Invalid choice.")
        
        except ValueError:
            print("Invalid input.")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
   
    global current_character
    
   
    
    try:
        character_manager.save_character(current_character)
    except Exception as e:
        print(f"Warning: Could not save game: {e}")


def load_game_data():
    
    global all_quests, all_items
    
    
    
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Game data files not found. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except (InvalidDataFormatError, CorruptedDataError) as e:
        print(f"Error loading game data: {e}")
        raise


def handle_character_death():
   
    global current_character, game_running
    
    
    
    print("\n" + "=" * 50)
    print("YOU HAVE DIED!")
    print("=" * 50)
    print(f"\nOptions:")
    print(f"1. Revive (Costs 50 Gold)")
    print(f"2. Quit to Main Menu")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-2): "))
            
            if choice == 1:
                # Revive
                if current_character['gold'] >= 50:
                    current_character['gold'] -= 50
                    character_manager.revive_character(current_character)
                    print(f"✓ Revived! Gold spent: 50")
                    break
                else:
                    print(f"✗ Not enough gold! (Need 50, have {current_character['gold']})")
            
            elif choice == 2:
                # Quit
                game_running = False
                break
            
            else:
                print("Invalid choice.")
        
        except ValueError:
            print("Invalid input.")


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("✓ Game data loaded successfully!\n")
    except (MissingDataFileError, InvalidDataFormatError, CorruptedDataError) as e:
        print(f"✗ Error loading game data: {e}")
        print("Please check your data files and try again.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
