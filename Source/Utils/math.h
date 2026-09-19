#pragma once

#ifdef _EXPORTING
#define MATH_API __declspec(dllexport)
#elif _IMPORTING
#define MATH_API __declspec(dllimport)
#else
#define MATH_API
#endif

namespace LifeExe
{
MATH_API int max(int x, int y);
MATH_API int factorial(int n);
MATH_API int randomInt(int min, int max);
MATH_API float randomFloat(float min, float max);
}  // namespace LifeExe
