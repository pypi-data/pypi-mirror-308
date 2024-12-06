
#ifndef HYPERGIRGS_API_H
#define HYPERGIRGS_API_H

#ifdef HYPERGIRGS_STATIC_DEFINE
#  define HYPERGIRGS_API
#  define HYPERGIRGS_NO_EXPORT
#else
#  ifndef HYPERGIRGS_API
#    ifdef hypergirgs_EXPORTS
        /* We are building this library */
#      define HYPERGIRGS_API __attribute__((visibility("default")))
#    else
        /* We are using this library */
#      define HYPERGIRGS_API __attribute__((visibility("default")))
#    endif
#  endif

#  ifndef HYPERGIRGS_NO_EXPORT
#    define HYPERGIRGS_NO_EXPORT __attribute__((visibility("hidden")))
#  endif
#endif

#ifndef HYPERGIRGS_DEPRECATED
#  define HYPERGIRGS_DEPRECATED __attribute__ ((__deprecated__))
#endif

#ifndef HYPERGIRGS_DEPRECATED_EXPORT
#  define HYPERGIRGS_DEPRECATED_EXPORT HYPERGIRGS_API HYPERGIRGS_DEPRECATED
#endif

#ifndef HYPERGIRGS_DEPRECATED_NO_EXPORT
#  define HYPERGIRGS_DEPRECATED_NO_EXPORT HYPERGIRGS_NO_EXPORT HYPERGIRGS_DEPRECATED
#endif

/* NOLINTNEXTLINE(readability-avoid-unconditional-preprocessor-if) */
#if 0 /* DEFINE_NO_DEPRECATED */
#  ifndef HYPERGIRGS_NO_DEPRECATED
#    define HYPERGIRGS_NO_DEPRECATED
#  endif
#endif

#endif /* HYPERGIRGS_API_H */
