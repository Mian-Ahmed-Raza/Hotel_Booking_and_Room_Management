# Database Schema

## Tables

### users
Stores user account information with hashed passwords.

| Column    | Type          | Constraints                 | Description                    |
|-----------|---------------|----------------------------|--------------------------------|
| id        | INT           | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier         |
| username  | VARCHAR(100)  | UNIQUE, NOT NULL            | Login username                 |
| password  | VARCHAR(255)  | NOT NULL                    | SHA-256 hashed password        |
| full_name | VARCHAR(255)  | NULL                        | User's full name               |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `username`

**Engine:** InnoDB

## Future Tables (To Be Implemented)

### rooms
| Column      | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | INT           | Room identifier                |
| room_number | VARCHAR(10)   | Room number                    |
| room_type   | VARCHAR(50)   | Type (Single, Double, Suite)   |
| price       | DECIMAL(10,2) | Price per night                |
| status      | VARCHAR(20)   | Available, Occupied, Maintenance|

### bookings
| Column      | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | INT           | Booking identifier             |
| user_id     | INT           | Foreign key to users           |
| room_id     | INT           | Foreign key to rooms           |
| check_in    | DATE          | Check-in date                  |
| check_out   | DATE          | Check-out date                 |
| status      | VARCHAR(20)   | Confirmed, Checked-in, Completed|
| total_price | DECIMAL(10,2) | Total booking price            |

### payments
| Column      | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | INT           | Payment identifier             |
| booking_id  | INT           | Foreign key to bookings        |
| amount      | DECIMAL(10,2) | Payment amount                 |
| payment_date| TIMESTAMP     | When payment was made          |
| method      | VARCHAR(50)   | Payment method                 |
| status      | VARCHAR(20)   | Pending, Completed, Refunded   |

### reviews
| Column      | Type          | Description                    |
|-------------|---------------|--------------------------------|
| id          | INT           | Review identifier              |
| booking_id  | INT           | Foreign key to bookings        |
| rating      | INT           | Rating (1-5)                   |
| comment     | TEXT          | Review comment                 |
| created_at  | TIMESTAMP     | When review was created        |

## SQL Commands

### Create Database
```sql
CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### View Current Schema
```sql
USE hotel_db;
SHOW TABLES;
DESCRIBE users;
```

### Create Admin User Manually
```sql
USE hotel_db;
-- Password: admin123 (hashed)
INSERT INTO users (username, password, full_name) 
VALUES ('admin', 
        '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 
        'Administrator');
```

### Reset Database
```sql
DROP DATABASE hotel_db;
CREATE DATABASE hotel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
Then run `python setup.py` to recreate tables.
