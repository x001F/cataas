from aiogram.filters.state import State, StatesGroup
# i'm fucking genius


class CommonForm(StatesGroup):
    # Only for /cattype, /catsize, /catfilter
    image_type = State()
    size = State()


class FiltersForm(StatesGroup):
    # Only for /catfilter
    wait = State()
    rgb = State()


class TextColorSizeGifForm(StatesGroup):
    # Only for /catgifsaysmore
    text = State()
    fontColor = State()
    fontSize = State()
    type = State()


class TextGifForm(StatesGroup):
    # Only for /catgifsays
    text = State()


class TextColorSizeForm(StatesGroup):
    # Only for /catsaysmore
    text = State()
    fontColor = State()
    fontSize = State()


class TagTextForm(StatesGroup):
    # Only for /cattag, /catsays
    tag = State()
    text = State()


class TagAndTextForm(StatesGroup):
    # Only for /cattagsays
    tag = State()
    text = State()
