cmake_minimum_required(VERSION 3.12)

project(MyOpenCVProject)

find_package(OpenCV REQUIRED)
find_package(CUDA REQUIRED)

set(CMAKE_CXX_STANDARD 11)

add_executable(MyApp main.cpp)

target_link_libraries(MyApp ${OpenCV_LIBS} ${CUDA_LIBRARIES})
