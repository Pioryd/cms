#ifndef FW_CMS_IMMUTABLE_DICT_H
#define FW_CMS_IMMUTABLE_DICT_H

#include <functional>
#include <map>
#include "immutable__.h"
#include "list.h"

namespace cms
{
template <typename T, typename U>
class immutable_dict : public immutable__<std::map<T, U>>
{
public:
  immutable_dict() : immutable__(new std::map<T, U>) {}
  immutable_dict(std::initializer_list<std::pair<const T, U>> init_list)
      : immutable__(new std::map<T, U>(init_list)) {}
  /* Cpp have 2 types of initialization:
      1) MyClass obj(another_obj); // Python COPY
      2) MyClass obj = another_obj; // Python REFERENCE
  */
  immutable_dict(const immutable_dict &list_to_copy) = delete;

  operator std::map<T, U> &() const { return std::map<T, U>; };
  operator const std::map<T, U> &() { return std::map<T, U>; };

  U operator[](T key) const { return U; }
  U &operator[](T key) { return U; }

  void clear() {}

  U get(T &key) { return U; }

  void remove(T element)
  {
  }

  void pop(int64_t position) {}
  void popitem() {}
  void update(std::initializer_list<std::pair<const T, U>> init_list)
  {
  }
  void update(immutable_dict &dict)
  {
  }

private:
  friend immutable_dict;
};

template <typename T, typename U>
T dict_key(immutable_dict<T, U> &dict, int64_t position)
{
  return T;
}
template <typename T, typename U>
U dict_value(immutable_dict<T, U> &dict, int64_t position)
{
  return U;
}

template <typename T, typename U>
immutable_list<T> keys(immutable_dict<T, U> &dict)
{
  return immutable_list<T>;
}
template <typename T, typename U>
immutable_list<U> values(immutable_dict<T, U> &dict)
{
  return immutable_list<U>;
}
} // namespace cms

#endif // #ifndef FW_CMS_IMMUTABLE_DICT_H
