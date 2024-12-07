# Movie and Series Library Management Project

This project provides a Python-based library management system for handling movie and TV series data. It includes modules to store, search, and filter essential information such as title, genre, release date, rating, director, cast, country, budget, box office revenue, and runtime, all accessible through a unified interface. The system enables efficient access to detailed records for both movies and series.

---

## Project Structure

The project is organized into the following directories and modules:


### Directory Overview

- **data/**: Contains CSV files (`pelis.csv` for movies and `series.csv` for series) with sample data.
- **library/**: Houses the core module for managing both movies and series.
- **examples/**: Includes sample data examples for movies and series, illustrating the type of information stored in the system.

---

## Modules Overview
### Peliculas Module
The **Peliculas** module handles series data operations

#### Class `Peliculas`
- **Constructor Parameters**:
  - `csv_file`: Path to the movies CSV file (default is pelis.csv).

- **Key Methods**:
- `add_movie(title, genre, rating):` Adds a new movie to the DataFrame and optionally to the CSV file.
- `search_by_title(title):` Searches for a movie by title. Returns a DataFrame of movies that match the title.
- `filter_by_genre(genre):` Filters movies by a specified genre (e.g., 'Action', 'Drama').
- `show_top_rating(top_n=10):` Displays the top-rated movies based on ratings.

```python
from peliculas.Peliculas import Peliculas

movies = Movies()

# Add a new movie
movies.add_movie("Inception", "Sci-Fi", 8.8)

# Search for a specific title in movies
movies.search_by_title("Inception")

# Display the top 3 rated movies
movies.**mostrar_top_rating**(3)
```

#### Class `Series`
- **Constructor Parameters**:
- `csv_file:` Path to the series CSV file (default is series.csv).

- **Key Methods**:
- `add_series(title, category, rating):` Adds a new series to the DataFrame and optionally to the CSV file.
- `search_by_title(title):` Searches for a series by title. Returns a DataFrame of series that match the title.
- `filter_by_category(category):` Filters series by a specified category (e.g., 'Drama', 'Comedy').
- `show_top_rating(top_n=10):` Displays the top-rated series based on ratings.

#### Example Usage
``` python
from series.Series import Series

series = Series()

# Add a new series
series.agregar_serie("New Series", "Comedy", 8.5)

# Search for a specific title in series
series.buscar_por_titulo("Breaking Bad")

# Display the top 3 rated series
series.mostrar_top_rating(3)
```

### Library Module

The **Library** module serves as the central interface for managing movie and series data, providing search and filtering functionality across both datasets.
#### Class `Library`

- **Constructor Parameters**:
  - `peliculas_csv`: Path to the movies CSV file (default is `pelis.csv`).
  - `series_csv`: Path to the series CSV file (default is `series.csv`).

- **Key Methods**:
  - `search_by_title(title)`: Searches for movie and series titles. Returns a dictionary with separate lists for movie and series results.
  - `show_top_rating(top_n=10)`: Displays the top-rated movies and series based on ratings.

#### Example Usage

```python
from library.Library import Library

library = Library()

# Search for a title in both movies and series
library.search_by_title("Inception")

# Display the top 3 rated titles
library.show_top_rating(3)
```

### Requirements

To install the required dependencies, run:

```pip install -r requirements.txt```

### Usage

1. Load the CSV files (pelis.csv and series.csv) in the data/ directory with your movie and series data.
2. Use the Library class from the library/ module to search for titles and display the top-rated movies and series.
3. Refer to Examples_Films.py and Examples_Series.py in the examples/ directory to see examples of how to structure movie and series dat
