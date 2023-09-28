#include <archive.h>
#include <archive_entry.h>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <string>
#include <string_view>
#include <vector>
#include <algorithm>

// defines colors for terminal output
constexpr std::string_view BLACK       = "\033[0;30m";
constexpr std::string_view RED         = "\033[0;31m";
constexpr std::string_view GREEN       = "\033[0;32m";
constexpr std::string_view YELLOW      = "\033[0;33m";
constexpr std::string_view BLUE        = "\033[0;34m";
constexpr std::string_view MAGENTA     = "\033[0;35m";
constexpr std::string_view CYAN        = "\033[0;36m";
constexpr std::string_view WHITE       = "\033[0;37m";
constexpr std::string_view RESET_COLOR = "\033[0;0m";


namespace fs = std::filesystem;

// Function to get the current time in HH:MM:SS format
std::string getCurrentTime() {
    time_t now = time(nullptr);
    struct tm tm_info {};
    localtime_r(&now, &tm_info);

    char timeStr[9];
    strftime(timeStr, sizeof(timeStr), "%T", &tm_info);
    return timeStr;
}

void displayPrompt(const fs::path &currentDir, int commandsCounter, const std::string &archivePath) {
    std::cout << GREEN << "┌─" << RED << "[ " << RESET_COLOR << getCurrentTime() << RED << " ]"
              << "─────[ vshell"
              << GREEN << "@" << BLUE << archivePath << RED << " ]───[ " << RESET_COLOR << commandsCounter << RED
              << " ]\n";
    std::cout << GREEN << "|\n";
    std::cout << "└─[ " << RESET_COLOR << std::string(currentDir) << GREEN << " ]────► \033[0m";
}

void extractArchive(const std::string &archivePath, const std::string &extractPath) {
    struct archive *a;
    struct archive *ext;
    struct archive_entry *entry;
    int r;

    a = archive_read_new();
    archive_read_support_filter_all(a);
    archive_read_support_format_all(a);
    ext = archive_write_disk_new();
    archive_write_disk_set_options(ext, ARCHIVE_EXTRACT_TIME);
    archive_write_disk_set_standard_lookup(ext);

    if ((r = archive_read_open_filename(a, archivePath.c_str(), 10240))) {
        std::cerr << RED << "Failed to open archive: " << YELLOW << archive_error_string(a) << RESET_COLOR << std::endl;
        return;
    }

    while (archive_read_next_header(a, &entry) == ARCHIVE_OK) {
        const char *entryPath = archive_entry_pathname(entry);
        fs::path outputPath   = fs::path(extractPath) / entryPath;

        archive_entry_set_pathname(entry, outputPath.string().c_str());

        if ((r = archive_write_header(ext, entry)) != ARCHIVE_OK) {
            std::cerr << RED << "Failed to write archive header: " << YELLOW << archive_error_string(ext) << RESET_COLOR << std::endl;
            return;
        }

        if (archive_entry_size(entry) > 0) {
            char buffer[8192];
            size_t size;
            while ((size = archive_read_data(a, buffer, sizeof(buffer))) > 0) {
                if (archive_write_data(ext, buffer, size) != size) {
                    std::cerr << RED << "Failed to write data to file: " << YELLOW << archive_error_string(ext) << RESET_COLOR << std::endl;
                    return;
                }
            }
        }
        archive_write_finish_entry(ext);
    }
    archive_read_close(a);
    archive_read_free(a);
    archive_write_close(ext);
    archive_write_free(ext);
}

void vshell(const std::string &archivePath) {
    const std::string tempDir = "temp_extracted";
    fs::create_directory(tempDir);
    extractArchive(archivePath, tempDir);

    std::string currentDir = tempDir;

    int commandsCounter = 0;

    while (true) {
        currentDir = fs::relative(currentDir);

        displayPrompt(std::string(currentDir), commandsCounter, archivePath);

        std::string command;
        std::getline(std::cin, command);

        if (command == "exit") {
            break;
        } else if (command == "pwd") {
            std::cout << currentDir << std::endl;
        } else {
            // Split the command into tokens
            std::istringstream iss(command);
            std::vector<std::string> tokens(std::istream_iterator<std::string>{iss},
                                            std::istream_iterator<std::string>());

            if (tokens.empty()) {
                continue;  // Empty command, continue the loop
            }

            if (tokens[0] == "ls") {
                // Handle the "ls" command
                std::string pathToList = (tokens.size() > 1) ? tokens[1] : ".";  // Default to current directory
                fs::path listPath      = currentDir + "/" + pathToList;

                if (fs::exists(listPath) && fs::is_directory(listPath)) {
                    for (const auto &entry : fs::directory_iterator(listPath)) {
                        std::cout << std::string(entry.path().filename()) << std::endl;
                    }
                } else {
                    std::cerr << RED << "Directory not found: " << YELLOW << pathToList << RESET_COLOR << std::endl;
                }
            } else if (tokens[0] == "cd") {
                // Handle the "cd" command
                if (tokens.size() > 1) {
                    std::string newDir = tokens[1];
                    if (newDir == ".." || newDir == "../") {
                        // Check for "cd ../" and move up one directory
                        if (currentDir != tempDir) {
                            currentDir = fs::path(currentDir).parent_path();
                        }
                    } else if (newDir == "/" || std::all_of(newDir.begin(), newDir.end(), [](char c) { return c == '/'; })) {
                        // Go to the root directory
                        currentDir = tempDir;
                    } else {
                        fs::path newPath = currentDir + "/" + newDir;

                        if (fs::is_directory(newPath)) {
                            currentDir = newPath;
                        } else {
                            std::cerr << RED << "Directory not found: " << YELLOW << newDir << RESET_COLOR << std::endl;
                        }
                    }
                } else if (tokens.size() == 1) {
                    currentDir = tempDir;
                } else {
                    std::cerr << RED << "Usage: " << CYAN << "cd <directory>" << RESET_COLOR << std::endl;
                }
            } else if (tokens[0] == "cat") {
                // Handle the "cat" command
                if (tokens.size() > 1) {
                    std::string filePath = tokens[1];
                    fs::path fullPath    = currentDir + "/" + filePath;

                    if (fs::exists(fullPath)) {
                        if (fs::is_directory(fullPath)) {
                            std::cerr << RED << "Failed to read data from the file: " << YELLOW << std::string(fullPath) << ": Is a directory" << RESET_COLOR << std::endl;
                        } else {
                            std::ifstream file(fullPath);
                            if (file) {
                                std::cout << file.rdbuf();
                            } else {
                                std::cerr << RED << "Failed to open file: " << YELLOW << fullPath << RESET_COLOR << std::endl;
                            }
                        }
                    } else {
                        std::cerr << RED << "File not found: " << YELLOW << fullPath << RESET_COLOR << std::endl;
                    }
                } else {
                    std::cerr << RED << "Usage: " << CYAN << "cat <file>" << RESET_COLOR << std::endl;
                }
            } else {
                std::cerr << RED << "Unknown command: " << MAGENTA << tokens[0] << RESET_COLOR << std::endl;
            }
        }
        commandsCounter++;
    }

    fs::remove_all(tempDir);
}

int main(int argc, char *argv[]) {
    if (argc != 3 || std::string(argv[1]) != "--script") {
        std::cerr << "Usage: " << CYAN << argv[0] << " --script <archive_file>" << RESET_COLOR << std::endl;
        return 1;
    } else if (!fs::exists(argv[2])) {
        std::cerr << argv[2] << " doesn't exist." << RESET_COLOR << std::endl;
        return 1;
    }

    std::string archivePath = argv[2];
    vshell(archivePath);

    return 0;
}
