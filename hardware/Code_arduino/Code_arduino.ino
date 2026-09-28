#include <Servo.h>  // Inclusion de la bibliothèque Servo pour contrôler un servomoteur

// Définition des broches utilisées
#define MAX_LEN_MESSAGE 20  // Nombre max de caractères du message reçu par le port série
#define ledPinInfo 2        // LED indiquant la réception d'un message
#define ledPinFrequency 3   // LED clignotant selon la fréquence
#define ledPinLevelRed 4    // LED rouge pour afficher le niveau
#define ledPinLevelGreen 5  // LED verte pour afficher le niveau
#define buttonPin 6         // Bouton pour changer le niveau
#define servoPin 7          // Broche du servomoteur azimut
#define servoPin 8          // Broche du servomoteur altitude

Servo SERVO1;  // Création de l'objet servomoteur azimut
Servo SERVO2;  // Création de l'objet servomoteur altitude
char message[MAX_LEN_MESSAGE];  // Tableau pour stocker le message reçu
int azimuth, altitude, power, frequencyThrow, frequencyLauncher, level;  // Variables pour stocker les données reçues

// Variables pour gérer le temps (évite l'utilisation de `delay()`)
unsigned long previousMillisT = 0;
unsigned long previousMillisB = 0;
unsigned long previousMillisL = 0;
unsigned long currentMillis;

// Variables pour stocker l'état de certaines valeurs
int Tfrequency = 0;                          // Fréquence de clignotement de la LED bleue
int Lfrequency = 0;                          // Fréquence de mise à jour du lanceur
int Level = 0;                               // Niveau actuel
int statePrevious = digitalRead(buttonPin);  // État précédent du bouton
int stateCurrent = digitalRead(buttonPin);   // État actuel du bouton
int levelPrevious = 0;                       // Niveau précédent pour éviter les répétitions inutiles

void setup() {
  Serial.begin(115200);     // Initialisation de la communication série
  SERVO1.attach(servoPin);  // Attachement du servomoteur sur la broche définie
  SERVO2.attach(servoPin);

  // Configuration des broches en sortie pour les LEDs
  pinMode(ledPinInfo, OUTPUT);
  pinMode(ledPinFrequency, OUTPUT);
  pinMode(ledPinLevelRed, OUTPUT);
  pinMode(ledPinLevelGreen, OUTPUT);

  // Configuration du bouton en entrée avec résistance de pull-up activée
  pinMode(buttonPin, INPUT_PULLUP);

  // Test du servomoteur (déplacement à différentes positions)
  SERVO1.write(0);
  delay(500);
  SERVO1.write(90);
  delay(500);
  SERVO1.write(45);
  delay(500);
  SERVO2.write(0);
  delay(500);
  SERVO2.write(90);
  delay(500);
  SERVO2.write(45);
}

void loop() {
  static String inputString = "";  // Stocke la chaîne de caractères reçue
  static bool newData = false;     // Indique si une nouvelle donnée est disponible

  // Lecture du message série caractère par caractère
  while (Serial.available() > 0) {
    char receivedChar = Serial.read();

    if (receivedChar == '\n') {  // Fin de message détectée
      newData = true;
      break;
    } else {
      inputString += receivedChar;  // Ajout du caractère reçu à la chaîne
    }
  }

  if (newData) {
    // Conversion de la chaîne String en tableau de caractères
    inputString.toCharArray(message, MAX_LEN_MESSAGE);

    // Extraction des valeurs à partir du message reçu
    if (sscanf(message, "%d:%d:%d:%d:%d:%d", &azimuth, &altitude, &power, &frequencyThrow, &frequencyLauncher, &level) == 6) {

      if (currentMillis - previousMillisL >= Lfrequency) {
        previousMillisL = currentMillis;  // Mise à jour du dernier temps d'exécution

        // Mise à jour de la position du servomoteur en fonction des angles reçus
        SERVO1.write(45 - azimuth);
        SERVO2.write(45 - altitude);
      }

      // Filtrage des interférences sur la fréquence
      if ((frequencyThrow == 0) || (frequencyThrow > 99)) {
        Tfrequency = frequencyThrow;
      }

      currentMillis = millis();  // Obtention du temps actuel
      // Filtrage des interférences sur la fréquence
      if ((frequencyLauncher == 0) || (frequencyLauncher > 99)) {
        Lfrequency = frequencyLauncher;
      }

      // Mise à jour du niveau si aucune valeur précédente
      if (Level == 0) {
        Level = level;
      }
    } else {
      Serial.println("Erreur de format");  // Message d'erreur si le format est incorrect
    }

    // Clignotement de la LED pour indiquer la réception d'un message
    digitalWrite(ledPinInfo, HIGH);
    delay(50);
    digitalWrite(ledPinInfo, LOW);

    // Réinitialisation des variables pour la prochaine lecture
    inputString = "";
    newData = false;
  }

  // Gestion de la LED de fréquence si une fréquence valide a été reçue
  if (Tfrequency != 0) {
    currentMillis = millis();  // Obtention du temps actuel

    if (currentMillis - previousMillisT >= Tfrequency) {
      previousMillisT = currentMillis;  // Mise à jour du dernier temps d'exécution

      // Clignotement de la LED de fréquence
      digitalWrite(ledPinFrequency, LOW);
      delay(2000);
      digitalWrite(ledPinFrequency, HIGH);
    }
  }

  // Affichage du niveau uniquement s'il a changé
  if (Level != levelPrevious) {
    Serial.println(Level);
    levelPrevious = Level;
  }

  // Gestion de l'affichage des LEDs en fonction du niveau reçu
  if (Level == 1) {
    digitalWrite(ledPinLevelGreen, LOW);
    digitalWrite(ledPinLevelRed, HIGH);
  } else if (Level == 2) {
    digitalWrite(ledPinLevelGreen, LOW);
    digitalWrite(ledPinLevelRed, LOW);
  } else if (Level == 3) {
    digitalWrite(ledPinLevelGreen, HIGH);
    digitalWrite(ledPinLevelRed, LOW);
  }

  // Gestion du bouton pour modifier le niveau
  currentMillis = millis();
  stateCurrent = digitalRead(buttonPin);

  // Détection d'un appui (changement d'état de LOW à HIGH)
  if ((stateCurrent == 1) && (statePrevious == 0) && (currentMillis - previousMillisB >= 300)) {
    previousMillisB = currentMillis;  // Mise à jour du dernier temps d'appui
    Level += 1;                       // Incrémentation du niveau

    // Retour à 1 si on dépasse le niveau 3
    if (Level > 3) {
      Level = 1;
    }
  }

  statePrevious = stateCurrent;  // Mise à jour de l'état du bouton
}
