# GLIBC compatibility header

This project provides header files `glibc-X.Y.h` that contain versioned symbols from specific versions of GLIBC. When using one of these headers the compiler is directed to use the specific versions of the symbols mentioned in the header and because GLIBC is backwards compatible the resulting program will run on any GLIBC-based Linux distribution that has this or a later version of GLIBC.

The easiest way to use one of the `glibc-X.Y.h` headers is by including the `-include glibc-X.Y.h` GCC option when building your project. For example, you may include this option in your `CFLAGS`, etc.

## Caveats

When using `glibc-X.Y.h` you should be aware of the following caveats:

- You might miss important bug fixes in newer symbols.

- It is likely that multiple versions of the same symbol might be used when dyna-linking with other libs. For example, `fprintf@GLIBC_2.x` might be used by the main executable and `fprintf@GLIBC_2.y` might be used by a `dlopen`'ed library.

- It is possible that using old symbols with new headers can also cause problems. For example, suppose that a new header changed the definition of an internal `struct` that is accessed via a macro or inline from the header file. We could then have code in the executable using both the new `struct` definition via the macro and the old `struct` definition via the old symbol reference. (I am not aware of any such cases, but it is a possibility.)

- This approach will build executables that run on glibc-based systems. Distros that uses other libc's (e.g. Alpine/MUSL) are not supported.

## Header Generation

In order to generate a `glibc-X.Y.h` header file locate the libc in your system and issue the command below:

```
objdump -T /PATH/TO/libc-X.Y.so | python3 gensym.py > glibc-X.Y.h
```

## License

The License gives you all the freedoms of the MIT License, except that you may NOT remove the License notice from any of the files.
