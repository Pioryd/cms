#include "cms.h"

namespace cms {
cms::string str(int64_t value) { return std::to_string(value); }

int64_t len(const cms::string& string) { return ((std::string)string).size(); }

}  // namespace cms