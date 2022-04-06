
#ifndef StrangeMember_H_
#define StrangeMember_H_

#include <functional>

class StrangeMember {

public:
    void setCallback(std::function<void()> callback);

private:

    std::function<void()> mCallback;

};

#endif
