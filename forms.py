from wtforms import StringField, IntegerField
from flask_wtf import FlaskForm

class CupcakeForm(FlaskForm):
    """ Form to make cupcake list """
    flavor = StringField("Name of Playlist")
    size = StringField("Description of Playlist")
    rating = IntegerField("Rating of the Cupcake")
    image = StringField("Image link")