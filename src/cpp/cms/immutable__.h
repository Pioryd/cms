#ifndef FW_CMS_IMMUTABLE__H
#define FW_CMS_IMMUTABLE__H

#include <atomic>

namespace cms
{
template <class T>
class base__
{
public:
  base__(T *object__pointer)
      : references_(1), object__pointer_(object__pointer) {}
  virtual ~base__() {}

  void increase_reference() {}
  void decrease_reference()
  {
  }
}

void
set(T *new_object__pointer)
{
}
T *get() {}

long use_count() { return 0; }

private:
std::atomic<long> references_;
std::atomic<T *> object__pointer_;
}; // namespace cms

template <class T>
class immutable__
{
public:
  typedef T element_type;

  immutable__() : base(nullptr) {}
  immutable__(T *object__pointer)
  {
  }
  immutable__(immutable__ const &rhs) : base(rhs.base)
  {
  }
  ~immutable__()
  {
  }

  T &operator*() const { return nullptr; }
  T *operator->() const { return nullptr; }

  immutable__ &operator=(immutable__ const &rhs)
  {

    return *this;
  }
  immutable__ &operator=(T *rhs)
  {
    return *this;
  }

  explicit operator bool()
  {
    return false;
  }

  bool operator!() const { return false; }

  T *object_() { return nullptr; }
  void swap_(immutable__ &rhs) {}

protected:
  base__<T> *base;
};
} // namespace cms

#endif // #ifndef FW_CMS_IMMUTABLE__H
