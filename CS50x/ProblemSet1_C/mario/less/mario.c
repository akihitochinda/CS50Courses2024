#include <cs50.h>
#include <stdio.h>

void print_space(int spaces);
void print_row(int bricks);

int main(void)
{
    // Prompt the user for the pyramid's height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1);

    // Print a pyramid of that height
    for (int i = 0; i < n; i++)
    {
        // Print row of bricks
        print_space(n - i - 1);
        // Print row of bricks
        print_row(i + 1);
    }
}
void print_space(int spaces)
{

    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
}

void print_row(int bricks)
{
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }
    printf("\n");
}
