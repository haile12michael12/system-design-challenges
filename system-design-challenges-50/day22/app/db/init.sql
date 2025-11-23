-- Database initialization script

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id),
    content TEXT NOT NULL,
    media_url VARCHAR(255),
    likes_count INTEGER DEFAULT 0,
    comments_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create feed_cache table
CREATE TABLE IF NOT EXISTS feed_cache (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    feed_data TEXT NOT NULL,
    cache_key VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create metadata_rollup table
CREATE TABLE IF NOT EXISTS metadata_rollup (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INTEGER NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    metric_value BIGINT NOT NULL,
    rollup_period VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_feed_cache_user_id ON feed_cache(user_id);
CREATE INDEX IF NOT EXISTS idx_feed_cache_expires_at ON feed_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_metadata_rollup_entity ON metadata_rollup(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_metadata_rollup_metric ON metadata_rollup(metric_name);
CREATE INDEX IF NOT EXISTS idx_metadata_rollup_timestamp ON metadata_rollup(timestamp);