# Python Generators - Advanced Data Processing

This project demonstrates advanced usage of Python generators to efficiently handle large datasets, process data in batches, and simulate real-world scenarios involving live updates and memory-efficient computations.

## Learning Objectives

- Master Python Generators for iterative data processing
- Handle Large Datasets with batch processing and lazy loading
- Simulate Real-world Scenarios with live data updates
- Optimize Performance using memory-efficient operations
- Apply SQL Knowledge for dynamic data fetching

## Project Structure

### Files

1. **`seed.py`** - Database setup and data seeding
   - Creates MySQL database `ALX_prodev`
   - Sets up `user_data` table with UUID primary key
   - Populates database from CSV file

2. **`0-stream_users.py`** - Generator for streaming database rows
   - Implements `stream_users()` generator
   - Yields user data one row at a time from database

3. **`1-batch_processing.py`** - Batch processing for large datasets
   - `stream_users_in_batches(batch_size)` - fetches data in batches
   - `batch_processing(batch_size)` - filters users over age 25

4. **`2-lazy_paginate.py`** - Lazy loading with pagination
   - `paginate_users(page_size, offset)` - fetches specific page
   - `lazy_pagination(page_size)` - generator for lazy page loading

5. **`4-stream_ages.py`** - Memory-efficient aggregation
   - `stream_user_ages()` - yields ages one by one
   - `calculate_average_age()` - computes average without loading all data

## Database Schema

The `user_data` table contains:
- `user_id` (CHAR(36), Primary Key, UUID, Indexed)
- `name` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(255), NOT NULL) 
- `age` (DECIMAL(3,0), NOT NULL)

## Key Features

### Memory Efficiency
- Uses generators with `yield` to process data one item at a time
- Minimizes memory footprint for large datasets
- Implements lazy loading patterns

### Database Integration
- MySQL connectivity with proper connection handling
- Dynamic SQL queries with parameterized statements
- Efficient cursor management and resource cleanup

### Batch Processing
- Configurable batch sizes for optimal performance
- Offset-based pagination for large result sets
- Stream processing with filtering capabilities

### Error Handling
- Robust exception handling for database operations
- Graceful connection management
- Resource cleanup in finally blocks

## Usage Examples

### Basic Streaming
```python
from itertools import islice

# Stream first 6 users
for user in islice(stream_users(), 6):
    print(user)
```

### Batch Processing
```python
# Process users over 25 in batches of 50
batch_processing(50)
```

### Lazy Pagination
```python
# Paginate through data 100 records at a time
for page in lazy_pagination(100):
    for user in page:
        print(user)
```

### Memory-Efficient Aggregation
```python
# Calculate average age without loading all data
average_age = calculate_average_age()
print(f"Average age: {average_age:.2f}")
```

## Requirements

- Python 3.x
- MySQL Server
- `mysql-connector-python` package
- Understanding of generator functions and `yield`
- Basic SQL knowledge

## Setup

1. Install MySQL and create appropriate user/permissions
2. Update database credentials in `seed.py`
3. Ensure `user_data.csv` file is available
4. Run `seed.py` to initialize database and import data

## Performance Benefits

- **Memory Usage**: Generators use constant memory regardless of dataset size
- **Processing Speed**: Lazy evaluation processes only needed data
- **Scalability**: Handles datasets too large for memory
- **Resource Management**: Efficient database connection handling

This implementation showcases best practices for handling large-scale data processing in Python using generators, making it suitable for real-world applications dealing with substantial datasets.