
set(PROJECT_NAME MathLib)

set(MATH_SOURCES math.cpp)
set(MATH_INCLUDES math.h) 
add_library(MathLib STATIC ${MATH_SOURCES} ${MATH_INCLUDES})