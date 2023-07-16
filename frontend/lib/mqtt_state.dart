import 'dart:convert';
import 'dart:ffi';
import 'package:flutter/cupertino.dart';

class MQTTAppState with ChangeNotifier {
  int _currentCars = 0;
  int _maxCars = 0;
  String _siteName = "";
  bool _isConnected = false;

  void setIsConnected(bool newValue) {
    _isConnected = newValue;
  }

  void setReceivedText(String json) {
    Map<String, dynamic> counter = jsonDecode(json);

    _maxCars = counter['MaxCars'].clamp(1, 0x7FFFFFFFFFFFFFFF);
    _currentCars = counter['CurrentCars'].clamp(0, _maxCars);
    _siteName = counter['DisplayName'];

    notifyListeners();
  }

  int get getcurrentCars => _currentCars;
  int get getMaxCars => _maxCars;
  String get getSiteName => _siteName;
  bool get getIsConnected => _isConnected;
}
