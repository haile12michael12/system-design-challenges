-- Initialize database for news service

-- Create articles table
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    author VARCHAR(100) NOT NULL,
    published_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_published BOOLEAN DEFAULT TRUE,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_articles_title ON articles(title);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at);

-- Create categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for categories
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);

-- Create user_preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    preferred_categories TEXT,
    preferred_authors TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for user_preferences
CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- Insert sample data
INSERT INTO categories (name, description) VALUES
    ('technology', 'Technology news and updates'),
    ('science', 'Scientific discoveries and research'),
    ('business', 'Business and economic news'),
    ('health', 'Health and medical news'),
    ('entertainment', 'Entertainment and celebrity news')
ON CONFLICT (name) DO NOTHING;

-- Insert sample articles
INSERT INTO articles (title, content, category, author, is_published) VALUES
    ('Introduction to FastAPI', 'FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.', 'technology', 'Author 1', TRUE),
    ('The Future of AI', 'Artificial Intelligence is rapidly evolving and changing the way we live and work.', 'technology', 'Author 2', TRUE),
    ('Climate Change Research', 'Recent studies show significant progress in understanding climate change patterns.', 'science', 'Author 3', TRUE),
    ('Market Trends 2023', 'Analysis of current market trends and economic forecasts for 2023.', 'business', 'Author 4', TRUE),
    ('Healthy Living Tips', 'Simple tips for maintaining a healthy lifestyle in busy modern times.', 'health', 'Author 5', TRUE)
ON CONFLICT DO NOTHING;