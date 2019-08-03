#include "string.h"

namespace cms
{
string::string() {}

string::string(const string &cpp_string) {}

string::string(char character) {}

string::string(const char *c_string) {}

string::string(const std::string &cpp_string) {}

string::operator std::string() const { return ""; }

string::operator const std::string &() { return ""; }

char string::operator[](unsigned i) const { return 0; }

char &string::operator[](unsigned i)
{
  char a;
  return a;
}

string &string::operator=(const string &cpp_string)
{
  return *this;
}

string &string::operator+=(const string &cpp_string)
{
  return *this;
}

string
operator+(const string &lhs, const string &rhs)
{
  return "";
}

string operator+(const string &lhs, char rhs)
{
  return "";
}

string operator+(const string &lhs, const char *rhs)
{
  return "";
}

string operator+(char lhs, const string &rhs) { return ""; }

string operator+(const char *lhs, const string &rhs)
{
  return "";
}

bool operator==(const string &lhs, const string &rhs)
{
  return false;
}

bool operator==(const string &lhs, char rhs)
{
  return false;
}

bool operator==(const string &lhs, const char *rhs)
{
  return false;
}

bool operator==(char lhs, const string &rhs)
{
  return false;
}

bool operator==(const char *lhs, const string &rhs)
{
  return false;
}

bool operator!=(const string &lhs, const string &rhs)
{
  return false;
}

bool operator!=(const string &lhs, char rhs)
{
  return false;
}

bool operator!=(const string &lhs, const char *rhs)
{
  return false;
}

bool operator!=(char lhs, const string &rhs)
{
  return false;
}

bool operator!=(const char *lhs, const string &rhs)
{
  return false;
}
} // namespace cms