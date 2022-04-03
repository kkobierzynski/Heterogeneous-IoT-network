ADC_MODE(ADC_VCC);  //umożliwia  odczytanie napięcia vcc za pomocą komendy ESP.getVcc()

//Dodanie do kodu potrzebnych bibliotek
#include <DHTesp.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

//Definiowanie nazw odpowiednio dla klienta WiFi, klienta mqtt oraz dla DHT11 - czujnika temperatury i wilgotności
WiFiClient wifiClient; 
PubSubClient mqtt_client(wifiClient);
DHTesp dht;

//Definiowanie danych potrzebnych do poprawnego połączenia się z siecią WiFi oraz serwerem mqtt
const char* wifi_name = "UPC9223073";
const char* password = "DoDoder285Na1";
const char* mqtt_server = "192.168.0.220";  //Numer IP urządzenia na którym znajduje się serwer mqtt, w tym wypadku jest to ip Raspberrypi
const char* mqtt_user_name = "pi";  //Opcjonalna nazwa użytkownika i hasło. Można połaczyć się bez nich jezeli w konfiguracji mosquitto doda się -> allow_anonymous true
const char* mqtt_password = "raspberrypi";

//Zdefiniowanie struktury danych jaka będzie wysyłana przez MQTT w formacie JSON
struct data{
  float temperature;
  float humidity;
  unsigned long real_time;
  String wifi_name;
  String ip;
};

//Definiowanie rozmiaru zmiennych dla nazwy płytki oraz nazw topików
char board_id[16];
char topic_pub_data[256];
char topic_sub_led[256];


int LED2 = 2; //Dla używanego modelu ESP8226 dioda led znajduje się na pinie 2
float humidity;
float temperature;



//--------------------------------------------------------------------------------------------

//Funkcja ta wykorzystując zmienne znajdujące się w strukturze danych tworzy strukturę JSON i zapisuje ją do łańcucha znaków - chain. Dopiero tak przetworzone dane będą wysłane przez MQTT
void serialize_json(struct data json_data, char *chain, int size){
  DynamicJsonDocument doc(300);
  JsonObject sensor_data = doc.createNestedObject("Data");  //Dodanie do korzenia obiektu który będzie zawierać dane odczytane z sensora
  sensor_data["Temperature"] = json_data.temperature;
  sensor_data["Humidity"] = json_data.humidity;

  JsonObject network_data = doc.createNestedObject("Network");  //Dodanie do korzenia obiektu który będzie zawierać dane dotyczące sieci
  network_data["Wifi_name"] = json_data.wifi_name;
  network_data["Server_ip"] = json_data.ip;

  doc["Time"] = json_data.real_time;

  serializeJson(doc, chain, 512); //zapisywanie całej struktury doc do łańcucha znaków chain
  Serial.println(chain);
}




//Funkcja umożłiwiająca połączenie się do sieci WiFi. Funkcja wywoływana jest w części setup()
void wifi_connection(){
  Serial.println("Establishing a wifi connection");
  WiFi.mode(WIFI_STA);  //Informuje że płytka ma pracować w trybie station (czyli jest urządzeniem które podłącza sie do punktu dostępowego)
  WiFi.begin(wifi_name, password);  //połączenie się do WiFi z użyciem podanych wcześniej dancyh

  //Pętla będzie wykonywać się tak długo aż uda się nawiązać połączenie
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
  
}




//Funkcja umożliwiająca połączenie się z serwerem MQTT
void mqtt_connection(){
  while (!mqtt_client.connected()){
    //Argument w if wykonuje połączenie z serwerem mqtt korzystając z podanych zmiennych. Dodatkowo zwraca false lub true w zależności od połączenia. 
    if(mqtt_client.connect(board_id, mqtt_user_name, mqtt_password)){
      mqtt_client.subscribe(topic_sub_led); //Jezeli połączenie się udało dokonaj subskrypcji topików.
    }else {
      Serial.print("MQTT - Failed to connect");
    }
  }
  
}




//Funkcja ta wywołuje się gdy do urządzenia przychodzi jakiś topick
void callback(char* topic, byte* payload, unsigned int length){
  
    char chain[512];
    char *message = (char *)malloc(length); // Rezerwowanie pamięci dla message do której kopiowany będzie payload
    strncpy(message, (char*)payload, length); //kopiowanie informacji z payloadu do message
    //message[length] = '\0'; //do usuniecia
    Serial.printf("Message received %s\n", message);

    if (strcmp(topic, topic_sub_led) == 0) {
        StaticJsonDocument<512> root;
        DeserializationError error = deserializeJson(root, message, length);  //Sprawdzenie ewentualnego błedu 

        if (error) {
            Serial.print("Error deserializeJson() failed: ");
            Serial.println(error.c_str());
        } else if (root.containsKey("led_status")) {  //Wykonaj dla zmiennej led_status
            int value = root["led_status"];
            if(value == 0){
              digitalWrite(LED2, HIGH);
            } else if(value == 1){
              digitalWrite(LED2, LOW);
            }
            
        } else {
            Serial.print("Error : ");
            Serial.println("Key not found in JSON");
        }
    }else{
      Serial.print("Error: Topic not found");
    }
    free(message);  //Zwolnienie pamięci zarezerowowanej dla message
    
}

//--------------------------------------------------------------------------------------------

//Funkcja setup uruchamiana jest jednorazowo podczas właczania programu
void setup(){
  Serial.begin(115200); //Ustawia szybkość transmisji danych w bitach na sekundę (bodów) dla szeregowej transmisji danych, aby komunikować się z monitorem szeregowym.
  pinMode(LED2, OUTPUT);

  dht.setup(5, DHTesp::DHT11);

  //Definicja topików oraz przypisanie nazwy oraz id płytki
  sprintf(topic_pub_data, "kitchen/data");
  sprintf(topic_sub_led, "kitchen/led");
  sprintf(board_id, "ESP%d", ESP.getChipId());

  //Połączenie do wifi oraz MQTT
  wifi_connection();
  mqtt_client.setServer(mqtt_server, 1883);
  mqtt_client.setBufferSize(512); //Ustawienie max wielkości bajtów przesyłanej wiadomości
  mqtt_client.setCallback(callback);
  mqtt_connection();
}




#define message_size 128
unsigned long last_message = 0;



//Właściwa część działania programu
void loop(){
  char chain[512];
  struct data my_data;

  //Sprawdzenie czy program jest połączony z serverem MQTT
  if (!mqtt_client.connected()){
    mqtt_connection();
  }
  
  mqtt_client.loop(); //funkcja ta musi być regularnie wywoływana aby umożliwić klientowi przetwarzanie przychodzących wiadomości w celu wysłania publikowanych danych i odświeżenia połączenia.
  unsigned long time_now = millis();

  //Wykonanie częsci kodu jedynie raz na określony czas
  if (time_now - last_message >= 1000){
    last_message = time_now;
    //char message[message_size];

    //Pobranie danych z czujnika
    humidity = dht.getHumidity();
    temperature = dht.getTemperature();

    //Zapisanie danych do struktury danych
    my_data.temperature = temperature;
    my_data.humidity = humidity;
    my_data.real_time = time_now;
    my_data.wifi_name = wifi_name;
    my_data.ip = mqtt_server;

    //Wywołanie funkcji tworzącej strukturę JSON
    serialize_json(my_data,chain,512);
    //Wysłanie struktury JSON poprzez MQTT
    mqtt_client.publish(topic_pub_data, chain);
    
  }
}
