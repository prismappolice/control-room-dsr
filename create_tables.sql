-- PostgreSQL table creation for Control Room DSR
-- Users table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(120),
    password_hash VARCHAR(255),
    user_type VARCHAR(20) NOT NULL,
    district_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_password_change TIMESTAMP
);

-- DSR entries table  
CREATE TABLE IF NOT EXISTS dsr_entry (
    id SERIAL PRIMARY KEY,
    district_name VARCHAR(100) NOT NULL,
    form_type VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES "user"(id)
);

-- Control room uploads table
CREATE TABLE IF NOT EXISTS control_room_upload (
    id SERIAL PRIMARY KEY,
    date DATE,
    upload_type VARCHAR(50),
    filename VARCHAR(255),
    original_filename VARCHAR(255), 
    file_path VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES "user"(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_dsr_entry_district_date ON dsr_entry(district_name, date);
CREATE INDEX IF NOT EXISTS idx_dsr_entry_form_type ON dsr_entry(form_type);
CREATE INDEX IF NOT EXISTS idx_user_username ON "user"(username);