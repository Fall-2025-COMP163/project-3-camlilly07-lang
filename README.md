
1. **Module Architecture:** Explain your module organization
   
game_data.py – Loads all the game info from text files, like items and quests. It also checks that the data is formatted correctly.

character_manager.py – Handles creating the player’s character and managing its stats.

inventory_system.py – Manages the player’s items, such as adding, removing, or using items.

quest_handler.py – Keeps track of quests: which ones you’ve started, completed, or still need to finish.

combat_system.py – Controls battles, including damage, health changes, and enemy interactions.

custom_exceptions.py – Stores all custom error types the game uses so the other modules can easily raise specific errors.

main.py – The file that starts the game. It loads everything, creates the character, and runs the main game loop.


2. **Exception Strategy:** Describe when/why you raise specific exceptions
If the game loads a file like items or quests and something is formatted wrong or missing, a custom exception is raised. This stops the game before it uses broken data.

If the player tries to do something they aren’t allowed to do like use an item they don’t have or choose an invalid character class an exception is raised so the game knows the action isn’t valid.

If something happens that shouldn’t be possible like the player having negative health, an exception is raised to flag the mistake.
   
3. **Design Choices:** Justify major decisions
  
the code was split into different files so each file focuses on one job. This makes the project easier to work on and easier to fix if something breaks.

Loading and checking game data at the start:
Instead of loading item and quest data over and over, the game reads everything once at the beginning. This keeps the game running smoothly and prevents errors later.

Using custom exceptions:
I was given special error types so the game can tell the difference between bad data, bad player actions, or actual bugs. This helps the game give clearer messages and prevents crashes.

Following the required function names and structure:
The project has automated tests, so I made sure my functions match the exact names and inputs they expect. This helps everything work correctly together.

Choosing simple designs instead of complicated ones:
 I focused on clear and simple code instead of branching out and adding creative things like new special attacks, this can prevent any code from not working. This makes the game easier to understand, easier to debug, and easier for someone else to modify in the future.

   
4. **AI Usage:** Detail what AI assistance you used

    Copilot was used to fix formatting of the program, fix try/except handling, and fix errors in loops like in inventory_system.py. Copilot was used after each module was completed to ensure correctness.

   Copilot was used to help with isinstance and check to make sure required fields have an exact type (health, int)

   VSCode will automatically suggest simple blocks of code like setting up for/while loops which was used in this project.

   
5. **How to Play:** Instructions for running the game

have Python installed 

Run the game via the main.py launcher:

python main.py

Upon starting, you will be prompted to create a character (choose class: Warrior, Mage, Rogue, Cleric — names must match exactly).

Once your character is created, you can interact via command-line to: view inventory, equip items, view quests, accept quests, fight enemies (goblin, orc, dragon, etc.), manage character/quests/inventory.

Your progress (inventory, quest status, character stats) will be automatically saved into data/save_games/, allowing you to quit and resume later.

To restart or begin a new game — you can either pick a new save or delete the old save file.



