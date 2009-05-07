__doc__ = """Filters spam. After training on a corpus of ham and spam, add |"/path/to/spamfilter.py -o outputfile" to your .forward file, and then the program will add an additional header to your message indicating whether or not it is spam. Can also run in bulk on directories of files. Additional details on usage are in spamfilter.py's help message."""

__all__ = ['Brain','directory','spamfilter','tokenizer','tools']
