"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    
    
    # Check if inventory is full
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Inventory is full! Maximum capacity is {MAX_INVENTORY_SIZE}")
    
    # Add item to inventory
    character['inventory'].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    
    
    # Check if item exists
    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory")
    
    # Remove item from inventory
    character['inventory'].remove(item_id)
    return True


def has_item(character, item_id):
   
    return item_id in character['inventory']


def count_item(character, item_id):
   
    
    return character['inventory'].count(item_id)


def get_inventory_space_remaining(character):
   
    
    return MAX_INVENTORY_SIZE - len(character['inventory'])


def clear_inventory(character):
    
    
    # Save items before clearing
    removed_items = character['inventory'].copy()
    
    # Clear inventory
    character['inventory'] = []
    
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    
    
   # Check item exists
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # ✅ Check item is consumable type
    item_type = item_data.get('type', '')
    if item_type != 'consumable':
        raise InvalidItemTypeError(
            f"Cannot use '{item_id}': item type is '{item_type}', "
            f"not 'consumable'. Only consumable items can be used."
        )
    
    # Apply effect
    if 'effect' in item_data:
        effect = item_data['effect']
        
        # Parse string format: "stat:value"
        if isinstance(effect, str):
            try:
                stat_name, value_str = effect.split(':')
                value = int(value_str)
                apply_stat_effect(character, stat_name, value)
            except (ValueError, IndexError):
                raise InvalidItemTypeError(f"Invalid effect format: {effect}")
        
        # Parse dict format: {'stat': value}
        elif isinstance(effect, dict):
            for stat_name, value in effect.items():
                apply_stat_effect(character, stat_name, value)
    
    # Remove used item
    character['inventory'].remove(item_id)
    
    return f"Used {item_id}"


def equip_weapon(character, item_id, item_data):
   
    
    # Check item exists
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Check it's a weapon
    if item_data.get('type') != 'weapon':
        raise InvalidItemTypeError(f"'{item_id}' is not a weapon")
    
    # Unequip current weapon if any
    if character.get('equipped_weapon'):
        old_weapon = character['equipped_weapon']
        try:
            unequip_weapon(character)
        except InventoryFullError:
            # Inventory full, can't unequip
            raise InventoryFullError("Cannot unequip: inventory full")
    
    # Remove from inventory
    character['inventory'].remove(item_id)
    
    # Apply weapon bonus
    if 'effect' in item_data:
        effect = item_data['effect']
        
        # Parse effect if it's a string (format: "stat:value")
        if isinstance(effect, str):
            try:
                stat_name, value_str = effect.split(':')
                value = int(value_str)
                character[stat_name] = character.get(stat_name, 0) + value
            except (ValueError, IndexError):
                raise InvalidItemTypeError(f"Invalid effect format: {effect}")
        
        # Or apply if it's a dict
        elif isinstance(effect, dict):
            for stat_name, value in effect.items():
                character[stat_name] = character.get(stat_name, 0) + value
    
    # Set equipped weapon
    character['equipped_weapon'] = item_id
    
    return f"Equipped {item_id}"


def equip_armor(character, item_id, item_data):
    
    
    # Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Check if item type is armor
    if item_data.get('type') != 'armor':
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor")
    
    # Unequip current armor if exists
    if 'equipped_armor' in character and character['equipped_armor'] is not None:
        unequip_armor(character)
    
    # Parse effect and apply
    effect = item_data.get('effect', {})
    if isinstance(effect, dict):
        for stat_name, value in effect.items():
            apply_stat_effect(character, stat_name, value)
    
    # Store equipped armor
    character['equipped_armor'] = item_id
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    return f"Equipped {item_data.get('name', item_id)}!"


def unequip_weapon(character):
   
    
    # Check if weapon is equipped
    if 'equipped_weapon' not in character or character['equipped_weapon'] is None:
        return None
    
    weapon_id = character['equipped_weapon']
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip weapon.")
    
    # We would need weapon_data to remove bonuses, so for now just store the item
    # The calling function should handle removing stat bonuses
    
    # Add weapon back to inventory
    character['inventory'].append(weapon_id)
    
    # Clear equipped weapon
    character['equipped_weapon'] = None
    
    return weapon_id


def unequip_armor(character):
   
    
    # Check if armor is equipped
    if 'equipped_armor' not in character or character['equipped_armor'] is None:
        return None
    
    armor_id = character['equipped_armor']
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot unequip armor.")
    
    # Add armor back to inventory
    character['inventory'].append(armor_id)
    
    # Clear equipped armor
    character['equipped_armor'] = None
    
    return armor_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    
    
    # Get item cost
    cost = item_data.get('cost', 0)
    
    # Check if character has enough gold
    if character['gold'] < cost:
        raise InsufficientResourcesError(
            f"Not enough gold! Need {cost}, have {character['gold']}"
        )
    
    # Check if inventory has space
    if len(character['inventory']) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full! Cannot purchase item.")
    
    # Subtract gold
    character['gold'] -= cost
    
    # Add item to inventory
    add_item_to_inventory(character, item_id)
    
    return True


def sell_item(character, item_id, item_data):
    
    
    # Check if character has the item
    if not has_item(character, item_id):
        raise ItemNotFoundError(f"Item '{item_id}' not in inventory")
    
    # Calculate sell price (half of purchase cost)
    cost = item_data.get('cost', 0)
    sell_price = cost // 2
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Add gold to character
    character['gold'] += sell_price
    
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    
    
    if ':' not in effect_string:
        return None
    
    parts = effect_string.split(':')
    stat_name = parts[0].strip()
    
    try:
        value = int(parts[1].strip())
        return (stat_name, value)
    except (ValueError, IndexError):
        return None


def apply_stat_effect(character, stat_name, value):
   
    
    stat_name = stat_name.lower()
    
    # Apply the stat modification
    if stat_name in character:
        character[stat_name] += value
        
        # Ensure health doesn't exceed max_health
        if stat_name == 'health' and 'max_health' in character:
            character['health'] = min(character['health'], character['max_health'])


def display_inventory(character, item_data_dict): 
    inventory = character.get('inventory', [])
    
    if not inventory:
        print("Inventory is empty!")
        return
    
    print("\n--- Inventory ---")
    print(f"Capacity: {len(inventory)}/{MAX_INVENTORY_SIZE}")
    
    # Count unique items
    item_counts = {}
    for item_id in inventory:
        if item_id not in item_counts:
            item_counts[item_id] = 0
        item_counts[item_id] += 1
    
    # Display items
    for item_id, count in sorted(item_counts.items()):
        item_data = item_data_dict.get(item_id, {})
        item_name = item_data.get('name', item_id)
        item_type = item_data.get('type', 'unknown')
        
        if count > 1:
            print(f"  • {item_name} ({item_type}) x{count}")
        else:
            print(f"  • {item_name} ({item_type})")
    
    # Display equipped items
    print("\n--- Equipment ---")
    if 'equipped_weapon' in character and character['equipped_weapon']:
        weapon_id = character['equipped_weapon']
        weapon_data = item_data_dict.get(weapon_id, {})
        weapon_name = weapon_data.get('name', weapon_id)
        print(f"  Weapon: {weapon_name}")
    else:
        print(f"  Weapon: None")
    
    if 'equipped_armor' in character and character['equipped_armor']:
        armor_id = character['equipped_armor']
        armor_data = item_data_dict.get(armor_id, {})
        armor_name = armor_data.get('name', armor_id)
        print(f"  Armor: {armor_name}")
    else:
        print(f"  Armor: None")
    
    print("-" * 30)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

