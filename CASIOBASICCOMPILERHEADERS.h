#pragma once
#include <vector>

class string {
  public:
  string(const char* cstr) {}
  string() = default;
};

class list {
  public:
  float& operator[](size_t index){}
  const float& operator[](size_t index) const {}

  void size(size_t length){}
};

class matrix {
  public:
  std::vector<float>& operator[](size_t index){}
  const std::vector<float>& operator[](size_t index) const {}

  void size(size_t columns, size_t rows){} //maybe switch bc matrix row column funny
};

/*
@brief Displays text at the specified location.

@param columnNumber The column where text will begin displaying, 1 - 21.
@param lineNumber The line where text will begin displaying, 1 - 7.
@param text The text that will be displayed.
*/
void locate(const int columnNumber, const int lineNumber, string text){}
/*
@brief Displays values at the specified location.

@param columnNumber The column where values will begin displaying, 1 - 21.
@param lineNumber The line where values will begin displaying, 1 - 7.
@param number The value that will be displayed.
*/
void locate(const int columnNumber, const int lineNumber, float number){}
/*
@brief Displays values at the specified location.

@param columnNumber The column where values will begin displaying, 1 - 21.
@param lineNumber The line where values will begin displaying, 1 - 7.
@param number The value that will be displayed.
*/
void locate(const int columnNumber, const int lineNumber, int number){}