from app.model.models import CreateThemeLogo


def clear(existing_user: CreateThemeLogo):
    existing_user.color_1=None
    existing_user.color_2 = None
    existing_user.color_3 = None
    existing_user.callback_id=None
