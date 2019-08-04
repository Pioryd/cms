# CMS (C++ Modular Scripting) [*Early Access*]

**Project Status:**
* Build: Stable
* Type: Early Access
* Tests: full

CMS allow to script in C++ syntax. Can work in 2 ways:
* compiled as c++ source
* scripted as converted to python

For example CMS(C++) file converted to python file:

**C++:**
```cpp
#include <cms>

cms::sometype type_1 = INITIALIZER_LIST("heel", "check", "top")

struct MyStruct : OtherStruct, ParentStruct { 
  void fun(const std::string& name, int* type, char val) {
    while(a > 5 && c <= 9 || (a == 12 && c < d)) {
      print("hello");
    }
  }
}
// Some comment
```
**Python:**
```python
import cms

type_1 = {"heel", "check", "top"}


class MyStruct(OtherStruct, ParentStruct):

  def fun(self, name, type, val):
    while a > 5 and c <= 9 or (a == 12 and c < d):
      print("hello")
	  
# Some comment
```
