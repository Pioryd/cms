#ifndef FW_CMS_IMMUTABLE_LIST_H
#define FW_CMS_IMMUTABLE_LIST_H

#include <functional>
#include <vector>
#include "immutable__.h"

namespace cms {
template <typename T>
class immutable_list : public immutable__<std::vector<T>> {
 public:
  immutable_list() : immutable__(new std::vector<T>) {}
  immutable_list(std::initializer_list<T> init_list)
      : immutable__(new std::vector<T>(init_list)) {}
  /* Cpp have 2 types of initialization:
      1) MyClass obj(another_obj); // Python COPY
      2) MyClass obj = another_obj; // Python REFERENCE
  */
  immutable_list(const immutable_list& list_to_copy) = delete;

  operator std::vector<T>&() const { return *object_(); };
  operator const std::vector<T>&() { return *object_(); };

  T operator[](unsigned i) const { return (*object_())[i]; }
  T& operator[](unsigned i) { return (*object_())[i]; }

  void clear() { object_()->clear(); }

  void append(T element) { object_()->push_back(element); }

  void extend(immutable_list<T>& list) {
    object_()->insert(object_()->end(), list.object_()->begin(),
                      list.object_()->end());
  }

  void insert(int64_t position, T element) {
    object_()->insert(object_()->begin() + position, element);
  }

  void remove(T element) {
    it = std::find(object_()->begin(), object_()->end(), element);
    if (it != object_()->end()) object_()->erase(it);
  }

  void pop(int64_t position) {
    object_()->erase(object_()->begin() + position);
  }

  int64_t index(T element) {
    it = std::find(object_()->begin(), object_()->end(), element);
    if (it != object_()->end()) return -1;
    return it - object_()->begin();
  }

  int64_t count(T element) {
    return std::count(object_()->begin(), object_()->end(), element);
  }

  void sort(std::function<bool(T&)> sort = nullptr, bool reverse = false) {
    if (sort)
      std::sort(object_()->begin(), object_()->end(), sort);
    else if (reverse == true)
      std::reverse(object_()->begin(), object_()->end());
    else
      std::sort(object_()->begin(), object_()->end());
  }

  void reverse() { std::reverse(object_()->begin(), object_()->end()); }

 private:
  friend immutable_list;
};

}  // namespace cms

#endif  // #ifndef FW_CMS_IMMUTABLE_LIST_H
