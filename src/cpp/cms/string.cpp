#include "string.h"

namespace cms
{
string::string() {}

string::string(const string &cpp_string) { std_string_ = cpp_string; }

string::string(char character) { std_string_ = std::string(1, character); }

string::string(const char *c_string) { std_string_ = c_string; }

string::string(const std::string &cpp_string) { std_string_ = cpp_string; }

string::operator std::string() const { return std_string_; }

string::operator const std::string &() { return std_string_; }

char string::operator[](unsigned i) const { return std_string_[i]; }

char &string::operator[](unsigned i) { return std_string_[i]; }

string &string::operator=(const string &cpp_string)
{
  std_string_ = cpp_string;
  return *this;
}

string &string::operator+=(const string &cpp_string)
{
  std_string_ = std_string_ + (std::string)cpp_string;
  return *this;
}

string operator+(const string &lhs, const string &rhs)
{
  return string(lhs) += rhs;
}

string operator+(const string &lhs, char rhs)
{
  return string(lhs) += string(rhs);
}

string operator+(const string &lhs, const char *rhs)
{
  return string(lhs) += string(rhs);
}

string operator+(char lhs, const string &rhs) { return string(lhs) += rhs; }

string operator+(const char *lhs, const string &rhs)
{
  return string(lhs) += rhs;
}

bool operator==(const string &lhs, const string &rhs)
{
  return (std::string)lhs == (std::string)rhs;
}

bool operator==(const string &lhs, char rhs)
{
  return (std::string)lhs == std::string(1, rhs);
}

bool operator==(const string &lhs, const char *rhs)
{
  return (std::string)lhs == rhs;
}

bool operator==(char lhs, const string &rhs)
{
  return std::string(1, lhs) == (std::string)rhs;
}

bool operator==(const char *lhs, const string &rhs)
{
  return lhs == (std::string)rhs;
}

bool operator!=(const string &lhs, const string &rhs)
{
  return (std::string)lhs != (std::string)rhs;
}

bool operator!=(const string &lhs, char rhs)
{
  return (std::string)lhs != std::string(1, rhs);
}

bool operator!=(const string &lhs, const char *rhs)
{
  return (std::string)lhs != rhs;
}

bool operator!=(char lhs, const string &rhs)
{
  return std::string(1, lhs) != (std::string)rhs;
}

bool operator!=(const char *lhs, const string &rhs)
{
  return lhs != (std::string)rhs;
}
} // namespace cms