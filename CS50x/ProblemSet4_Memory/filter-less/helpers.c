#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Take average of red, green, and blue
            RGBTRIPLE *pixel = &image[i][j];
            int average = round(((*pixel).rgbtBlue + (*pixel).rgbtGreen + (*pixel).rgbtRed) / 3.0);

            // Update pixel values
            (*pixel).rgbtBlue = (int) average;
            (*pixel).rgbtGreen = (int) average;
            (*pixel).rgbtRed = (int) average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Compute sepia values
            RGBTRIPLE *pixel = &image[i][j];
            int sepiaRed = round(0.393 * (*pixel).rgbtRed + 0.189 * (*pixel).rgbtBlue +
                                 0.769 * (*pixel).rgbtGreen);
            int sepiaGreen = round(0.349 * (*pixel).rgbtRed + 0.168 * (*pixel).rgbtBlue +
                                   0.686 * (*pixel).rgbtGreen);
            int sepiaBlue = round(0.272 * (*pixel).rgbtRed + 0.131 * (*pixel).rgbtBlue +
                                  0.534 * (*pixel).rgbtGreen);

            // Update pixel with sepia values
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            (*pixel).rgbtBlue = sepiaBlue;
            (*pixel).rgbtGreen = sepiaGreen;
            (*pixel).rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop over all pixels
    for (int i = 0; i < height; i++)
    {
        int end = width - 1;
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][end];
            image[i][end] = tmp;
            end--;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int counter = 0, red = 0, green = 0, blue = 0;
            // Current pixel
            red += copy[i][j].rgbtRed;
            green += copy[i][j].rgbtGreen;
            blue += copy[i][j].rgbtBlue;
            counter++;

            // Check if pixel above and to the left exists
            if (i - 1 >= 0 && j - 1 >= 0)
            {
                red += copy[i - 1][j - 1].rgbtRed;
                green += copy[i - 1][j - 1].rgbtGreen;
                blue += copy[i - 1][j - 1].rgbtBlue;
                counter++;
            }
            // Pixel directly above
            if (i - 1 >= 0 && j >= 0)
            {
                red += copy[i - 1][j].rgbtRed;
                green += copy[i - 1][j].rgbtGreen;
                blue += copy[i - 1][j].rgbtBlue;
                counter++;
            }
            // Pixel above and to the right
            if (i - 1 >= 0 && j + 1 < width)
            {
                red += copy[i - 1][j + 1].rgbtRed;
                green += copy[i - 1][j + 1].rgbtGreen;
                blue += copy[i - 1][j + 1].rgbtBlue;
                counter++;
            }
            // Pixel to the left
            if (j - 1 >= 0)
            {
                red += copy[i][j - 1].rgbtRed;
                green += copy[i][j - 1].rgbtGreen;
                blue += copy[i][j - 1].rgbtBlue;
                counter++;
            }
            // Pixel to the right
            if (j + 1 < width)
            {
                red += copy[i][j + 1].rgbtRed;
                green += copy[i][j + 1].rgbtGreen;
                blue += copy[i][j + 1].rgbtBlue;
                counter++;
            }
            // Pixel below and to the left
            if (i + 1 < height && j - 1 >= 0)
            {
                red += copy[i + 1][j - 1].rgbtRed;
                green += copy[i + 1][j - 1].rgbtGreen;
                blue += copy[i + 1][j - 1].rgbtBlue;
                counter++;
            }
            // Pixel directly below
            if (i + 1 < height && j >= 0)
            {
                red += copy[i + 1][j].rgbtRed;
                green += copy[i + 1][j].rgbtGreen;
                blue += copy[i + 1][j].rgbtBlue;
                counter++;
            }
            // Pixel below and to the right
            if (i + 1 < height && j + 1 < width)
            {
                red += copy[i + 1][j + 1].rgbtRed;
                green += copy[i + 1][j + 1].rgbtGreen;
                blue += copy[i + 1][j + 1].rgbtBlue;
                counter++;
            }

            image[i][j].rgbtRed = round(red / (counter * 1.0));
            image[i][j].rgbtGreen = round(green / (counter * 1.0));
            image[i][j].rgbtBlue = round(blue / (counter * 1.0));
        }
    }
    return;
}
