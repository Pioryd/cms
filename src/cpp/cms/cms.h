#ifndef FW_CMS_CMS_H
#define FW_CMS_CMS_H

#include "list.h"
#include "dict.h"
#include "string.h"

namespace cms {
cms::string str(int64_t value);

template <typename T>
int64_t len(immutable_list<T>& list) {
  return list.object_()->size();
}

int64_t len(const cms::string& string);

template <typename T>
void copy(immutable_list<T>& to_list, immutable_list<T>& from_list) {
  to_list.extend(from_list);
}
template <typename T, typename U>
int64_t len(immutable_dict<T, U>& dict) {
  return dict.object_()->size();
}
template <typename T, typename U>
void copy(immutable_dict<T, U>& to_list, immutable_dict<T, U>& from_list) {
  to_list.extend(from_list);
}
}  // namespace cms

#endif  // #ifndef FW_CMS_CMS_H
