from dataclasses import dataclass


@dataclass
class Home:
    locality: str = None
    home_type: str = None
    subtype: str = None
    price: int = None
    type_of_sale: str = None
    room: int = None
    area: int = None
    equipped: bool = None
    furnished: bool = None
    open_fire: bool = None
    terrace: bool = None
    terrace_area: int = None
    garden: bool = None
    garden_area: int = None
    livable_area: int = None
    surface_of_land_area: int = None
    facades: int = None
    swimming_pool: bool = None
    state_of_building: str = None
