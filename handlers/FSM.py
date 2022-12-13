from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    teaching = State()
    ask_eche_primer = State()
    strana = State()
    pravilo = State()
    play = State()
    prodolzhaem = State()
    chose_theme = State()
    chose_theme_btn = State()
    chose_theme_for_rule = State()
    play_1 = State()
    mem_rule = State()
    mem_rule_crt = State()
    admin_statistics = State()