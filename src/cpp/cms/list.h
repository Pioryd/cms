#ifndef FW_CMS_IMMUTABLE_LIST_H
#define FW_CMS_IMMUTABLE_LIST_H

#include <functional>
#include <vector>
#include "immutable__.h"

namespace cms
{
template <typename T>
class immutable_list : public immutable__<std::vector<T>>
{
public:
  immutable_list() : immutable__(new std::vector<T>) {}
  immutable_list(std::initializer_list<T> init_list)
      : immutable__(new std::vector<T>(init_list)) {}
  /* Cpp have 2 types of initialization:
      1) MyClass obj(another_obj); // Python COPY
      2) MyClass obj = another_obj; // Python REFERENCE
  */
  immutable_list(const immutable_list &list_to_copy) = delete;

  operator std::vector<T> &() const { return std::vector<T>; };
  operator const std::vector<T> &() { return std::vector<T>; };

  T operator[](unsigned i) const { return T; }
  T &operator[](unsigned i) { return T; }

  void clear() {}

  void append(T element) {}

  void extend(immutable_list<T> &list)
  {
  }

  void insert(int64_t position, T element)
  {
  }

  void remove(T element)
  {
  }

  void pop(int64_t position)
  {
  }

  int64_t index(T element)
  {
    return 0;
  }

  int64_t count(T element)
  {
    return 0;
  }

  void sort(std::function<bool(T &)> sort = nullptr, bool reverse = false)
  {
  }

  void reverse() {}

private:
  friend immutable_list;
};

} // namespace cms

#endif // #ifndef FW_CMS_IMMUTABLE_LIST_H
