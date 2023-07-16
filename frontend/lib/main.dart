import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'mqtt.dart';
import 'mqtt_state.dart';
import 'package:uuid/uuid.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (context) => MQTTAppState(),
        ),
      ],
      child: const MaterialApp(
        home: Home(),
      ),
    );
  }
}

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  String host = "192.168.178.2";
  String topic = "HS_Coburg";
  late MQTTAppState currentAppState;
  late MQTTManager manager;

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    final MQTTAppState appState = Provider.of<MQTTAppState>(context);
    currentAppState = appState;

    int currentCars = currentAppState.getcurrentCars;
    int maxCars = currentAppState.getMaxCars;
    String siteName = currentAppState.getSiteName;
    bool isConnected = currentAppState.getIsConnected;

    if (!isConnected) {
      configureAndConnect();
    }

    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        title: const Text("Parkhaus Auslastung"),
        centerTitle: true,
        backgroundColor: Colors.grey[850],
        elevation: 5.0,
      ),
      body: Padding(
        padding: const EdgeInsets.fromLTRB(30.0, 10, 30, 0),
        child: Center(
          child: Container(
            margin: const EdgeInsets.fromLTRB(0, 0, 0, 100),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Container(
                    margin: const EdgeInsets.fromLTRB(0, 0, 0, 50),
                    child: Text(
                      siteName,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                          color: Colors.grey, letterSpacing: 1.2, fontSize: 30),
                    ),
                  ),
                  Text(
                    "${maxCars - currentCars}",
                    style: TextStyle(
                        color: Color.fromARGB(
                            200,
                            (currentCars / maxCars * 255).round(),
                            ((1 - currentCars / maxCars) * 255).round(),
                            0),
                        letterSpacing: 2,
                        fontSize: 80,
                        fontWeight: FontWeight.w300),
                  ),
                  Text(
                    "${(currentCars / maxCars * 100).toStringAsFixed(1)} %",
                    style: const TextStyle(
                        color: Colors.grey, letterSpacing: 2, fontSize: 20),
                  )
                ]),
          ),
        ),
      ),
    );
  }

  void configureAndConnect() {
    manager = MQTTManager(
        host: host,
        topic: topic,
        identifier: const Uuid().v4(),
        state: currentAppState);
    manager.initializeMQTTClient();
    manager.connect();
  }

  void disconnect() {
    manager.disconnect();
  }
}
