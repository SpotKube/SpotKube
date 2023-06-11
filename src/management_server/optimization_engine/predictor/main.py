from . import helpers
from . import spotPredictor
from . import privateInit

def predict():
    spots = helpers.getSpotInstances()
    for spot in spots:
        spotPredictor.predict(spot)

    privateInit.updatePrivateConfig()
