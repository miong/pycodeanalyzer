package com.jcraft.jzlib;


final public class GenericClass<T>  {
    private T value;

    GenericClass(T val) {
        value = val;
    }

    public <K> void genericMethod(K otherType) {
        //DO nothing
    }

    public void set(T t) {
        this.value = t;
    }

    public T get() {
        return value;
    }
}


final public class GenericClassIntImpl extends GenericClass<Integer> {
    //Nothing
}
