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

  operator std::map<T, U> &() const { return *object_(); };
  operator const std::map<T, U> &() { return *object_(); };

  U operator[](T key) const { return (*object_())[key]; }
  U &operator[](T key) { return (*object_())[key]; }

  void clear() { object_()->clear(); }

  U get(T &key) { return (*object_())[key]; }

  void remove(T element)
  {
    it = std::find(object_()->begin(), object_()->end(), element);
    if (it != object_()->end())
      object_()->erase(it);
  }

  void pop(int64_t position) { object_()->erase(object_()->begin() + position); }
  void popitem() { object_()->erase(object_()->end() - 1); }
  void update(std::initializer_list<std::pair<const T, U>> init_list)
  {
    for (auto &[key, value] : init_list)
      (*object_())[key] = value;
  }
  void update(immutable_dict &dict)
  {
    for (auto &[key, value] : (*dict.object_()))
      (*object_())[key] = value;
  }

private:
  friend immutable_dict;
};

template <typename T, typename U>
T dict_key(immutable_dict<T, U> &dict, int64_t position)
{
  auto it = (*dict.object_()).begin();
  if (position > 0)
    std::advance(it, position);
  return it->first;
}
template <typename T, typename U>
U dict_value(immutable_dict<T, U> &dict, int64_t position)
{
  auto it = (*dict.object_()).begin();
  if (position > 0)
    std::advance(it, position);
  return it->second;
}

template <typename T, typename U>
immutable_list<T> keys(immutable_dict<T, U> &dict)
{
  immutable_list<T> keys;
  for (auto const &[key, value] : (*dict.object_()))
    keys.append(key);
  return keys;
}
template <typename T, typename U>
immutable_list<U> values(immutable_dict<T, U> &dict)
{
  immutable_list<U> values;
  for (auto const &[key, value] : (*dictnobject_()))
    values.append(value);
  return values;
}
} // namespace cms

#endif // #ifndef FW_CMS_IMMUTABLE_DICT_H
