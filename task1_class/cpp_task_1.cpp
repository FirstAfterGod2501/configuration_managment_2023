#include <iostream>
#include <string>
#include <unordered_set>

bool isValidChar(char c)
{
    return (c >= 'a' && c <= 'z') ||
           (c >= 'A' && c <= 'Z') ||
           (c >= '0' && c <= '9') ||
           (c == '_');
}

std::unordered_set<std::string> extractIdentifiers(const std::string& code)
{
    std::unordered_set<std::string> identifiers;
    std::string currentIdentifier;

    for (char c : code)
    {
        if (isValidChar(c))
        {
            currentIdentifier += c;
        }
        else if (!currentIdentifier.empty())
        {
            identifiers.insert(currentIdentifier);
            currentIdentifier.clear();
        }
    }

    if (!currentIdentifier.empty())
    {
        identifiers.insert(currentIdentifier);
    }

    return identifiers;
}

int main()
{
    std::string code = "int main() { int a = 5; int b = 10; return a + b; }";
    std::unordered_set<std::string> identifiers = extractIdentifiers(code);

    for (const auto& identifier : identifiers)
    {
        std::cout << identifier << std::endl;
    }

    return 0;
}