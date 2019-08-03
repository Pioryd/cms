#ifndef FW_CMS_STRING_H
#define FW_CMS_STRING_H

#include <string>

namespace cms
{
class string
{
public:
  string();
  string(const string &cpp_string);
  string(char);
  string(const char *c_string);
  string(const std::string &cpp_string);

  operator std::string() const;
  operator const std::string &();

  char operator[](unsigned i) const;
  char &operator[](unsigned i);

  string &operator=(const string &s);

  string &operator+=(const string &s);

  friend string operator+(const string &lhs, const string &rhs);
  friend string operator+(const string &lhs, char rhs);
  friend string operator+(const string &lhs, const char *rhs);
  friend string operator+(char lhs, const string &rhs);
  friend string operator+(const char *lhs, const string &rhs);

  friend bool operator==(const string &lhs, const string &rhs);
  friend bool operator==(const string &lhs, char rhs);
  friend bool operator==(const string &lhs, const char *rhs);
  friend bool operator==(char lhs, const string &rhs);
  friend bool operator==(const char *lhs, const string &rhs);

  friend bool operator!=(const string &lhs, const string &rhs);
  friend bool operator!=(const string &lhs, char rhs);
  friend bool operator!=(const string &lhs, const char *rhs);
  friend bool operator!=(char lhs, const string &rhs);
  friend bool operator!=(const char *lhs, const string &rhs);

private:
  std::string std_string_;
};
} // namespace cms

#endif // #ifndef FW_CMS_STRING_H
