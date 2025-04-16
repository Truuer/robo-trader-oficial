import 'package:flutter/material.dart';

// Tema claro
final ThemeData lightTheme = ThemeData(
  primarySwatch: Colors.blue,
  brightness: Brightness.light,
  scaffoldBackgroundColor: Colors.white,
  appBarTheme: AppBarTheme(
    backgroundColor: Colors.blue,
    foregroundColor: Colors.white,
    elevation: 2,
  ),
  cardTheme: CardTheme(
    elevation: 2,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    selectedItemColor: Colors.blue,
    unselectedItemColor: Colors.grey,
    backgroundColor: Colors.white,
    elevation: 8,
  ),
  textTheme: TextTheme(
    headline1: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.black87),
    headline2: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.black87),
    headline3: TextStyle(fontSize: 18, fontWeight: FontWeight.w500, color: Colors.black87),
    bodyText1: TextStyle(fontSize: 16, color: Colors.black87),
    bodyText2: TextStyle(fontSize: 14, color: Colors.black54),
  ),
  colorScheme: ColorScheme.light(
    primary: Colors.blue,
    secondary: Colors.green,
    error: Colors.red,
  ),
);

// Tema escuro
final ThemeData darkTheme = ThemeData(
  primarySwatch: Colors.blue,
  brightness: Brightness.dark,
  scaffoldBackgroundColor: Color(0xFF121212),
  appBarTheme: AppBarTheme(
    backgroundColor: Color(0xFF1F1F1F),
    foregroundColor: Colors.white,
    elevation: 2,
  ),
  cardTheme: CardTheme(
    color: Color(0xFF1F1F1F),
    elevation: 2,
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(12),
    ),
  ),
  bottomNavigationBarTheme: BottomNavigationBarThemeData(
    selectedItemColor: Colors.blue,
    unselectedItemColor: Colors.grey,
    backgroundColor: Color(0xFF1F1F1F),
    elevation: 8,
  ),
  textTheme: TextTheme(
    headline1: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white),
    headline2: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.white),
    headline3: TextStyle(fontSize: 18, fontWeight: FontWeight.w500, color: Colors.white),
    bodyText1: TextStyle(fontSize: 16, color: Colors.white),
    bodyText2: TextStyle(fontSize: 14, color: Colors.white70),
  ),
  colorScheme: ColorScheme.dark(
    primary: Colors.blue,
    secondary: Colors.green,
    error: Colors.red,
  ),
);
