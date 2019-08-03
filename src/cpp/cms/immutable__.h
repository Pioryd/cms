#ifndef FW_CMS_IMMUTABLE__H
#define FW_CMS_IMMUTABLE__H

#include <atomic>

namespace cms {
template <class T>
class base__ {
 public:
  base__(T* object__pointer)
      : references_(1), object__pointer_(object__pointer) {}
  virtual ~base__() {}

  void increase_reference() { ++references_; }
  void decrease_reference() {
    if (--references_ == 0) {
      delete object__pointer_;
      object__pointer_ = nullptr;
      delete this;
    }
  }

  void set(T* new_object__pointer) {
    T* previous_object__pointer = object__pointer_;
    object__pointer_ = new_object__pointer;
    if (previous_object__pointer) delete previous_object__pointer;
  }
  T* get() { return object__pointer_; }

  long use_count() { return references_; }

 private:
  std::atomic<long> references_;
  std::atomic<T*> object__pointer_;
};

template <class T>
class immutable__ {
 public:
  typedef T element_type;

  immutable__() : base(nullptr) {}
  immutable__(T* object__pointer) {
    base =
        (object__pointer != nullptr) ? new base__<T>(object__pointer) : nullptr;
  }
  immutable__(immutable__ const& rhs) : base(rhs.base) {
    if (base != nullptr) base->increase_reference();
  }
  ~immutable__() {
    if (base != nullptr) base->decrease_reference();
  }

  T& operator*() const { return *base->get(); }
  T* operator->() const { return base->get(); }

  immutable__& operator=(immutable__ const& rhs) {
    immutable__(rhs).swap_(*this);
    return *this;
  }
  immutable__& operator=(T* rhs) {
    immutable__(rhs).swap_(*this);
    return *this;
  }

  explicit operator bool() {
    return base == nullptr ? nullptr : &immutable__::base;
  }

  bool operator!() const { return base == nullptr; }

  T* object_() { return base->get(); }
  void swap_(immutable__& rhs) { std::swap(base, rhs.base); }

 protected:
  base__<T>* base;
};
}  // namespace cms

#endif  // #ifndef FW_CMS_IMMUTABLE__H
