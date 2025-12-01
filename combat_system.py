"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================
#random can now be used in this file
import random
def create_enemy(enemy_type):
  
    #
    enemy_type = enemy_type.lower()
    
    if enemy_type == "goblin":
        return {
            'name': 'Goblin',
            'type': 'goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type == "orc":
        return {
            'name': 'Orc',
            'type': 'orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type == "dragon":
        return {
            'name': 'Dragon',
            'type': 'dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")


def get_random_enemy_for_level(character_level):
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        self.character = character.copy()  # Use copy to not modify original
        self.enemy = enemy.copy()
        self.combat_active = True
        self.turn_count = 0
        self.battle_log = []
    
    def start_battle(self):
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is dead and cannot fight!")
        
        # Display battle start
        display_battle_log(f"⚔️ Battle started: {self.character['name']} vs {self.enemy['name']}!")
        
        # Battle loop
        while self.combat_active:
            # Display current stats
            display_combat_stats(self.character, self.enemy)
            
            # Player turn
            self.player_turn()
            
            # Check if enemy is dead
            result = self.check_battle_end()
            if result == 'player':
                display_battle_log(f"✓ Victory! {self.enemy['name']} has been defeated!")
                rewards = get_victory_rewards(self.enemy)
                return {
                    'winner': 'player',
                    'xp_gained': rewards['xp'],
                    'gold_gained': rewards['gold']
                }
            
            # Enemy turn (if still alive)
            if self.combat_active and self.enemy['health'] > 0:
                self.enemy_turn()
                
                # Check if character is dead
                result = self.check_battle_end()
                if result == 'enemy':
                    display_battle_log(f"✗ Defeat! You have been defeated by {self.enemy['name']}!")
                    return {
                        'winner': 'enemy',
                        'xp_gained': 0,
                        'gold_gained': 0
                    }
            
            self.turn_count += 1
    
    def player_turn(self):
        
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active!")
        
        # Display options
        print("\nYour turn! Choose an action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            # Basic attack
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
        
        elif choice == '2':
            # Special ability
            try:
                use_special_ability(self.character, self.enemy)
                display_battle_log(f"{self.character['name']} used special ability!")
            except Exception as e:
                display_battle_log(f"Could not use ability: {e}")
        
        elif choice == '3':
            # Try to escape
            if self.attempt_escape():
                display_battle_log("You escaped from battle!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")
        
        else:
            display_battle_log("Invalid choice, basic attack used instead!")
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks for {damage} damage!")
    
    def enemy_turn(self):
       
        
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active!")
        
        # Enemy always attacks (simple AI)
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks for {damage} damage!")
    
    def calculate_damage(self, attacker, defender):
        
        # Base damage from strength
        base_damage = attacker['strength']
        
        # Reduction from defender's strength
        defense = defender['strength'] // 4
        
        # Calculate final damage
        damage = base_damage - defense
        
        # Ensure minimum damage of 1
        return max(1, damage)
    
    def apply_damage(self, target, damage):
        
        #health is reduced by the amount of damage
        target['health'] -= damage
        
        # Prevents health from going negative
        if target['health'] < 0:
            target['health'] = 0
    
    def check_battle_end(self):
        
        if self.enemy['health'] <= 0:
            return 'player'
        elif self.character['health'] <= 0:
            return 'enemy'
        else:
            return None
    
    def attempt_escape(self):
       
        #Ai used random module to generate a random number and help implement a 50% chance to escape
        # 50% chance to escape
        if random.random() < 0.5:
            self.combat_active = False
            return True
        else:
            return False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    
    
    character_class = character.get('class', '').lower()
    
    if character_class == 'warrior':
        return warrior_power_strike(character, enemy)
    elif character_class == 'mage':
        return mage_fireball(character, enemy)
    elif character_class == 'rogue':
        return rogue_critical_strike(character, enemy)
    elif character_class == 'cleric':
        return cleric_heal(character)
    else:
        return "No special ability available for this class"


def warrior_power_strike(character, enemy):
   
    #Double strength damage
    damage = character['strength'] * 2
    enemy['health'] -= damage
    #sets enemies health to 0 if it goes below 0
    if enemy['health'] < 0:
        enemy['health'] = 0
    
    return f"Power Strike! Deals {damage} damage!"


def mage_fireball(character, enemy):
  
    #Double magic damage
    damage = character['magic'] * 2
    enemy['health'] -= damage
    
    if enemy['health'] < 0:
        enemy['health'] = 0
    
    return f"Fireball! Deals {damage} damage!"


def rogue_critical_strike(character, enemy):
    
    #used same method as attempt_escape to generate a 50% chance
    if random.random() < 0.5:
        # Critical hit!
        #strength damage is tripled
        damage = character['strength'] * 3
        enemy['health'] -= damage
        
        if enemy['health'] < 0:
            enemy['health'] = 0
        
        return f"Critical Strike! Deals {damage} damage!"
    else:
        # Miss
        return "Critical Strike missed!"


def cleric_heal(character):
   
    
    heal_amount = 30
    
    # Don't exceed max health
    if character['health'] + heal_amount > character['max_health']:
        heal_amount = character['max_health'] - character['health']
    
    character['health'] += heal_amount
    
    return f"Healing Light! Restored {heal_amount} HP!"


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    
    
    return character['health'] > 0


def get_victory_rewards(enemy):
   
    
    return {
        'xp': enemy.get('xp_reward', 25),
        'gold': enemy.get('gold_reward', 10)
    }


def display_combat_stats(character, enemy):
    
    
    print(f"\n--- Combat Status ---")
    print(f"{character['name']}: HP={character['health']}/{character['max_health']} | STR={character['strength']} | MAG={character['magic']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']} | STR={enemy['strength']} | MAG={enemy['magic']}")
    print("-" * 40)


def display_battle_log(message):
    
    
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

