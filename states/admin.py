from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_category_name = State()
    
    # Test adding flow
    waiting_for_test_file = State()
    waiting_for_test_name = State()
    waiting_for_test_keys = State()
    # Stores current category id in state data
    
    # Video adding flow (future)
    waiting_for_video = State()
    waiting_for_video_caption = State()
    
    # Edit flows
    waiting_for_new_key = State()