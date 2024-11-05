import RPi.GPIO as GPIO
import time
import os
import sys

# Configuration des pins
button_pin = 17  # Le GPIO17 pour l'interrupteur
signal_pin = 4   # Le GPIO4 pour signal d'extinction

# Initialisation de GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Interrupteur avec résistance pull-up interne
GPIO.setup(signal_pin, GPIO.OUT)  # Pin pour signal d'extinction

# Fonction pour éteindre le Raspberry Pi
def shutdown():
    print("RaspberryPi shutdown")
    
    # Simulation d'un signal avant extinction
    print("Setting pin GPIO4 High")
    GPIO.output(signal_pin, GPIO.HIGH)  # Activer GPIO4
    time.sleep(1)
    print("Setting pin GPIO4 Low")
    GPIO.output(signal_pin, GPIO.LOW)   # Désactiver GPIO4
    time.sleep(1)
    
    # Effectuer l'extinction
    os.system('sudo shutdown -h now')
    sys.exit()

# Variable pour garder l'état de l'interrupteur
shutdown_triggered = False

# Vérifier l'état initial du bouton
initial_state = GPIO.input(button_pin)

if initial_state == GPIO.LOW:
    print("Switch is ON at boot, waiting for OFF to trigger shutdown")
    shutdown_triggered = True  # Marque l'extinction comme déclenchée dès le démarrage

try:
    while True:
        current_state = GPIO.input(button_pin)

        # Détecte si l'interrupteur passe de OFF (HIGH) à ON (LOW)
        if current_state == GPIO.LOW and not shutdown_triggered:
            print("Interrupteur basculé en position ON, extinction en cours...")
            shutdown()  # Appel à la fonction d'extinction
            shutdown_triggered = True  # Marque l'extinction comme déclenchée

        # Si l'interrupteur est repassé à OFF, réinitialise pour le prochain basculement
        elif current_state == GPIO.HIGH and shutdown_triggered:
            print("Interrupteur remis en position OFF, prêt pour une nouvelle extinction.")
            shutdown_triggered = False  # Réinitialise l'état pour la prochaine extinction

        time.sleep(0.1)  # Pause pour éviter un survoltage du CPU

except KeyboardInterrupt:
    GPIO.cleanup()

