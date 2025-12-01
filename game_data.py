"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
   
    # Check if file exists
    if not os.path.exists(filename):
        #raises custom exception if file not found
        raise MissingDataFileError(f"Quest file not found: {filename}")
    
    # Try to read the file
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        #raises corrupted data error if file cannot be read
        raise CorruptedDataError(f"Could not read quest file: {e}")
    
    # Parse quests separates them by blank lines)
    quests = {}
    quest_blocks = content.strip().split('\n\n')
    
    try:
        for block in quest_blocks:
            if not block.strip():
                continue
            
            # Parse this quest block
            lines = block.strip().split('\n')

            #reads lines and converts them into a quest dictionary
            quest = parse_quest_block(lines)
            
            # Validate the quest
            validate_quest_data(quest)
            
            # Stores each quest by its quest_id
            quests[quest['quest_id']] = quest
    
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error parsing quest data: {e}")
    
    return quests


def load_items(filename="data/items.txt"):
  
    # Check if file exists
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")
    
    # Try to read the file
    try:
        with open(filename, 'r') as file:
            content = file.read()
    except Exception as e:
        raise CorruptedDataError(f"Could not read item file: {e}")
    
    # Parse items (separated by blank lines)
    items = {}
    item_blocks = content.strip().split('\n\n')
    
    try:
        for block in item_blocks:
            if not block.strip():
                continue
            
            # Parse this item block
            lines = block.strip().split('\n')
            item = parse_item_block(lines)
            
            # Validate the item
            validate_item_data(item)
            
            # Store by item_id
            items[item['item_id']] = item
    
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error parsing item data: {e}")
    
    return items


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(quest_dict):
    
    required_fields = {
        'quest_id': str,
        'title': str,
        'description': str,
        'reward_xp': int,
        'reward_gold': int,
        'required_level': int,
        'prerequisite': str
    }
    
    #Ai used to help with for loop structure and isinstance checks
    # Check each required field
    for field, field_type in required_fields.items():
        # Check if field exists
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
        # Check field type
        if not isinstance(quest_dict[field], field_type):
            raise InvalidDataFormatError(
                f"Invalid type for field '{field}': expected {field_type.__name__}, "
                f"got {type(quest_dict[field]).__name__}"
            )
    
    return True


def validate_item_data(item_dict):
    
    required_fields = {
        'item_id': str,
        'name': str,
        'type': str,
        'effect': (str, dict),  # Accept both string and dict formats
        'cost': int,
        'description': str
    }
    
    # Check each required field
    for field, field_type in required_fields.items():
        # Check if field exists
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: {field}")
        
        # Check field type
        # Handle tuple of types (allows multiple types)
        #Ai used to help with isinstance checks for multiple types and error message formatting
        if isinstance(field_type, tuple):
            if not isinstance(item_dict[field], field_type):
                type_names = " or ".join(t.__name__ for t in field_type)
                raise InvalidDataFormatError(
                    f"Invalid type for field '{field}': expected {type_names}, "
                    f"got {type(item_dict[field]).__name__}"
                )
        else:
            if not isinstance(item_dict[field], field_type):
                raise InvalidDataFormatError(
                    f"Invalid type for field '{field}': expected {field_type.__name__}, "
                    f"got {type(item_dict[field]).__name__}"
                )
    
    # Validate item type
    valid_item_types = ['weapon', 'armor', 'consumable']
    if item_dict['type'] not in valid_item_types:
        raise InvalidDataFormatError(
            f"Invalid item type: {item_dict['type']}. "
            f"Must be one of: {', '.join(valid_item_types)}"
        )
    
    return True


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    
    quest = {}
    
    try:
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for colon separator
            if ':' not in line:
                raise InvalidDataFormatError(f"Malformed line in quest data: {line}")
            
            # Split on colon and strip whitespace
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Parse different field types
            if key == 'quest_id':
                quest['quest_id'] = value
            elif key == 'title':
                quest['title'] = value
            elif key == 'description':
                quest['description'] = value
            elif key == 'reward_xp':
                quest['reward_xp'] = int(value)
            elif key == 'reward_gold':
                quest['reward_gold'] = int(value)
            elif key == 'required_level':
                quest['required_level'] = int(value)
            elif key == 'prerequisite':
                quest['prerequisite'] = value
            else:
                raise InvalidDataFormatError(f"Unknown field in quest: {key}")
    
    except ValueError as e:
        raise InvalidDataFormatError(f"Could not convert value to correct type: {e}")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")
    
    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    item = {}
    
    try:
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for colon separator
            if ':' not in line:
                raise InvalidDataFormatError(f"Malformed line in item data: {line}")
            
            # Split on colon and strip whitespace
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Parse different field types
            if key == 'item_id':
                item['item_id'] = value
            elif key == 'name':
                item['name'] = value
            elif key == 'type':
                item['type'] = value.lower()
            elif key == 'effect':
                # Keep effect as STRING format for now
                # This allows both "stat:value" and conversion to dict later
                item['effect'] = value
            elif key == 'cost':
                item['cost'] = int(value)
            elif key == 'description':
                item['description'] = value
            else:
                raise InvalidDataFormatError(f"Unknown field in item: {key}")
    
    except ValueError as e:
        raise InvalidDataFormatError(f"Could not convert value to correct type: {e}")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")
    
    return item


def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # Create data directory if needed
    if not os.path.exists("data"):
        try:
            os.makedirs("data")
        except Exception as e:
            print(f"Warning: Could not create data directory: {e}")
    
    # Create default quests file
    quests_file = "data/quests.txt"
    if not os.path.exists(quests_file):
        try:
            default_quests = """QUEST_ID: defeat_goblin
TITLE: Defeat the Goblin
DESCRIPTION: A goblin has been causing trouble in the nearby forest. Defeat it!
REWARD_XP: 50
REWARD_GOLD: 25
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: slay_orc
TITLE: Slay the Orc
DESCRIPTION: A powerful orc has been terrorizing the village. Defeat it to save the people!
REWARD_XP: 150
REWARD_GOLD: 75
REQUIRED_LEVEL: 3
PREREQUISITE: defeat_goblin

QUEST_ID: defeat_dragon
TITLE: Defeat the Dragon
DESCRIPTION: The mighty dragon must be stopped before it destroys everything!
REWARD_XP: 500
REWARD_GOLD: 250
REQUIRED_LEVEL: 6
PREREQUISITE: slay_orc"""
            
            with open(quests_file, 'w') as f:
                f.write(default_quests)
            print(f"✓ Created default quests file: {quests_file}")
        except Exception as e:
            print(f"Warning: Could not create default quests file: {e}")
    
    # Create default items file
    items_file = "data/items.txt"
    if not os.path.exists(items_file):
        try:
            default_items = """ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 50
DESCRIPTION: A basic iron sword. Good for beginners.

ITEM_ID: steel_armor
NAME: Steel Armor
TYPE: armor
EFFECT: defense:3
COST: 100
DESCRIPTION: Protective steel armor. Reduces incoming damage.

ITEM_ID: health_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:50
COST: 25
DESCRIPTION: Restores 50 health points when used.

ITEM_ID: ancient_bow
NAME: Ancient Bow
TYPE: weapon
EFFECT: strength:8
COST: 150
DESCRIPTION: A legendary bow carved from ancient wood.

ITEM_ID: dragon_scale_armor
NAME: Dragon Scale Armor
TYPE: armor
EFFECT: defense:8
COST: 300
DESCRIPTION: Forged from real dragon scales. Extremely protective."""
            
            with open(items_file, 'w') as f:
                f.write(default_items)
            print(f"✓ Created default items file: {items_file}")
        except Exception as e:
            print(f"Warning: Could not create default items file: {e}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

