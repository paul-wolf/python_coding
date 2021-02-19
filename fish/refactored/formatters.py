from typing import Optional, Callable

import constants


def get_formatted_fish(name_data, formatter: Optional[Callable] = None):
    return (
        formatter(name_data) if formatter else constants.NAME_TEMPLATE.format(name_data)
    )
