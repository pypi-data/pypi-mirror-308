
#ifndef GIRGS_API_H
#define GIRGS_API_H

#ifdef GIRGS_STATIC_DEFINE
#  define GIRGS_API
#  define GIRGS_NO_EXPORT
#else
#  ifndef GIRGS_API
#    ifdef girgs_EXPORTS
        /* We are building this library */
#      define GIRGS_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define GIRGS_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef GIRGS_NO_EXPORT
#    define GIRGS_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef GIRGS_DEPRECATED
#  define GIRGS_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef GIRGS_DEPRECATED_EXPORT
#  define GIRGS_DEPRECATED_EXPORT GIRGS_API GIRGS_DEPRECATED
#endif

#ifndef GIRGS_DEPRECATED_NO_EXPORT
#  define GIRGS_DEPRECATED_NO_EXPORT GIRGS_NO_EXPORT GIRGS_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef GIRGS_NO_DEPRECATED
#    define GIRGS_NO_DEPRECATED
#  endif
#endif

#endif /* GIRGS_API_H */
