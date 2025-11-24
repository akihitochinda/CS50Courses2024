// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table: array of linked list
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // access linked list at that index in the hash table
    // start with cursor set to first item in linked list
    node *cursor = table[hash(word)];

    // traverse linked list
    while (cursor != NULL)
    {
        // keep moving cursor until you get to NULL, checking each node for the word
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number: assigns a number to every input corresponding to which "bucket" to store
// the word in
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    //    return toupper(word[0]) - 'A';

    int index = 0;

    // word, with alphabetical characters and possibly apotrophes
    for (int i = 0; word[i] != '\0'; i++)
        index += tolower(word[i]);

    // numerical indexbetween 0 and N - 1, inclusive, deterministic
    // larger N means more buckets, if your function ends up with a value greater than N, you can
    // take the value % N to get a value in the appropriate range
    return index % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    char word[LENGTH + 1];

    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");

    // Read each word in the file
    while (fscanf(source, "%s", word) != EOF)
    {
        // create a new node for each word
        node *new_node = malloc(sizeof(node));

        if (new_node == NULL)
        {
            unload();
            return false;
        }
        else
        {
            // Add each word to the hash table
            strcpy(new_node->word, word);

            // hash word to obtain a hash value
            int n = hash(new_node->word);

            // insert node into hash table at that location
            new_node->next = table[n];
            table[n] = new_node;
        }
    }
    // Close the dictionary file
    fclose(source);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int counter = 0;

    // iterate through hashtable
    for (int i = 0; i < N; i++)
    {
        // set pointer to head of list
        node *cursor = table[i];

        // traverse list
        while (cursor != NULL)
        {
            counter++;
            cursor = cursor->next;
        }
    }
    return counter;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        // traverse list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        free(cursor);
    }
    return true;
}
