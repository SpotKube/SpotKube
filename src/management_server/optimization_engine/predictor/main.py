import helpers
import spotPredictor
import privateInit

def predict():
    spots = helpers.getSpotInstances()
    for spot in spots:
        spotPredictor.predict(spot)

    privateInit.updatePrivateConfig()
    
if __name__ == '__main__':
    predict()