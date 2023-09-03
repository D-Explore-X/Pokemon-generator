import random
from datetime import datetime

# Constants
PATH_TO_SPRITES = 'sprites/normal/'
PATH_TO_SHINY_SPRITES = 'sprites/shiny/'
SPRITE_EXTENSION = '.png'

class GeneratedPokemon:
    def __init__(self, pokemon=None, form=None, options=None):
        self.id = None
        self.base_name = None
        self.name = None
        self.sprite_suffix = None
        self.nature = None
        self.shiny = None
        self.date = None

        if pokemon:
            self.id = pokemon['id']
            self.base_name = pokemon['name']
            self.name = form['name'] if form else pokemon['name']
            self.sprite_suffix = form['spriteSuffix'] if form and 'spriteSuffix' in form else None
            if options and options['natures']:
                self.nature = generate_nature()
            # Simulating the shiny probability (1 in 4096)
            self.shiny = random.randint(1, 4096) == 1
            self.date = datetime.now()

    @staticmethod
    def generate(pokemon, form, options):
        return GeneratedPokemon(pokemon, form, options)

    @staticmethod
    def from_json(parsed):
        pokemon = GeneratedPokemon()
        for key, value in parsed.items():
            setattr(pokemon, key, value)
        return pokemon

    def to_html(self, include_sprite):
        classes = ""
        if self.shiny:
            classes += "shiny "
        if not include_sprite:
            classes += "imageless "
        
        sprite_html = self.to_image() if include_sprite else ""
        text_html = self.to_text()
        
        return f'<li class="{classes}">\n{sprite_html}\n{text_html}\n</li>'

    def to_text(self):
        nature_span = f'<span class="nature">{self.nature}</span>' if self.nature else ""
        star_span = '<span class="star">&starf;</span>' if self.shiny else ""
        return f'\n{nature_span}\n{self.name}\n{star_span}'

    def to_image(self):
        alt_text = ("Shiny " if self.shiny else "") + self.name
        return f'<img src="{self.get_sprite_path()}" alt="{alt_text}" title="{alt_text}" />'

    def get_sprite_path(self):
        path = PATH_TO_SHINY_SPRITES if self.shiny else PATH_TO_SPRITES
        name = self.normalize_name()
        if self.sprite_suffix:
            name += "-" + self.sprite_suffix
        return path + name + SPRITE_EXTENSION

    def normalize_name(self):
        base_name = self.base_name or self.name
        return (
            base_name.lower()
            .replace("é", "e")
            .replace("♀", "f")
            .replace("♂", "m")
            .replace("'", "")
            .replace(".", "")
            .replace(":", "")
            .replace("%", "")
            .replace(" ", "")
            .replace("-", "")
        )

def generate_nature():
    return random.choice(NATURES)

NATURES = ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle", "Hardy", "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naive", "Naughty", "Quiet", "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]
