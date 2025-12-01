"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Cam'Ren Lilly]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    quest = quest_data_dict[quest_id]
    
    if quest_id in character.get('completed_quests', []):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' already completed")
    
    if quest_id in character.get('active_quests', []):
        return True
    
    required_level = quest.get('required_level', 1)
    if character['level'] < required_level:
        raise InsufficientLevelError(
            f"Character level {character['level']} below required {required_level}"
        )
    
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if prerequisite not in character.get('completed_quests', []):
            raise QuestRequirementsNotMetError(f"Must complete '{prerequisite}' first")
    
    if 'active_quests' not in character:
        character['active_quests'] = []
    character['active_quests'].append(quest_id)
    
    return True


def complete_quest(character, quest_id, quest_data_dict):
    
    
    # Check if quest is active
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    # Get quest data
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found in quest data")
    
    quest = quest_data_dict[quest_id]
    
    # Get rewards
    xp_reward = quest.get('reward_xp', 0)
    gold_reward = quest.get('reward_gold', 0)
    quest_title = quest.get('title', quest_id)
    
    # Award XP (causes leveling if needed)
    if xp_reward > 0:
        import character_manager
        character_manager.gain_experience(character, xp_reward)
    
    # Award gold
    if gold_reward > 0:
        import character_manager
        character_manager.add_gold(character, gold_reward)
    
    # Move from active to completed
    character['active_quests'].remove(quest_id)
    if 'completed_quests' not in character:
        character['completed_quests'] = []
    character['completed_quests'].append(quest_id)
    
    # Return result
    return {
        'quest_id': quest_id,
        'quest_title': quest_title,
        'xp_reward': xp_reward,
        'gold_reward': gold_reward
    }

def abandon_quest(character, quest_id):
    
    
    if quest_id not in character.get('active_quests', []):
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active")
    
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    
    
    active_quests = []
    for quest_id in character.get('active_quests', []):
        if quest_id in quest_data_dict:
            active_quests.append(quest_data_dict[quest_id])
    
    return active_quests


def get_completed_quests(character, quest_data_dict):
   
    
    completed_quests = []
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            completed_quests.append(quest_data_dict[quest_id])
    
    return completed_quests


def get_available_quests(character, quest_data_dict):
   
    
    available = []
    
    for quest_id, quest in quest_data_dict.items():
        if quest_id in character.get('completed_quests', []):
            continue
        if quest_id in character.get('active_quests', []):
            continue
        
        required_level = quest.get('required_level', 1)
        if character['level'] < required_level:
            continue
        
        prerequisite = quest.get('prerequisite', 'NONE')
        if prerequisite != 'NONE':
            if prerequisite not in character.get('completed_quests', []):
                continue
        
        available.append(quest)
    
    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    
    
    return quest_id in character.get('completed_quests', [])


def is_quest_active(character, quest_id):
    
    
    return quest_id in character.get('active_quests', [])


def can_accept_quest(character, quest_id, quest_data_dict):
    
  
    
    if quest_id not in quest_data_dict:
        return False
    
    quest = quest_data_dict[quest_id]
    
    if quest_id in character.get('completed_quests', []):
        return False
    
    if quest_id in character.get('active_quests', []):
        return False
    
    required_level = quest.get('required_level', 1)
    if character['level'] < required_level:
        return False
    
    prerequisite = quest.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        if prerequisite not in character.get('completed_quests', []):
            return False
    
    return True


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
   
    # TODO: Implement prerequisite chain tracing
    
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found")
    
    chain = []
    current_id = quest_id
    visited = set()
    
    while current_id is not None:
        if current_id in visited:
            break
        visited.add(current_id)
        
        if current_id not in quest_data_dict:
            break
        
        chain.insert(0, current_id)
        
        quest = quest_data_dict[current_id]
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite == 'NONE':
            break
        
        current_id = prerequisite
    
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    
    
    if not quest_data_dict:
        return 0.0
    
    total_quests = len(quest_data_dict)
    completed_quests = len(character.get('completed_quests', []))
    
    percentage = (completed_quests / total_quests) * 100
    return percentage


def get_total_quest_rewards_earned(character, quest_data_dict):
    
    
    total_xp = 0
    total_gold = 0
    
    for quest_id in character.get('completed_quests', []):
        if quest_id in quest_data_dict:
            quest = quest_data_dict[quest_id]
            total_xp += quest.get('reward_xp', 0)
            total_gold += quest.get('reward_gold', 0)
    
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }


def get_quests_by_level(quest_data_dict, min_level, max_level):
   
    
    quests = []
    
    for quest_id, quest in quest_data_dict.items():
        required_level = quest.get('required_level', 1)
        if min_level <= required_level <= max_level:
            quests.append(quest)
    
    return quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
   
    
    print(f"\n{'=' * 50}")
    print(f"=== {quest_data.get('title', 'Unknown Quest')} ===")
    print(f"{'=' * 50}")
    print(f"\nDescription: {quest_data.get('description', 'No description')}")
    print(f"\nRequirements:")
    print(f"  Level: {quest_data.get('required_level', 1)}")
    
    prerequisite = quest_data.get('prerequisite', 'NONE')
    if prerequisite != 'NONE':
        print(f"  Prerequisite: {prerequisite}")
    
    print(f"\nRewards:")
    print(f"  Experience: {quest_data.get('reward_xp', 0)} XP")
    print(f"  Gold: {quest_data.get('reward_gold', 0)} Gold")
    print(f"\n{'=' * 50}\n")


def display_quest_list(quest_list):
    
    
    if not quest_list:
        print("\nNo quests to display.")
        return
    
    print(f"\n{'=' * 60}")
    print(f"{'Title':<25} {'Level':<10} {'XP':<10} {'Gold':<10}")
    print(f"{'=' * 60}")
    
    for quest in quest_list:
        title = quest.get('title', 'Unknown')[:23]
        level = quest.get('required_level', 1)
        xp = quest.get('reward_xp', 0)
        gold = quest.get('reward_gold', 0)
        
        print(f"{title:<25} {level:<10} {xp:<10} {gold:<10}")
    
    print(f"{'=' * 60}\n")


def display_character_quest_progress(character, quest_data_dict):
   
    
    active_count = len(character.get('active_quests', []))
    completed_count = len(character.get('completed_quests', []))
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print(f"\n{'=' * 50}")
    print("QUEST PROGRESS")
    print(f"{'=' * 50}")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion: {percentage:.1f}%")
    print(f"\nTotal Rewards Earned:")
    print(f"  Experience: {rewards['total_xp']} XP")
    print(f"  Gold: {rewards['total_gold']} Gold")
    print(f"{'=' * 50}\n")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
   
    
    for quest_id, quest in quest_data_dict.items():
        prerequisite = quest.get('prerequisite', 'NONE')
        
        if prerequisite != 'NONE':
            if prerequisite not in quest_data_dict:
                raise QuestNotFoundError(
                    f"Quest '{quest_id}' has invalid prerequisite '{prerequisite}'"
                )
    
    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

