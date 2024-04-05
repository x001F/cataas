from .cat import cat_router
from .catsays import cat_says_router
from .catsaysmore import cat_says_more_router
# from .cattag import cat_tag_router
# from .cattagsays import cat_tagsays_router
from .catgif import cat_gif_router
from .catgifsays import cat_gif_says_router
from .catgifsaysmore import cat_gif_says_more_router
from .cattype import cat_type_router
from .catfilter import cat_filter_router
from .catsize import cat_size_router
from .basic import basic_router

routers = (cat_router, cat_says_router, cat_says_more_router,
           cat_gif_router, cat_gif_says_router, cat_gif_says_more_router,
           cat_type_router, cat_filter_router, cat_size_router, basic_router,
           # cat_tag_router, cat_tagsays_router
           )
# *tag* commands disabled because cataas.com have problems with tags
# Some tags are exist (/api/tags, or /api/cats (in cat properties)) but cataas don't think so))
