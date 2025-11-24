#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// prototype
bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Make sure program was run with just one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Make sure every character in argv[1] is a digit
    bool result = only_digits(argv[1]);
    if (result != 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert argv[1] from a `string` to an `int`
    int k = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext:  ");

    // For each character in the plaintext:
    for (int i = 0, len = strlen(plaintext); i < len; i++)
    {
        // Rotate the character if it's a letter
        plaintext[i] = rotate(plaintext[i], k);
    }

    printf("ciphertext: %s\n", plaintext);
}

bool only_digits(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (isalpha(s[i]))
        {
            return 1;
        }
    }

    return 0;
}

char rotate(char c, int n)
{
    int value = 0;

    // ciphertext = (plaintext + k) % 26;
    if (isalpha(c))
    {
        if (isupper(c) && 'Z' > c + n)
        {
            value = (c + n);
        }
        else if (isupper(c) && 'Z' <= c + n)
        {
            value = (c - 'A' + n) % 26 + 'A';
        }
        else if (islower(c) && 'z' > c + n)
        {
            value = (c + n);
        }
        else if (islower(c) && 'z' <= c + n)
        {
            value = (c - 'a' + n) % 26 + 'a';
        }
    }
    else
    {
        value = c;
    }

    return value;
}
