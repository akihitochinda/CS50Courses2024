#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt the user for some text

    string text = get_string("Text: ");

    // Count the number of letters, words, and sentences in the text
    double letters = count_letters(text);
    double words = count_words(text);
    double sentences = count_sentences(text);

    double L = 0;
    double S = 0;

    if (words >= 1)
    {
        L = letters / words * 100;
        S = sentences / words * 100;
    }

    // Compute the Coleman-Liau index
    double index = 0.0588 * L - 0.296 * S - 15.8;
    int result = round(index);

    // Print the grade level
    if (16 <= result)
    {
        printf("Grade 16+\n");
    }
    else if (result < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (1 <= result && result < 2)
    {
        printf("Grade 1\n");
    }
    else if (2 <= result && result < 3)
    {
        printf("Grade 2\n");
    }
    else if (3 <= result && result < 4)
    {
        printf("Grade 3\n");
    }
    else if (4 <= result && result < 5)
    {
        printf("Grade 4\n");
    }
    else if (5 <= result && result < 6)
    {
        printf("Grade 5\n");
    }
    else if (6 <= result && result < 7)
    {
        printf("Grade 6\n");
    }
    else if (7 <= result && result < 8)
    {
        printf("Grade 7\n");
    }
    else if (8 <= result && result < 9)
    {
        printf("Grade 8\n");
    }
    else if (9 <= result && result < 10)
    {
        printf("Grade 9\n");
    }
    else if (10 <= result && result < 11)
    {
        printf("Grade 10\n");
    }
    else if (11 <= result && result < 12)
    {
        printf("Grade 11\n");
    }
    else if (13 <= result && result < 14)
    {
        printf("Grade 13\n");
    }
    else if (14 <= result && result < 15)
    {
        printf("Grade 14\n");
    }
    else if (15 <= result && result < 16)
    {
        printf("Grade 15\n");
    }
}

int count_letters(string text)
{
    // Keep track of count
    int count = 0;

    // Return the number of letters in text
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (isupper(text[i]) || islower(text[i]))
        {
            count = count + 1;
        }
    }
    //    printf("%d\n",count);
    return count;
}

int count_words(string text)
{
    // Keep track of count
    int count = 0;

    // Return the number of words in text
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == ' ')
        {
            count = count + 1;
        }
    }
    count = count + 1;
    //    printf("%d\n",count);
    return count;
}

int count_sentences(string text)
{
    // Keep track of count
    int count = 0;

    // Return the number of sentences in text
    for (int i = 0, len = strlen(text); i < len; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            count = count + 1;
        }
    }
    //    printf("%d\n",count);
    return count;
}
