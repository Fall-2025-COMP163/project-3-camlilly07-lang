"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    
    valid_classes = {"Warrior", "Mage", "Rogue", "Cleric"}
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    
    # Set base stats based on class
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    elif character_class == "Cleric":
        health = 100
        strength = 10
        magic = 15
    
    # Create and return character dictionary
    character = {
        'name': name,
        'class': character_class,
        'level': 1,
        'health': health,
        'max_health': health,
        'strength': strength,
        'magic': magic,
        'experience': 0,
        'gold': 100,
        'inventory': [],
        'active_quests': [],
        'completed_quests': []
    }
    return character


def save_character(character, save_directory="data/save_games"):
    
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Construct the filename
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")
    
    try:
        with open(filename, 'w') as file:
            # Write each character field to the file
            file.write(f"NAME: {character['name']}\n")
            file.write(f"CLASS: {character['class']}\n")
            file.write(f"LEVEL: {character['level']}\n")
            file.write(f"HEALTH: {character['health']}\n")
            file.write(f"MAX_HEALTH: {character['max_health']}\n")
            file.write(f"STRENGTH: {character['strength']}\n")
            file.write(f"MAGIC: {character['magic']}\n")
            file.write(f"EXPERIENCE: {character['experience']}\n")
            file.write(f"GOLD: {character['gold']}\n")
            
            # Convert lists to comma-separated strings
            inventory_str = ','.join(character['inventory'])
            file.write(f"INVENTORY: {inventory_str}\n")
            
            active_quests_str = ','.join(character['active_quests'])
            file.write(f"ACTIVE_QUESTS: {active_quests_str}\n")
            
            completed_quests_str = ','.join(character['completed_quests'])
            file.write(f"COMPLETED_QUESTS: {completed_quests_str}\n")
        
        return True
    
    except (PermissionError, IOError) as e:
        raise e


def load_character(character_name, save_directory="data/save_games"):
    # Construct the filename
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    
    # Check if file exists
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    # Try to read the file
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(f"Could not read save file for '{character_name}': {e}")
    
    # Parse the file
    character = {}
    try:
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for colon separator
            if ":" not in line:
                raise InvalidSaveDataError(f"Malformed line in save file: {line}")
            
            # Split on colon and strip whitespace
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            
            # Parse different field types
            if key in {"NAME", "CLASS"}:
                character[key.lower()] = value
            elif key in {"LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"}:
                character[key.lower()] = int(value)
            elif key in {"INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"}:
                # Handle empty lists properly
                if value == "" or value is None:
                    character[key.lower()] = []
                else:
                    # Split on comma and filter out empty strings
                    items = [item.strip() for item in value.split(',') if item.strip()]
                    character[key.lower()] = items
            else:
                raise InvalidSaveDataError(f"Unexpected key '{key}' in save file.")
        
        # Validate loaded character data
        validate_character_data(character)
        return character
    
    except InvalidSaveDataError:
        raise
    except Exception as e:
        raise InvalidSaveDataError(f"Invalid save data for '{character_name}': {e}")


def list_saved_characters(save_directory="data/save_games"):
  
    if not os.path.exists(save_directory):
        return []
    
    # Get all saved character names
    character_names = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            # Remove the '_save.txt' extension (9 characters)
            character_name = filename[:-9]
            character_names.append(character_name)
    
    return character_names


def delete_character(character_name, save_directory="data/save_games"):
  
    
    # Construct the filename
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    
    # Check if file exists
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character '{character_name}' not found.")
    
    # Delete the file
    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
   
    # Check if character is dead
    if character['health'] <= 0:
        raise CharacterDeadError("Cannot gain experience: character is dead.")
    
    # Add experience
    character['experience'] += xp_amount
    
    # Check for level ups (can level up multiple times)
    while character['experience'] >= character['level'] * 100:
        # Subtract XP needed for this level
        character['experience'] -= character['level'] * 100
        
        # Increase level
        character['level'] += 1
        
        # Increase max health
        character['max_health'] += 10
        
        # Increase stats
        character['strength'] += 2
        character['magic'] += 2
        
        # Restore health to max
        character['health'] = character['max_health']
    
    return character


def add_gold(character, amount):
   
    # Check if result would be negative
    if character['gold'] + amount < 0:
        raise ValueError("Not enough gold.")
    
    # Add the gold
    character['gold'] += amount
    return character['gold']


def heal_character(character, amount):

    # Check if already at max health
    if character['health'] >= character['max_health']:
        return 0
    
    # Calculate actual healing amount
    actual_heal = min(amount, character['max_health'] - character['health'])
    
    # Apply healing
    character['health'] += actual_heal
    return actual_heal


def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    
    return character['health'] <= 0


def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    
    # Check if character is not dead and returns false is true
    if character['health'] > 0:
        return False
    
    # Revive with 50% health
    character['health'] = character['max_health'] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
   
    required_fields = {
        'name': str,
        'class': str,
        'level': int,
        'health': int,
        'max_health': int,
        'strength': int,
        'magic': int,
        'experience': int,
        'gold': int,
        'inventory': list,
        'active_quests': list,
        'completed_quests': list
    }
    
    # Check each required field
    for field, field_type in required_fields.items():
        # Check if field exists
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
        
        # Check field type
        if not isinstance(character[field], field_type):
            raise InvalidSaveDataError(
                f"Invalid type for field '{field}': expected {field_type.__name__}, "
                f"got {type(character[field]).__name__}"
            )
    
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
         char = create_character("TestHero", "Warrior")
         print(f"Created: {char['name']} the {char['class']}")
         print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
         print(f"Invalid class: {e}")
    
    # Test saving
    try:
         save_character(char)
         print("Character saved successfully")
    except Exception as e:
         print(f"Save error: {e}")
    
    # Test loading
    try:
         loaded = load_character("TestHero")
         print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
         print("Character not found")
    except SaveFileCorruptedError:
         print("Save file corrupted")

