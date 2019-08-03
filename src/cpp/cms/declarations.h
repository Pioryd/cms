#ifndef FW_CMS_DECLARATIONS_H
#define FW_CMS_DECLARATIONS_H

#include "cms.h"
#include "dict.h"
#include "list.h"
#include "string.h"

#define BIND(...) std::bind(__VA_ARGS__)
#define INITIALIZER_LIST(...) \
  { __VA_ARGS__ }
#endif  // #ifndef FW_CMS_DECLARATIONS_H
