card_manifest = None


def create_card_manifest(card_manifest_dict):
    global card_manifest
    if card_manifest is None:
        card_manifest = card_manifest_dict


def get_card_manifest():
    global card_manifest
    return card_manifest
