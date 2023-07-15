import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Home(),
    );
  }
}

class Home extends StatefulWidget {
  const Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  static const int maxSpace = 500;
  int carCounter = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        title: const Text("Parkhaus Auslastung"),
        centerTitle: true,
        backgroundColor: Colors.grey[850],
        elevation: 5.0,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          setState(() {
            if (carCounter < maxSpace) carCounter++;
          });
        },
        child: Icon(Icons.add),
        backgroundColor: Colors.grey[800],
      ),
      body: Padding(
        padding: EdgeInsets.fromLTRB(30.0, 10, 30, 0),
        child: Center(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Text(
                  "${maxSpace - carCounter}",
                  style: TextStyle(
                      color: Color.fromARGB(
                          200,
                          (carCounter / maxSpace * 255).round(),
                          ((1 - carCounter / maxSpace) * 255).round(),
                          0),
                      letterSpacing: 2,
                      fontSize: 80,
                      fontWeight: FontWeight.w300),
                ),
                Text(
                  "${(carCounter / maxSpace * 100).toStringAsFixed(1)} %",
                  style: TextStyle(
                      color: Colors.grey, letterSpacing: 2, fontSize: 20),
                )
              ]),
        ),
      ),
      persistentFooterButtons: [
        Slider.adaptive(
            value: carCounter.toDouble(),
            min: 0,
            max: maxSpace.toDouble(),
            thumbColor: Colors.grey[700],
            activeColor: Colors.grey[600],
            inactiveColor: Colors.grey[800],
            onChanged: (double newValue) {
              setState(() {
                carCounter = newValue.round();
              });
            })
      ],
    );
  }
}
