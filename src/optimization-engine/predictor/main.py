import helpers
import spotPredictor
import privateInit

def main():
    spots = helpers.getSpotInstances()
    for spot in spots:
        spotPredictor.predict(spot)

    privateInit.updatePrivateConfig()
    
if __name__ == '__main__':
    main()