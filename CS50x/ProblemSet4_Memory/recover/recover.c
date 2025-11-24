#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK 512
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");

    // Create a buffer for a block of data
    uint8_t buffer[512];

    int count = 0;
    char filename[8];
    FILE *img = NULL;

    // While there's still data left to read from the memory card
    while (fread(buffer, 1, 512, card) == 512)
    {
        // Create JPEGs from the data
        // If start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (count > 0)
            {
                fclose(img);
            }

            // Filenames: ###.jpg, starting at 000.jpg
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            fwrite(buffer, sizeof(buffer), 1, img);

            count++;
        }
        // If already found JPEG
        else if (count > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, img);
        }
    }

    fclose(card);
    fclose(img);
}
