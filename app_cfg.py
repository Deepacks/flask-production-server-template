app_cfg = None


def load_app_cfg(new_app_cfg):
    global app_cfg
    app_cfg = new_app_cfg


def get_app_cfg():
    global app_cfg
    return app_cfg
