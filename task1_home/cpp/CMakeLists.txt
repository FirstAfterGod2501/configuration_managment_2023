set(SHOULD_BE_TESTED ON)


if (LibArchive_FOUND)
    message(STATUS "libarchive found")
    include_directories(${LibArchive_INCLUDE_DIRS})

    add_executable(
            first_homework
            "${CMAKE_CURRENT_LIST_DIR}/main.cpp"
    )

    target_link_libraries(first_homework ${LibArchive_LIBRARIES})


else ()
    include(FetchContent)

    # Fetch libarchive
    FetchContent_Declare(
            libarchive
            GIT_REPOSITORY https://github.com/libarchive/libarchive.git
            GIT_TAG v3.5.2 # Specify the desired version
    )

    # Fetch libarchive during configuration step
    FetchContent_GetProperties(libarchive)
    if (NOT libarchive_POPULATED)
        FetchContent_Populate(libarchive)

        # Add libarchive as a subdirectory and build it
        add_subdirectory(${libarchive_SOURCE_DIR} ${libarchive_BINARY_DIR})
    endif ()

    # Specify where libarchive headers are located
    include_directories(${libarchive_SOURCE_DIR}/libarchive)

    add_executable(
            first_homework
            "${CMAKE_CURRENT_LIST_DIR}/main.cpp"
    )

    # Link against libarchive
    target_link_libraries(first_homework archive)

endif ()

set_property(TARGET first_homework PROPERTY ENABLE_EXPORTS ON)

target_link_libraries(test_first_homework first_homework)

set(testing_targets test_first_homework)