# CMS (C++ Modular Scripting) [*Early Access*]

<img align="left" src="doc/cms_struct.png">

* **Project Status:**
  - Build: Stable
  * Type: Early Access
  * Tests: Full
  * Documentation: source full

**CMS allow to script in C++ syntax.**

Can work in 2 ways:
* compiled as c++ source
* scripted as converted to python

For example CMS(C++) file converted to python file:

 **C++:**
```cpp
#include <cms>

cms::sometype type_1 = INITIALIZER_LIST("heel", "check", "top")

struct MyStruct : OtherStruct, ParentStruct { 
  void fun(const cms::string& name, int* type, char val) {
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
## Examples
See examples folder to check how files are converted from CMS(C++) to python.
